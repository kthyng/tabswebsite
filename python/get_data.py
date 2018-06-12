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
run get_data.py '../tmp/tabs_B_ven' --dstart '2018-6-1' --dend '2018-6-5 00:00' 'download' --usemodel 'True' --modelonly 'True' --s_rho '-999'
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
import logging

logging.basicConfig(filename=path.join('..', 'logs', 'get_data.log'),
                    level=logging.WARNING,
                    format='%(asctime)s %(message)s',
                    datefmt='%a %b %d %H:%M:%S %Z %Y')

bys = bp.load() # load in buoy properties

# parse the input arguments
parser = argparse.ArgumentParser()
parser.add_argument('fname', type=str, help='file name for either reading in or for saving to')
parser.add_argument('--dstart', type=str, help='dstart', default=None)
parser.add_argument('--dend', type=str, help='dend', default=None)
parser.add_argument('datatype', type=str, help='pic or data or download')
parser.add_argument('--units', type=str, help='units', default='M')
parser.add_argument('--tzname', type=str, help='time zone: "UTC" or "local" or "CST"', default='UTC')
parser.add_argument('--usemodel', type=str, help='plot model output', default='True')
parser.add_argument('--datum', type=str, help='Which tidal datum to use: "MHHW", "MHW", "MTL", "MSL", "MLW", "MLLW"', default='MSL')
parser.add_argument('--modelonly', type=str, help='Bonus option to be able to download model output. Excludes data.', default='False')
parser.add_argument('--s_rho', type=str,
                    help='Vertical layer for model output. Default gives surface of "-1". Input "-999" for full water column. There are 30 vertical layers to index.', default='-1')
args = parser.parse_args()

fname = args.fname
datatype = args.datatype
units = args.units
tzname = args.tzname
usemodel = args.usemodel
dstart = args.dstart
dend = args.dend
datum = args.datum
modelonly = args.modelonly
s_rho = args.s_rho

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

if modelonly == 'False':
    modelonly = False
elif modelonly == 'True':
    modelonly = True


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

# force the use of metric units if making a plot since both units shown anyway
if datatype == 'pic':
    units = 'M'

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
    if not modelonly:
        df = read.read(buoy, dstart, dend, table=table, units=units, tz=tz, datum=datum)
        if df is not None:  # won't work if data isn't available in this time period
            tools.write_file(df, fname)

    ## Read model ##
    # To use NOAA-provided model predictions
    if usemodel and bys[buoy]['table1'] == 'ports' and buoy != 'cc0101':
        dfmodelhindcast = None
        dfmodelrecent = None
        dfmodelforecast = None
        dfmodeltides = read.read(buoy, dstart, dend, usemodel=True,
                                    userecent=True, tz=tz, units=units)

    # using model but not ports buoy
    elif usemodel: # and bys[buoy]['table1'] in tables:
        dfmodelhindcast = read.read(buoy, dstart, dend, table=table,
                                          usemodel='hindcast', tz=tz, units=units, s_rho=int(s_rho))
        # only look for nowcast model output if hindcast doesn't cover it
        # sometimes the two times overlap but hindcast output is better
        if dfmodelhindcast is not None and (dfmodelhindcast.index[-1] - dend) < pd.Timedelta('1 hour'):
            dfmodelrecent = None
        else:
            dfmodelrecent = read.read(buoy, dstart, dend, table=table,
                                            usemodel='recent', tz=tz, units=units, s_rho=int(s_rho))
        dfmodelforecast = read.read(buoy, dstart, dend, table=table,
                                          usemodel='forecast', tz=tz, units=units, s_rho=int(s_rho))
        if bys[buoy]['table2'] == 'tidepredict':
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
elif datatype == 'download' and modelonly:
    # combine txla model output together
    dfs = [dfmodelhindcast, dfmodelrecent, dfmodelforecast]
    try:
        df = pd.concat([df for df in dfs if not None], axis=0, sort=False)
        # only remove duplicates if not multiple depths per time
        if df['Depth [m]'][0] == df['Depth [m]'][1]:
            df = df[~df.index.duplicated(keep='first')]  # remove any duplicated indices
        # add in NOAA model output
        try:
            df = df.join(dfmodeltides, how='outer')
        except:
            pass
    except:
        df = dfmodeltides
    if df is not None:
        tools.write_file(df, fname)
