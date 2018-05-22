'''
Update long-term data files.
'''

import tools
import buoy_properties as bp
import pandas as pd
from os import path
import run_daily as rd
import read
import logging

bys = bp.load() # load in buoy data
tablekeys = ['table1', 'table2', 'table3', 'table4', 'table5']


def remake_hdf(buoys=None):
    '''Remake HDF files from text files if messed up.

    Overwrites existing HDF files.
    '''

    if buoys is None:
        buoys = bys.keys()

    # loop through buoys
    for buoy in buoys:

        # pulls out the non-nan table values to loop over valid table names
        tables = [bys[buoy][table] for table in tablekeys if not pd.isnull(bys[buoy][table])]

        for table in tables:  # loop through tables for each buoy
            if len(buoy) == 1:
                assert table is not None, 'need to input table when using TABS buoy'
                fname = path.join('..', 'daily', 'tabs_' + buoy + '_' + table + '_all')
            else:
                fname = path.join('..', 'daily', buoy + '_all')
            # read from text file, write to hdf
            df = pd.read_table(fname, na_values=-999, parse_dates=True, index_col=0)
            tools.write_file(df, fname, filetype='hdf', mode='w', append=False)


def readwrite(buoy, table=None, dstart=pd.Timestamp('1980-1-1', tz='utc')):
    '''Creates or updates buoy data files.

    Reads through yesterday so that when appended to everything is consistent.
    This will take a long time to run if none of the files exist.
    Note that dstart is ignored if buoy data file already exists.
    '''

    # bring data in file up through yesterday. This way files are
    # consistent regardless of what time of day script is run.
    dend = pd.Timestamp('now', tz='UTC').normalize()
    # file write flag
    mode = 'w'
    append = False  # for hdf file

    if len(buoy) == 1:
        assert table is not None, 'need to input table when using TABS buoy'
        fname = path.join('..', 'daily', 'tabs_' + buoy + '_' + table + '_all')
    else:
        fname = path.join('..', 'daily', buoy + '_all')

    # if buoy is inactive and its "all" file exists, don't read
    if buoy in bys.keys() and not bys[buoy]['active'] and path.exists(fname):
        return

    # if file already exists, overwrite dstart with day after day from last line of file
    if path.exists(fname + '.hdf') and path.exists(fname):
        dstart = pd.Timestamp(open(fname).readlines()[-1][:10], tz='utc') + pd.Timedelta('1 days')
        mode = 'a'  # overwrite write mode
        append = True  # overwrite append mode for hdf
    # import pdb; pdb.set_trace()
    df = read.read(buoy, dstart, dend, table=table, units='M', tz='UTC',
                   usemodel=False, userecent=False)

    # can't append to file with empty dataframe
    if df is not None and not (mode == 'a' and df.empty):
        tools.write_file(df, fname, filetype='hdf', mode=mode, append=append)
        tools.write_file(df, fname, filetype='txt', compression=False, mode=mode)
        tools.write_file(df, fname, filetype='txt', compression=True, mode=mode)
    else:
        logging.warning('No new data has been read in for buoy ' + buoy + ' table ' + table)


if __name__ == "__main__":

    logging.basicConfig(filename=path.join('..', 'logs', 'read_all.log'),
                        level=logging.WARNING,
                        format='%(asctime)s %(message)s',
                        datefmt='%a %b %d, %H:%M:%S %Z, %Y')

    # loop through buoys: query, make text file
    for buoy in ['g06010']:# bys.keys():

        # pulls out the non-nan table values to loop over valid table names
        tables = [bys[buoy][table] for table in tablekeys if not pd.isnull(bys[buoy][table])]
        if not 'ports' in tables:
            continue
        for table in tables:  # loop through tables for each buoy
            if 'predict' not in table:  # don't use tables for model predictions
                print(buoy)
                readwrite(buoy, table=table, dstart=pd.Timestamp('1980-1-1', tz='UTC'))
        # for PORTS buoys, also read in full dataset
        if 'ports' in tables:
            print(buoy + 'full')
            readwrite(buoy + '_full', table='ports', dstart=pd.Timestamp('1980-1-1', tz='UTC'))
