'''
Update long-term data files.
'''

import tools
import buoy_properties as bp
import pandas as pd
from os import path
import run_daily as rd
import read

bys = bp.load() # load in buoy data

def longterm(buoy, table=None, dstart=pd.Timestamp('1980-1-1', tz='utc')):
    '''Creates or updates buoy data files.

    Reads through yesterday so that when appended to everything is consistent.
    This can take a long time to run.
    Note that dstart is ignored if buoy data file already exists.
    '''

    # bring data in file up through yesterday. This way files are
    # consistent regardless of what time of day script is run.
    dend = pd.Timestamp('now', tz='utc').normalize() - pd.Timedelta('1 day')
    # file write flag
    mode = 'w'

    if len(buoy) == 1:
        assert table is not None, 'need to input table when using TABS buoy'
        fname = path.join('..', 'daily', 'tabs_' + buoy + '_' + table + '_all')
    else:
        fname = path.join('..', 'daily', buoy + '_all')

    # if file already exists, overwrite dstart with day after day from last line of file
    if path.exists(fname):
        dstart = pd.Timestamp(open(fname).readlines()[-1][:10], tz='utc') + pd.Timedelta('1 days')
        mode = 'a'  # overwrite write mode

    # case when difference is short
    if (dend-dstart) < pd.Timedelta('30 days'):
        df = read.read(buoy, dstart, dend, table=table, usemodel=False)
        if df is not None:
            tools.write_file(df, fname, compression=False, mode=mode)
            tools.write_file(df, fname, compression=True, mode=mode)
        else:
            print('No new data has been read in for buoy ' + buoy + ' table ' + table)

    else:  # time difference is long

        # if buoy data is in mysql database, can read in all dates at once
        if bys[buoy]['inmysql']:
            if len(buoy) == 1:
                df = read.read_tabs(table, buoy, dstart, dend)
            else:
                df = read.read_ndbc(buoy, dstart, dend)
        else:
            date = dstart
            df = pd.DataFrame()  # initialize
            while date < dend:
                daystoread = min(pd.Timedelta('30 days'), dend-date)
                dftemp = read.read(buoy, date, date + daystoread, table=table)
                df = df.append(dftemp)
                date += pd.Timedelta('31 days')

        tools.write_file(df, fname, compression=False, mode=mode)
        tools.write_file(df, fname, compression=True, mode=mode)


if __name__ == "__main__":

    tablekeys = ['table1', 'table2', 'table3', 'table4', 'table5']

    # loop through buoys: query, make text file
    for buoy in bys.keys():

        # pulls out the non-nan table values to loop over valid table names
        tables = [bys[buoy][table] for table in tablekeys if not pd.isnull(bys[buoy][table])]

        for table in tables:  # loop through tables for each buoy

            longterm(buoy, table=table, dstart=pd.Timestamp('2017-6-1', tz='utc'))
