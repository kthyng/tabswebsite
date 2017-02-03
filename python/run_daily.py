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


def query_setup_recent(engine, buoy):
    '''return most recent datetime object for buoy that has reasonable data.

    Condition of data being reasonable is based on ven table tx!=-99.
    '''

    # query for last entry
    if len(buoy) == 1:
        lastline = 'SELECT * FROM tabs_' + buoy + '_ven order by obs_time DESC limit 1'
    elif len(buoy) > 1:
        lastline = 'SELECT * FROM ndbc_' + buoy + ' order by obs_time DESC limit 1'
    # read in query
    df = pd.read_sql_query(lastline, engine, index_col=['obs_time'])

    # check for real data, based on tx value
    counter = 1
    # while tx=-99 in the latest database entry, read in more lines from
    # database, 1 by 1, until finding one that has a real value.
    # Return the date time of this entry.
    if len(buoy) == 1:
        while (df.tail(1)['tx'].values[0] == -99):
            counter += 1
            lastline = 'SELECT * FROM tabs_' + buoy + '_' + table + ' order by obs_time DESC limit ' + str(counter)
            df = pd.read_sql_query(lastline, engine, index_col=['obs_time'])

    return df.index[-1]  # date for last available data


def query_setup(engine, buoy, table, dend):
    '''Query mysql database for data, given end date dend from
    query_setup_recent().'''

    dstart = (dend - timedelta(days=5)).strftime("%Y-%m-%d")  # 5 days earlier

    # get 5 days of data
    # want from beginning of first day but only up until data time on final day
    # buoy C doesn't have date and time listed separately which is mostly fine except for when querying for one day
    # ndbc buoys diff too
    if buoy == 'C':
        query = 'SELECT * FROM tabs_' + buoy + '_' + table + ' WHERE (obs_time BETWEEN "' + dstart + '" AND "' + dend.strftime("%Y-%m-%d %H:%M") + '") order by obs_time'
    if len(buoy) > 1:
        query = 'SELECT * FROM ndbc_' + buoy + ' WHERE (date BETWEEN "' + dstart + '" AND "' + dend.strftime("%Y-%m-%d %H:%M") + '") order by obs_time'
    else:
        query = 'SELECT * FROM tabs_' + buoy + '_' + table + ' WHERE (date BETWEEN "' + dstart + '" AND "' + dend.strftime("%Y-%m-%d %H:%M") + '") order by obs_time'

    return query


def make_text(df, fname):
    '''Make text file of data'''

    df.to_csv(fname, sep='\t', na_rep='-999', float_format='%3.2f', quoting=QUOTE_NONE,  escapechar='')
    # with no header:
    # df.to_csv(fname, sep='\t', na_rep='-999', float_format='%3.2f', header=False, quoting=csv.QUOTE_NONE,  escapechar=' ')


if __name__ == "__main__":

    engine = tools.engine()

    # loop through buoys: query, make text file, make plot
    # buoy = '42019'
    for buoy in bd.buoys():
        for table in bd.tables():  # loop through tables for each buoy
            if table == 'ven':
                if buoy in bd.avail('ven'):  # this condition due to ndbc buoys
                    # find end date of recent legitimate data
                    dend = query_setup_recent(engine, buoy)

            if not buoy in bd.avail(table):
                continue  # instrument not available for this buoy
            else:
                try:
                    import pdb; pdb.set_trace()
                    if table == 'ndbc':
                        dend = query_setup_recent(engine, buoy)
                    q = query_setup(engine, buoy, table, dend)
                    df = tools.read([q, engine])
                    if table != 'ndbc':
                        fname = path.join('..', 'daily', 'tabs_' + buoy + '_' + table)
                    elif table == 'ndbc':
                        fname = path.join('..', 'daily', 'ndbc_' + buoy)
                    # write daily data file
                    make_text(df, fname)
                    # read in model output
                    if table != 'ndbc':
                        dfmodelrecent = tools.read_model(q, timing='recent')
                        dfmodelforecast = tools.read_model(q, timing='forecast')
                    else:
                        dfmodelrecent = None
                        dfmodelforecast = None
                    # make and save plots
                    fig = plot_buoy.plot(df, buoy, table, dfmodelrecent, dfmodelforecast)
                    fig.savefig(fname + '.pdf')
                    fig.savefig(fname + '.png')
                    # save smaller for hover
                    fig.savefig(fname + '_low.png', dpi=60)
                    close(fig)
                # if data isn't available at the same time as the ven file,
                # leave as not written
                except:
                    pass

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
