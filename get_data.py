'''
Get data into temporary text files and present it as table or image.
Or, if dstart/dend are not provided, read in previously-created daily file
and present as table or image.

example (since dstart and dend are optional)
run get_data.py 'tmp/tabs_F_ven_test' --dstart '2017-01-5' --dend '2017-01-5' 'data'
run get_data.py 'tmp/tabs_F_ven_test' 'data'
'''

import run_daily
import tools
import plot_buoy
import argparse


# parse the input arguments
parser = argparse.ArgumentParser()
parser.add_argument('fname', type=str, help='file name to save to')
parser.add_argument('--dstart', type=str, help='dstart', default=None)
parser.add_argument('--dend', type=str, help='dend', default=None)
parser.add_argument('datatype', type=str, help='pic or data')
args = parser.parse_args()

fname = args.fname
dstart = args.dstart
dend = args.dend
datatype = args.datatype

buoy = fname.split('/')[1][5:6]
table = fname.split('/')[1][7:10]

## Read in data ##
# from daily file
if dstart is None:

    df = tools.read(buoy, fname, table)

# Call to database if needed
else:
    engine = run_daily.setup()
    query = "SELECT * FROM tabs_" + buoy + '_' + table + " WHERE (date BETWEEN '" + dstart + "' AND '" + dend + "') order by obs_time"
    df = tools.read(buoy, [query, engine], table)
    run_daily.make_text(df, buoy, table, fname)

print('<br><br>')
if datatype == 'data':
    tools.present(df)  # print data table to screen
elif datatype == 'pic':
    fig = plot_buoy.plot(df, buoy, table)
    fig.savefig(fname + '.pdf')
    fig.savefig(fname + '.png')
