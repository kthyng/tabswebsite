'''
Update long-term data files.
'''

import tools
import buoy_properties as bp
import pandas as pd
from os import path
import run_daily as rd
import read


def longterm(table, buoy, dstart=pd.datetime(1980, 1, 1)):


    dend = pd.datetime.now()

    if len(buoy) == 1:
        fname = path.join('..', 'daily', 'tabs_' + buoy + '_' + table + '_all')
    else:
        fname = path.join('..', 'daily', table + '_' + buoy + '_all')

    # if file already exists, append whatever is new to it
    if path.exists(fname):
        # start from day after day from last line of file
        dstart = parse(open(fname).readlines()[-1][:10]) + pd.Timedelta('1 days')

        # append to file
        if (dend-dstart) < pd.Timedelta('30 days'):
            dftemp = read.read(table, buoy, dstart, dend)
            with open(fname, 'a') as f:
                tools.write_file(df, f, compression=False)
                # df.to_csv(f, sep='\t', header=False)
        else:  # more than 30 days difference
            date = dstart
            while date < pd.datetime.now():
                df = df.append(read.read(table, buoy, date, date + pd.Timedelta('30 days')))
                date += pd.Timedelta('31 days')
FINISH
    # if the file doesn't exist, read in from dstart
    else:
        # if buoy data is in mysql database, can read in all dates at once
        if bd.inmysql(buoy):
            if 'ndbc' in table:
                df = read.read_ndbc(buoy, dstart, dend)
            else:
                df = read.read_tabs(table, buoy, dstart, dend)
        else:
            df = pd.DataFrame()  # initialize
            date = dstart
            while date < pd.datetime.now():
                df = df.append(read.read(table, buoy, date, date + pd.Timedelta('30 days')))
                date += pd.Timedelta('31 days')

    return df


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
    elif len(buoy) > 1:
        query = 'SELECT * FROM ndbc_' + buoy + ' WHERE (date BETWEEN "' + dstart + '" AND "' + dend + '") order by obs_time'
    else:
        query = 'SELECT * FROM tabs_' + buoy + '_' + table + ' WHERE (date BETWEEN "' + dstart + '" AND "' + dend + '") order by obs_time'

    return query


if __name__ == "__main__":

    engine = tools.engine()

    # long_term(table, buoy)

    # loop through buoys: query, make text file, make plot
    # active buoys
    for buoy in bd.buoys():
        for table in bd.tables():  # loop through tables for each buoy

            if not buoy in bd.avail(table):
                continue  # instrument not available for this buoy
            else:
                # get base of table name
                if '-' in table:
                    table = table.split('-')[0]
                tools.read(table, buoy, dstart, end)

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
    # inactive buoys
    for buoy in bd.buoys(kind='inactive'):
        for table in bd.tables():  # loop through tables for each buoy

            if not buoy in bd.avail(table):
                continue  # instrument not available for this buoy
            else:
                if table != 'ndbc':
                    fname = path.join('..', 'daily', 'tabs_' + buoy + '_' + table + '_all')
                elif table == 'ndbc':
                    fname = path.join('..', 'daily', 'ndbc_' + buoy + '_all')
                # only remake files if they don't exist since they aren't changing
                if path.exists(fname):
                    continue
                else:
                    q = query_setup(engine, buoy, table)
                    df = tools.read([q, engine])
                    rd.make_text(df, fname, compression=True)  # .gz
                    rd.make_text(df, fname, compression=False) # not .gz
