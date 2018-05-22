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
import numpy as np

bys = bp.load() # load in buoy data
tablekeys = ['table1', 'table2', 'table3', 'table4', 'table5']


def remake_file(buoys=None, tables=None, remaketype='hdf', remakefrom='txt'):
    '''Remake file from another file if messed up.

    Overwrites existing remaketype files.

    buoys (list): buoys to remake
    tables (list): tables to remake (just for TABS buoys). If buoys is None,
     tables will be read in for each buoy to cover all options.
    remaketype (str), default 'hdf': which type of file to remake
    remakefrom (str), default 'txt': which type of existing file to use to
     remake other file from.
    Options for both are 'hdf' and 'txt'.
    '''

    if buoys is None:
        buoys = bys.keys()

    # loop through buoys
    for buoy in buoys:

        # pulls out the non-nan table values to loop over valid table names
        if len(buoy) == 1 and tables is None:
            tables = [bys[buoy][table] for table in tablekeys if not pd.isnull(bys[buoy][table])]
        elif tables is None:
            tables = ['unused']

        for table in tables:  # loop through tables for each buoy
            if len(buoy) == 1:
                assert table is not None, 'need to input table when using TABS buoy'
                fname = path.join('..', 'daily', 'tabs_' + buoy + '_' + table + '_all')
            else:
                fname = path.join('..', 'daily', buoy + '_all')

            # read from remakefrom file, write to remaketype file
            df = tools.read(fname, remakefrom)
            tools.write_file(df, fname, filetype=remaketype, mode='w', append=False)


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

    # two types of files
    Types = ['txt', 'hdf']

    # if any of the files exist, then we want to make sure they are consistent
    if np.asarray([path.exists(fname + '.' + Type) for Type in Types]).any():
        lastrows = []
        for Type in Types:
            # get last row in file
            try:
                lastrows.append(tools.read(fname, Type, lastlineonly=True))
            # if can't get last row, remake file
            except:
                logging.warning('Could not access existing file %s of type %s. Will remake.' % (fname, Type))
                # try other type of files to remake this file if needed
                othertype = [temp for temp in Types if temp != Type]
                try:
                    remake_file(buoys=[buoy], tables=[table], remaketype=Type, remakefrom=othertype[0])
                    logging.warning('Remade file of type %s from type %s for buoy %s' % (Type, othertype[0], buoy))
                except:
                    logging.warning('Could not remake file for buoy %s' % (buoy))
                # now the file should exist, so can read in lastrow
                lastrows.append(tools.read(fname, Type, lastlineonly=True))


        # if last rows are not the same, remake shorter file
        if not lastrows[0] == lastrows[1]:
            lastrow = lastrows[0]; lastrow2 = lastrows[1]
            Type = Types[0]; Type2 = Types[1]
            if lastrow < lastrow2:
                remake_file(buoys=[buoy], remaketype=Type, remakefrom=Type2)
                logging.warning('File type %s for buoy %s was short and remade with file type %s.' % (Type, buoy, Type2))
            elif lastrow2 < lastrow:
                remake_file(buoys=[buoy], remaketype=Type2, remakefrom=Type)
                logging.warning('File type %s for buoy %s was short and remade with file type %s.' % (Type2, buoy, Type))

    # now files should be consistent at this point if they already exist
    # if file already exists, overwrite dstart with day after day from last line of file
    if path.exists(fname + '.hdf'):
        dstart = tools.read(fname, Type, lastlineonly=True).normalize().tz_localize('UTC') + pd.Timedelta('1 days')
        mode = 'a'  # overwrite write mode
        append = True  # overwrite append mode for hdf
    df = read.read(buoy, dstart, dend, table=table, units='M', tz='UTC',
                   usemodel=False, userecent=False)

    # can't append to file with empty dataframe
    if df is not None and not (mode == 'a' and df.empty):
        for Type in Types:
            try:
                tools.write_file(df, fname, filetype=Type, mode=mode, append=append)
            except:
                logging.warning('Could not write to file %s of type %s. Will remake.' % (fname, Type))
                # try both other types of files to remake this file if needed
                othertype = [temp for temp in Types if temp != Type]
                try:
                    remake_file(buoys=[buoy], tables=[table], remaketype=Type, remakefrom=othertype[0])
                    logging.warning('Remade file of type %s from type %s for buoy %s' % (Type, othertype[0], buoy))
                except:
                    logging.warning('Could not remake file for buoy %s' % (buoy))
    else:
        logging.warning('No new data has been read in for buoy ' + buoy + ' table ' + table)


if __name__ == "__main__":

    logging.basicConfig(filename=path.join('..', 'logs', 'read_all.log'),
                        level=logging.WARNING,
                        format='%(asctime)s %(message)s',
                        datefmt='%a %b %d, %H:%M:%S %Z, %Y')

    # loop through buoys: query, make text file
    for buoy in bys.keys():

        # pulls out the non-nan table values to loop over valid table names
        tables = [bys[buoy][table] for table in tablekeys if not pd.isnull(bys[buoy][table])]

        for table in tables:  # loop through tables for each buoy
            if 'predict' not in table:  # don't use tables for model predictions
                readwrite(buoy, table=table, dstart=pd.Timestamp('1980-1-1', tz='UTC'))
        # for PORTS buoys, also read in full dataset
        if 'ports' in tables:
            readwrite(buoy + '_full', table='ports', dstart=pd.Timestamp('1980-1-1', tz='UTC'))
