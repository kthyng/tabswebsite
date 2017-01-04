'''
Create text files and plots of recent data.

Have both use/show 5 days of data if possible, and use the same mysql query.
Run on a cron job.
'''

import time
import pandas as pd
from sqlalchemy import create_engine
from datetime import timedelta
import numpy as np
import csv
import plot_buoy
import os

buoys = ['B','D','F','J','K','N','R','V','W','X']
tables = ['ven', 'met', 'eng', 'salt', 'wave']


def setup():
    '''Setup database for mysql querying.'''

    engine = create_engine('mysql+mysqldb://tabsweb:tabs@tabs1.gerg.tamu.edu/tabsdb')

    return engine


def query_setup(engine, buoy, table):
    '''Query mysql database for data.'''

    # query for last entry
    lastline = 'SELECT * FROM tabs_' + buoy + '_' + table + ' order by obs_time DESC limit 1'
    df = pd.read_sql_query(lastline, engine, index_col=['obs_time'])
    dend = df.index[0].strftime("%Y-%m-%d")  # date for last available data
    # dend = df.index[0].strftime("%Y-%m-%d %H:%M")  # datetime for last available data

    dstart = (df.index[0] - timedelta(days=5)).strftime("%Y-%m-%d")  # 5 days earlier

    # get 5 days of data
    query = 'SELECT * FROM tabs_' + buoy + '_' + table + ' WHERE (date BETWEEN "' + dstart + '" AND "' + dend + '") order by obs_time'
    return query
    # df = pd.read_sql_query(query, engine, index_col=['obs_time'])
    # # remove extra date/time columns
    # df = df.drop(['date','time'], axis=1)
    # df.columns = ['East', 'North', 'Dir', 'WaterT', 'Tx', 'Ty']
    # # df.columns = ['East [cm/s]', 'North [cm/s]', 'Dir to [&deg;T]',
    # #               'WaterT [&deg;C]', 'Tx', 'Ty']
    # df.index.name = 'Dates [UTC]'
    # # drop Tx, Ty
    # df = df.drop(['Tx','Ty'], axis=1)
    # # add magnitude
    # df['Speed'] = np.sqrt(df['East']**2 + df['North']**2)
    # # df['Speed [cm/s]'] = np.sqrt(df['East [cm/s]']**2 + df['North [cm/s]']**2)
    # # reorder
    # df = df[['East', 'North', 'Speed', 'Dir', 'WaterT']]
    # # df = df[['East [cm/s]', 'North [cm/s]', 'Speed [cm/s]', 'Dir to [&deg;T]',
    # #               'WaterT [&deg;C]']]
    # return df


def make_text(buoy, table):
    '''Make text files with 5 days of data'''

    df.to_csv(os.path.join('daily', 'tabs_' + buoy + '_' + table + '.txt'), sep='\t', na_rep='-999', float_format='%3.2f', header=False, quoting=csv.QUOTE_NONE,  escapechar=' ')

# reference plot_buoy for plots (all kinds not just ven)
# read in text from previously made text files


if __name__ == "__main__":

    engine = setup()

    # # loop through buoys: query, make text file, make plot
    # for buoy in buoys:
    #
    #     for table in tables:  # loop through tables for each buoy

    buoy = 'F'
    table = 'ven'
    q = query_setup(engine, buoy, table)
    # df = query_setup(engine, buoy, table)
    df = plot_buoy.read(buoy, [q, engine], table)

    # import pdb; pdb.set_trace()
    make_text(buoy, table)
    # make_plot(buoy, table)
    fig = plot_buoy.plot(df, buoy, table)
    fig.savefig(os.path.join('daily', 'tabs_' + buoy + '_' + table + '.pdf'))
    fig.savefig(os.path.join('daily', 'tabs_' + buoy + '_' + table + '.png'))
