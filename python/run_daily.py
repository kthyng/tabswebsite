'''
Create text files and plots of recent data.

Have both use/show 5 days of data if possible, and use the same mysql query.
Run on a cron job.
'''

import pandas as pd
from datetime import timedelta
import numpy as np
from csv import QUOTE_NONE
import plot_buoy
from os import path
from matplotlib.pyplot import close
import tools
import buoy_data as bd
import buoy_header as bh


def query_setup_recent(engine, buoy, table):
    '''return most recent datetime object for buoy that has reasonable data.

    Condition of data being reasonable is based on ven table tx!=-99.
    '''

    # query for last entry
    if table == 'ndbc':
        lastline = 'SELECT * FROM ndbc_' + buoy + ' order by obs_time DESC limit 1'
    else:
        lastline = 'SELECT * FROM tabs_' + buoy + '_' + table + ' order by obs_time DESC limit 1'

    # read in query
    df = pd.read_sql_query(lastline, engine, index_col=['obs_time'])

    # check for real data, based on tx value - only for ven table
    counter = 1
    # while tx=-99 in the latest database entry, read in more lines from
    # database, 1 by 1, until finding one that has a real value.
    # Return the date time of this entry.
    if table == 'ven':
        while (df.tail(1)['tx'].values[0] == -99):
            counter += 1
            lastline = 'SELECT * FROM tabs_' + buoy + '_' + table + ' order by obs_time DESC limit ' + str(counter)
            df = pd.read_sql_query(lastline, engine, index_col=['obs_time'])

    return df.index[-1]  # date for last available data


def query_setup(engine, buoy, table, dstart, dend):
    '''Query mysql database for data, given end date dend from
    query_setup_recent().'''

    # get 5 days of data
    # want from beginning of first day but only up until data time on final day
    # buoy C doesn't have date and time listed separately which is mostly fine except for when querying for one day
    # ndbc buoys diff too
    if buoy == 'C':
        query = 'SELECT * FROM tabs_' + buoy + '_' + table + ' WHERE (obs_time BETWEEN "' + dstart + '" AND "' + dend.strftime("%Y-%m-%d %H:%M") + '") order by obs_time'
    elif len(buoy) > 1:
        query = 'SELECT * FROM ndbc_' + buoy + ' WHERE (date BETWEEN "' + dstart + '" AND "' + dend.strftime("%Y-%m-%d %H:%M") + '") order by obs_time'
    else:
        query = 'SELECT * FROM tabs_' + buoy + '_' + table + ' WHERE (date BETWEEN "' + dstart + '" AND "' + dend.strftime("%Y-%m-%d %H:%M") + '") order by obs_time'

    return query


def make_text(df, fname, compression=False):
    '''Make text file of data'''

    if compression:
        df.to_csv(fname + '.gz', sep='\t', na_rep='-999', float_format='%3.2f', quoting=QUOTE_NONE,  escapechar='', compression='gzip')
    else:
        df.to_csv(fname, sep='\t', na_rep='-999', float_format='%3.2f', quoting=QUOTE_NONE,  escapechar='')


if __name__ == "__main__":

    engine = tools.engine()

    # loop through buoys: query, make text file, make plot
    for buoy in bd.buoys():
        for table in bd.tables():  # loop through tables for each buoy

            if not buoy in bd.avail(table):
                continue  # instrument not available for this buoy
            else:
                if 'tcoon' not in table:  # tcoon are not in mysql
                    dend = query_setup_recent(engine, buoy, table)
                    # start 5 days earlier from last data
                    dstart = (dend - timedelta(days=5)).strftime("%Y-%m-%d")
                    q = query_setup(engine, buoy, table, dstart, dend)
                    df = tools.read([q, engine])
                elif 'tcoon' in table:
                    dend = pd.datetime.now()
                    # start 5 days earlier from last data
                    dstart = (dend - timedelta(days=5)).strftime("%Y%m%d")
                    # change dend to string
                    dend = dend.strftime("%Y%m%d")
                    # works whether -nomet or not
                    df = tools.read_tcoon(buoy, dstart, dend)
                if table != 'ndbc' and 'tcoon' not in table:
                    fname = path.join('..', 'daily', 'tabs_' + buoy + '_' + table)
                elif table == 'ndbc':
                    fname = path.join('..', 'daily', 'ndbc_' + buoy)
                elif 'tcoon' in table:
                    fname = path.join('..', 'daily', 'tcoon_' + buoy)
                # write daily data file, for whatever most recent time period
                # data was available
                make_text(df, fname)  # there is always data to write, but it might be old
                # if there are too few rows to plot, set as None
                if len(df) < 2:
                    df = None
                # no model output for TCOON stations since in bays
                if 'tcoon' in table:
                    dfmodelrecent = None
                    dfmodelforecast = None
                else:
                    # read in recent model output, not tied to when data output was found
                    now = pd.datetime.now()
                    past = (now - timedelta(days=5)).strftime("%Y-%m-%d")
                    future = (pd.datetime.now()+timedelta(days=5)).strftime('%Y-%m-%d %H:%M')
                    dfmodelrecent = tools.read_model(buoy, table, past, now.strftime('%Y-%m-%d %H:%M'), timing='recent')
                    # read in forecast model output, not tied to when data output was found
                    dfmodelforecast = tools.read_model(buoy, table, now.strftime('%Y-%m-%d'), future, timing='forecast')

                if table == 'wave' or table == 'eng' or dfmodelrecent is None or dfmodelforecast is None:
                    tlims = None
                else:
                    tlims = [dfmodelrecent.idx[0], dfmodelforecast.idx[-1]]
                # will plot model output from now if available, otherwise data regardless of how old
                fig = plot_buoy.plot(df, buoy, table, df1=None, df2=dfmodelrecent, df3=dfmodelforecast, tlims=tlims)
                fig.savefig(fname + '.pdf')
                fig.savefig(fname + '.png')
                # save smaller for hover
                fig.savefig(fname + '_low.png', dpi=60)
                close(fig)

    for buoy in bd.buoys():  # loop through buoys separately for buoy headers
        # write header
        bh.make(buoy)

    # separate for making currents summaries
    # use data that was calculated previously in this script
    dfs = []; buoys = []
    for buoy in bd.buoys():
        if len(buoy) > 1:  # don't include NDBC buoys
            continue
        fname = 'tabs_' + buoy + '_ven'
        df = tools.read(path.join('..', 'daily/', fname))
        # check if any of dataset is from within the past 5 days before appending
        if (pd.datetime.now() - df.index[-1]).days < 5:
            dfs.append(df)
        else:
            dfs.append(None)
        buoys.append(buoy)
    fig1 = plot_buoy.currents(dfs[:5], buoys[:5])
    fig2 = plot_buoy.currents(dfs[5:], buoys[5:])
    fig1.savefig(path.join('..', 'daily', 'currents1.pdf'))
    fig1.savefig(path.join('..', 'daily', 'currents1.png'))
    fig2.savefig(path.join('..', 'daily', 'currents2.pdf'))
    fig2.savefig(path.join('..', 'daily', 'currents2.png'))
    close(fig1)
    close(fig2)
