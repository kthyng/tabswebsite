'''
Get data into temporary text files and present it as table or image.
Or, if dstart/dend are not provided, read in previously-created daily file
and present as table or image.

example (since dstart and dend are optional)
run get_data.py '../tmp/tabs_F_ven_test' --dstart '2017-01-5' --dend '2017-01-5 00:00' 'data' --model True
run get_data.py '../tmp/tabs_F_ven_test' 'data'
run get_data.py '../tmp/ndbc_PTAT2_test' 'pic'
run get_data.py '../tmp/tabs_F_ven_test' 'data' --units 'E'
run get_data.py '../tmp/tcoon_8770475' --dstart '2017-01-5' --dend '2017-01-5 00:00' 'pic' --model False
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
now = pd.Timestamp('now', tz='utc')

# parse the input arguments
parser = argparse.ArgumentParser()
parser.add_argument('fname', type=str, help='file name for either reading in or for saving to')
parser.add_argument('--dstart', type=str, help='dstart', default=None)
parser.add_argument('--dend', type=str, help='dend', default=None)
parser.add_argument('datatype', type=str, help='pic or data')
parser.add_argument('--units', type=str, help='units', default='M')
parser.add_argument('--tz', type=str, help='time zone', default='UTC')
parser.add_argument('--model', type=str, help='plot model output', default='False')
args = parser.parse_args()

fname = args.fname
# change dstart and dend to datetime objects
dstart = pd.Timestamp(args.dstart, tz='utc')
dend = pd.Timestamp(args.dend, tz='utc')

if dend is not None:
    # make it so dend time is at end of the day
    dend += pd.Timedelta('23 hours')
datatype = args.datatype
units = args.units
tz = args.tz
model = args.model
# can't figure out how to have variable from php a boolean so sending string
if model == 'False':
    usemodel = False
elif model == 'True':
    usemodel = True

if 'tabs_' in fname:  # only need table name for tabs
    table = fname.split('/')[-1].split('_')[2]
    buoy = fname.split('/')[-1].split('_')[1]
else:
    table = None
    buoy = fname.split('/')[-1].split('_')[0]

## Read in data ##
# from daily file
if dstart is None:

    df = tools.read(fname, units=units, tz=tz)
    dfmodelhindcast = None
    dfmodelrecent = None
    dfmodelforecast = None

# Call to database if needed
else:
    ## Read data ##
    df = read.read(buoy, dstart, dend, table=table, units=None, tz=None)
    if df is not None:  # won't work if data isn't available in this time period
        tools.write_file(df, fname)

    ## Read model ##
    tables = ['ven', 'met', 'salt', 'tcoon', 'tcoon-nomet', 'ndbc',
              'ndbc-nowave-nowtemp', 'ndbc-nowave-nowtemp-nopress', 'ndbc-nowave']
    if usemodel and bys[buoy]['table1'] in tables:
        dfmodelhindcast = read.read_model(buoy, table, dstart, dend, timing='hindcast')
        dfmodelrecent = read.read_model(buoy, table, dstart, dend, timing='recent')
        dfmodelforecast = read.read_model(buoy, table, dstart, dend, timing='forecast')
    elif usemodel and bys[buoy]['table1'] == 'ports':
        dfmodelhindcast = None
        dftemp = read.read(buoy, dstart, dend, usemodel=True)
        dfmodelrecent = dftemp[:now] if dstart<now else None
        dfmodelforecast = dftemp[now:] if dend>now else None
    else:
        dfmodelhindcast = None
        dfmodelrecent = None
        dfmodelforecast = None



if datatype == 'data':
    # print('<br><br>')
    tools.present(df)  # print data table to screen
elif datatype == 'pic':
    # does this get called from the front page or otherwise for "recent" data?
    if not path.exists(fname + '.png'):
        print('<br><br>')
        if dend is not None:
            tlims = [date2num(pd.to_datetime(dstart).to_pydatetime()), date2num(pd.to_datetime(dend).to_pydatetime())]
        else:
            tlims = None
        fig = plot_buoy.plot(df, buoy, which=table, df1=dfmodelhindcast,
                             df2=dfmodelrecent, df3=dfmodelforecast, tlims=tlims)
        fig.savefig(fname + '.pdf')
        fig.savefig(fname + '.png')
