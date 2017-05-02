'''
Run script for plot_buoy.py
'''

import plot_buoy
import argparse
import tools


# parse the input arguments
parser = argparse.ArgumentParser()
parser.add_argument('which', type=str, help='which plot function to use ("ven", "met", "eng", "salt", "wave", "ndbc")')
parser.add_argument('dataname', type=str, help='datafile name, found in /tmp')
args = parser.parse_args()
buoy = args.dataname.split('/')[-1][0]

if __name__ == "__main__":

    df = tools.read(args.dataname)
    fig = plot_buoy.plot(df, buoy, args.which)
    fig.savefig(args.dataname + '.pdf')
    fig.savefig(args.dataname + '.png')
