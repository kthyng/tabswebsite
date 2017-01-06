'''
Get data into temporary text files.
'''

import run_daily
import tools
import plot_buoy
import argparse
from prettypandas import PrettyPandas
# import os
# from time import time


# parse the input arguments
parser = argparse.ArgumentParser()
parser.add_argument('buoy', type=str, help='buoy name')
parser.add_argument('table', type=str, help='table name e.g. "ven"')
parser.add_argument('fname', type=str, help='file name to save to')
parser.add_argument('dstart', type=str, help='dstart')
parser.add_argument('dend', type=str, help='dend')
parser.add_argument('datatype', type=str, help='pic or data')
args = parser.parse_args()
buoy = args.buoy
table = args.table
fname = args.fname
dstart = args.dstart
dend = args.dend
datatype = args.datatype

# Get the data
engine = run_daily.setup()
query = "SELECT * FROM tabs_" + buoy + '_' + table + " WHERE (date BETWEEN '" + dstart + "' AND '" + dend + "') order by obs_time"
# t1 = time()
df = tools.read(buoy, [query, engine], table)
# t2 = time()
# print('time to read data: ', t2-t1)
run_daily.make_text(df, buoy, table, fname)
# t3 = time()
# print('time to write text file: ', t3-t2)
# fig = plot_buoy.plot(df, buoy, table)
# fig.savefig(os.path.join('daily', 'tabs_' + buoy + '_' + table + '.pdf'))
# fig.savefig(os.path.join('daily', 'tabs_' + buoy + '_' + table + '.png'))
# # save smaller for hover
# if table == 'ven':
#     fig.savefig(os.path.join('daily', 'tabs_' + buoy + '_' + table + '_low.png'), dpi=60)
# close(fig)


print('<br><br>')
# read in data table
if datatype == 'data':
    print(PrettyPandas(df).render())
    # t4 = time()
    # print('time to display text: ', t4-t3)

    # html = df.to_html()
    # print(html)
elif datatype == 'pic':
    # os.system('/anaconda/bin/python run_plot_buoy.py "' + table + '" "' + fname + '"')
    fig = plot_buoy.plot(df, buoy, table)
    fig.savefig(fname + '.pdf')
    fig.savefig(fname + '.png')
    # t4 = time()
    # print('time to save image: ', t4-t3)
