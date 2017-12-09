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
tablekeys = ['table1', 'table2', 'table3', 'table4', 'table5']

def remake_hdf():
    '''Remake HDF files from text files if messed up.

    Overwrites existing HDF files.
    '''

    # loop through buoys
    for buoy in bys.keys():

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
            df.astype(float).tz_localize(None).to_hdf(fname + '.hdf', key='df', mode='w',
                                        format='table', complib='zlib')#, dropna=True)


def readwrite(buoy, table=None, dstart=pd.Timestamp('1980-1-1', tz='utc')):
    '''Creates or updates buoy data files.

    Reads through yesterday so that when appended to everything is consistent.
    This will take a long time to run if none of the files exist.
    Note that dstart is ignored if buoy data file already exists.
    '''

    # bring data in file up through yesterday. This way files are
    # consistent regardless of what time of day script is run.
    dend = pd.Timestamp('now', tz='utc').normalize()
    # file write flag
    mode = 'w'
    append = False  # for hdf file

    if len(buoy) == 1:
        assert table is not None, 'need to input table when using TABS buoy'
        fname = path.join('..', 'daily', 'tabs_' + buoy + '_' + table + '_all')
    else:
        fname = path.join('..', 'daily', buoy + '_all')

    # if file already exists, overwrite dstart with day after day from last line of file
    if path.exists(fname + '.hdf') and path.exists(fname):
        dstart = pd.Timestamp(open(fname).readlines()[-1][:10], tz='utc') + pd.Timedelta('1 days')
        mode = 'a'  # overwrite write mode
        append = True  # overwrite append mode for hdf
    # import pdb; pdb.set_trace()
    df = read.read(buoy, dstart, dend, table=table, units='M', tz='UTC',
                   usemodel=False, userecent=False)

    if df is not None:
        # try:
        tools.write_file(df, fname, filetype='hdf', mode=mode, append=append)
        tools.write_file(df, fname, filetype='txt', compression=False, mode=mode)
        tools.write_file(df, fname, filetype='txt', compression=True, mode=mode)
        # except:
        #     print("Can't write to file for buoy " + buoy)
    else:
        print('No new data has been read in for buoy ' + buoy + ' table ' + table)


if __name__ == "__main__":

    # loop through buoys: query, make text file
    for buoy in bys.keys():

        if buoy != '8770613':
            continue
        # pulls out the non-nan table values to loop over valid table names
        tables = [bys[buoy][table] for table in tablekeys if not pd.isnull(bys[buoy][table])]

        for table in tables:  # loop through tables for each buoy
            # if table != 'eng':
            #     continue
            print(buoy, table)
            readwrite(buoy, table=table, dstart=pd.Timestamp('1980-1-1', tz='utc'))
