'''
Get data into temporary text files and present it as table or image.
Or, if dstart/dend are not provided, read in previously-created daily file
and present as table or image.

example (since dstart and dend are optional)
run get_data.py 'tmp/tabs_F_ven_test' --dstart '2017-01-5' --dend '2017-01-5' 'data'
run get_data.py 'tmp/tabs_F_ven_test' 'data'
run get_data.py 'tmp/tabs_F_ven_test' 'data' --units 'E'
'''

import run_daily
import tools
import plot_buoy
import argparse
from os import path


# parse the input arguments
parser = argparse.ArgumentParser()
parser.add_argument('fname', type=str, help='file name for either reading in or for saving to')
parser.add_argument('--dstart', type=str, help='dstart', default=None)
parser.add_argument('--dend', type=str, help='dend', default=None)
parser.add_argument('datatype', type=str, help='pic or data')
parser.add_argument('--units', type=str, help='units', default='M')
parser.add_argument('--tz', type=str, help='time zone', default='UTC')
args = parser.parse_args()

fname = args.fname
dstart = args.dstart
dend = args.dend
datatype = args.datatype
units = args.units
tz = args.tz

buoy = fname.split('/')[1].split('_')[1]
table = fname.split('/')[1].split('_')[2]

## Read in data ##
# from daily file
if dstart is None:

    df = tools.read(fname, units=units, tz=tz)

# Call to database if needed
else:
    engine = tools.engine()
    query = "SELECT * FROM tabs_" + buoy + '_' + table + " WHERE (date BETWEEN '" + dstart + "' AND '" + dend + "') order by obs_time"
    df = tools.read([query, engine], units=units, tz=tz)
    run_daily.make_text(df, fname)

if datatype == 'data':
    print('<br><br>')
    tools.present(df)  # print data table to screen
elif datatype == 'pic':
    # does this get called from the front page or otherwise for "recent" data?
    if not path.exists(fname + '.png'):
        print('<br><br>')
        fig = plot_buoy.plot(df, buoy, table)
        fig.savefig(fname + '.pdf')
        fig.savefig(fname + '.png')
