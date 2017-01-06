'''
Get data into temporary text files.
'''

import run_daily
import tools
import plot_buoy
import argparse
from prettypandas import PrettyPandas


# parse the input arguments
parser = argparse.ArgumentParser()
# parser.add_argument('buoy', type=str, help='buoy name')
# parser.add_argument('table', type=str, help='table name e.g. "ven"')
parser.add_argument('fname', type=str, help='file name to save to')
parser.add_argument('dstart', type=str, help='dstart')
parser.add_argument('dend', type=str, help='dend')
parser.add_argument('datatype', type=str, help='pic or data')
args = parser.parse_args()
# buoy = args.buoy
# table = args.table
fname = args.fname
dstart = args.dstart
dend = args.dend
datatype = args.datatype

buoy = fname.split('/')[1][5:6]
table = fname.split('/')[1][7:10]

# Get the data
engine = run_daily.setup()
query = "SELECT * FROM tabs_" + buoy + '_' + table + " WHERE (date BETWEEN '" + dstart + "' AND '" + dend + "') order by obs_time"
df = tools.read(buoy, [query, engine], table)
run_daily.make_text(df, buoy, table, fname)

print('<br><br>')
if datatype == 'data':
    print(PrettyPandas(df).render())

elif datatype == 'pic':
    fig = plot_buoy.plot(df, buoy, table)
    fig.savefig(fname + '.pdf')
    fig.savefig(fname + '.png')
