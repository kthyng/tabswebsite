'''
Get data into temporary text files and present it as table or image.
Or, if dstart/dend are not provided, read in previously-created daily file
and present as table or image.

example (since dstart and dend are optional)
run get_data.py '../tmp/tabs_F_ven_test' --dstart '2017-01-5' --dend '2017-01-5 00:00' 'data' --usemodel 'True'
run get_data.py '../tmp/tabs_F_ven_test' 'data'
run get_data.py '../tmp/ndbc_PTAT2_test' 'pic'
run get_data.py '../tmp/tabs_F_ven_test' 'data' --units 'E'
run get_data.py '../tmp/8770475' --dstart '2018-5-7' --dend '2018-5-12 00:00' 'pic' --usemodel 'False' --datum 'MLLW'
'''

import run_daily
import tools
import plot_buoy
import argparse
from os import path
import pandas as pd
from matplotlib.dates import date2num
import read
import buoy_properties as bp

bys = bp.load() # load in buoy properties

# parse the input arguments
parser = argparse.ArgumentParser()
parser.add_argument('fname', type=str, help='file name for either reading in or for saving to')
parser.add_argument('--dstart', type=str, help='dstart', default=None)
parser.add_argument('--dend', type=str, help='dend', default=None)
parser.add_argument('datatype', type=str, help='pic or data')
parser.add_argument('--units', type=str, help='units', default='M')
parser.add_argument('--tzname', type=str, help='time zone: "UTC" or "local" or "CST"', default='UTC')
parser.add_argument('--usemodel', type=str, help='plot model output', default='True')
parser.add_argument('--datum', type=str, help='Which tidal datum to use: "MHHW", "MHW", "MTL", "MSL", "MLW", "MLLW"', default='MSL')
args = parser.parse_args()

fname = args.fname
datatype = args.datatype
units = args.units
tzname = args.tzname
usemodel = args.usemodel
dstart = args.dstart
dend = args.dend
datum = args.datum

if tzname.lower() in ['utc', 'gmt']:
    tz = 'UTC'
# CST or CDT as appropriate
elif tzname.lower() in ['local', 'cst/cdt', 'us/central']:
    tz = 'US/Central'
# CST only -- no transition for CDT
elif tzname.lower() in ['cst']:
    tz = 'Etc/GMT+6'

# can't figure out how to have variable from php a boolean so sending string
if usemodel == 'False':
    usemodel = False
elif usemodel == 'True':
    usemodel = True

# change dstart and dend to datetime objects
if dstart is not None:
    dstart = pd.Timestamp(dstart, tz=tz)
    dend = pd.Timestamp(dend, tz=tz)
now = pd.Timestamp('now', tz=tz)

if dend is not None:
    # add a day to dend time so that desired day is included
    dend += pd.Timedelta('1 day')

if 'tabs_' in fname:  # only need table name for tabs
    table = fname.split('/')[-1].split('_')[2]
    buoy = fname.split('/')[-1].split('_')[1]
else:
    buoy = fname.split('/')[-1].split('_')[0]
    table = bys[buoy]['table1']

## Read in data ##
# from daily file, only for showing table since images created in run_daily.py
if dstart is None:

    df = read.read(fname, dstart=None, dend=None, table=table, units=units, tz=tz, datum=datum)
    dfmodelhindcast = None
    dfmodelrecent = None
    dfmodelforecast = None

# Call to database if needed
else:
    ## Read data ##
    df = read.read(buoy, dstart, dend, table=table, units=units, tz=tz, datum=datum)
    if df is not None:  # won't work if data isn't available in this time period
        tools.write_file(df, fname)

    ## Read model ##
    # tables = ['ven', 'met', 'salt', 'tcoon', 'tcoon-nomet', 'ndbc',
            #   'ndbc-nowave-nowtemp', 'ndbc-nowave-nowtemp-nopress', 'ndbc-nowave']
    # To use NOAA-provided model predictions
    if usemodel and bys[buoy]['table1'] == 'ports':
        dfmodelhindcast = None
        dfmodelrecent = None
        dfmodelforecast = None
        dfmodeltides = read.read(buoy, dstart, dend, usemodel=True,
                                    userecent=True, tz=tz, units=units)

    # using model but not ports buoy
    elif usemodel: # and bys[buoy]['table1'] in tables:
        dfmodelhindcast = read.read(buoy, dstart, dend, table=table,
                                          usemodel='hindcast', tz=tz, units=units)
        # only look for nowcast model output if hindcast doesn't cover it
        # sometimes the two times overlap but hindcast output is better
        if dfmodelhindcast is not None and (dfmodelhindcast.index[-1] - dend) < pd.Timedelta('1 hour'):
            dfmodelrecent = None
        else:
            dfmodelrecent = read.read(buoy, dstart, dend, table=table,
                                            usemodel='recent', tz=tz, units=units)
        dfmodelforecast = read.read(buoy, dstart, dend, table=table,
                                          usemodel='forecast', tz=tz, units=units)
        if bys[buoy]['table2'] == 'tidepredict':
            # import pdb; pdb.set_trace()
            dfmodeltides = read.read(buoy, dstart, dend, usemodel=True,
                                     userecent=True, tz=tz, units=units, datum=datum)
        else:
            dfmodeltides = None

    else:
        dfmodelhindcast = None
        dfmodelrecent = None
        dfmodelforecast = None
        dfmodeltides = None


if datatype == 'data':
    # print('<br><br>')
    tools.present(df)  # print data table to screen
elif datatype == 'pic':
    # does this get called from the front page or otherwise for "recent" data?
    # if not path.exists(fname + '.png'):
    print('<br><br>')
    if dend is not None:
        tlims = [date2num(pd.to_datetime(dstart.tz_localize(None)).to_pydatetime()), date2num(pd.to_datetime(dend.tz_localize(None)).to_pydatetime())]
    else:
        tlims = None
    if any([dft is not None for dft in [df, dfmodelhindcast, dfmodelrecent, dfmodelforecast,dfmodeltides]]):
        fig = plot_buoy.plot(df, buoy, which=table, df1=dfmodelhindcast,
                             df2=dfmodelrecent, df3=dfmodelforecast,
                             df4=dfmodeltides, tlims=tlims)
        fig.savefig(fname + '.pdf')
        fig.savefig(fname + '.png')
