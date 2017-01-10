'''
Create text files and plots of recent data.

Have both use/show 5 days of data if possible, and use the same mysql query.
Run on a cron job.
'''

import time
import pandas as pd
from datetime import timedelta
import numpy as np
import csv
import plot_buoy
import os
from matplotlib.pyplot import close
import tools


buoys = ['B','D','F','J','K','N','R','V','W','X']
tables = ['ven', 'met', 'eng', 'salt', 'wave']


def query_setup_recent(engine, buoy):
    '''return most recent datetime object for buoy that has reasonable data.

    Condition of data being reasonable is based on ven table tx!=-99.
    '''

    # query for last entry
    lastline = 'SELECT * FROM tabs_' + buoy + '_ven order by obs_time DESC limit 1'
    # read in query
    df = pd.read_sql_query(lastline, engine, index_col=['obs_time'])

    # check for real data, based on tx value
    counter = 1
    # while tx=-99 in the latest database entry, read in more lines from
    # database, 1 by 1, until finding one that has a real value.
    # Return the date time of this entry.
    while (df.tail(1)['tx'].values[0] == -99):
        counter += 1
        lastline = 'SELECT * FROM tabs_' + buoy + '_' + table + ' order by obs_time DESC limit ' + str(counter)
        df = pd.read_sql_query(lastline, engine, index_col=['obs_time'])

    return df.index[-1]  #.strftime("%Y-%m-%d %H:%M")  # date for last available data


def query_setup(engine, buoy, table, dend):
    '''Query mysql database for data, given end date dend from
    query_setup_recent().'''

    # dend = df.index[-1].strftime("%Y-%m-%d")  # date for last available data
    # dend = df.index[0].strftime("%Y-%m-%d %H:%M")  # datetime for last available data

    dstart = (dend - timedelta(days=5)).strftime("%Y-%m-%d")  # 5 days earlier
    # dstart = (df.index[-1] - timedelta(days=5)).strftime("%Y-%m-%d")  # 5 days earlier

    # get 5 days of data
    # want from beginning of first day but only up until data time on final day
    query = 'SELECT * FROM tabs_' + buoy + '_' + table + ' WHERE (date BETWEEN "' + dstart + '" AND "' + dend.strftime("%Y-%m-%d %H:%M") + '") order by obs_time'
    return query


# def make_text(df, buoy, table, fname):
def make_text(df, fname):
    '''Make text file of data'''

    df.to_csv(fname, sep='\t', na_rep='-999', float_format='%3.2f', quoting=csv.QUOTE_NONE,  escapechar='')
    # with no header:
    # df.to_csv(fname, sep='\t', na_rep='-999', float_format='%3.2f', header=False, quoting=csv.QUOTE_NONE,  escapechar=' ')


if __name__ == "__main__":

    engine = tools.engine()

    avail = {}
    avail['ven'] = ['B','D','F','J','K','N','R','V','W','X']
    avail['eng'] = ['B','D','F','J','K','N','R','V','W','X']
    avail['met'] = ['B', 'H', 'J', 'K', 'N', 'V']
    avail['salt'] = ['B', 'D', 'F', 'J', 'K', 'N', 'R', 'V', 'W', 'X']
    avail['wave'] = ['K', 'N', 'V', 'X']

    # loop through buoys: query, make text file, make plot
    for buoy in buoys:
        for table in tables:  # loop through tables for each buoy

            if table == 'ven':
                # find end date of recent legitimate data
                dend = query_setup_recent(engine, buoy)

            if not buoy in avail[table]:
                continue  # instrument not available for this buoy
            else:
                try:
                    q = query_setup(engine, buoy, table, dend)
                    df = tools.read([q, engine], buoy, table)
                    fname = os.path.join('daily', 'tabs_' + buoy + '_' + table)
                    make_text(df, fname)
                    # import pdb; pdb.set_trace()
                    fig = plot_buoy.plot(df, buoy, table)
                    fig.savefig(os.path.join('daily', 'tabs_' + buoy + '_' + table + '.pdf'))
                    fig.savefig(os.path.join('daily', 'tabs_' + buoy + '_' + table + '.png'))
                    # save smaller for hover
                    if table == 'ven':
                        fig.savefig(os.path.join('daily', 'tabs_' + buoy + '_' + table + '_low.png'), dpi=60)
                    close(fig)
                # if data isn't available at the same time as the ven file,
                # leave as not written
                except:
                    pass
