'''
Update long-term data files.
'''

import tools
import buoy_data as bd
import pandas as pd
from os import path
import run_daily as rd


def query_setup(engine, buoy, table):
    '''Query mysql database for data, given end date dend from
    query_setup_recent().'''

    dstart = "1995-01-01"
    dend = pd.datetime.now().strftime("%Y-%m-%d %H:%M")
    # dstart = (dend - timedelta(days=ndays)).strftime("%Y-%m-%d")  # 5 days earlier

    # buoy C doesn't have date and time listed separately which is mostly fine except for when querying for one day
    # ndbc buoys diff too
    if buoy == 'C':
        query = 'SELECT * FROM tabs_' + buoy + '_' + table + ' WHERE (obs_time BETWEEN "' + dstart + '" AND "' + dend + '") order by obs_time'
    if len(buoy) > 1:
        query = 'SELECT * FROM ndbc_' + buoy + ' WHERE (date BETWEEN "' + dstart + '" AND "' + dend + '") order by obs_time'
    else:
        query = 'SELECT * FROM tabs_' + buoy + '_' + table + ' WHERE (date BETWEEN "' + dstart + '" AND "' + dend + '") order by obs_time'

    return query


if __name__ == "__main__":

    engine = tools.engine()

    # loop through buoys: query, make text file, make plot
    for buoy in bd.buoys():
        for table in bd.tables():  # loop through tables for each buoy

            if not buoy in bd.avail(table):
                continue  # instrument not available for this buoy
            else:
                # if table == 'ndbc' and buoy == 'PTAT2':
                #     import pdb; pdb.set_trace()
                q = query_setup(engine, buoy, table)
                df = tools.read([q, engine])
                if table != 'ndbc':
                    fname = path.join('..', 'daily', 'tabs_' + buoy + '_' + table + '_all')
                elif table == 'ndbc':
                    fname = path.join('..', 'daily', 'ndbc_' + buoy + '_all')
                # write daily data file, for whatever most recent time period
                # data was available
                rd.make_text(df, fname, compression=True)  # .gz
                rd.make_text(df, fname, compression=False) # not .gz
