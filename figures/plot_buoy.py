'''
Make plot of recent buoy data.

python plot_buoy.py -h for help
python plot_buoy.py 'ven' 'tempfile' 'tempout'
'''

import matplotlib.pyplot as plt
import pandas as pd
import matplotlib as mpl
import netCDF4 as netCDF
import numpy as np
import time
from datetime import datetime
import argparse

mpl.rcParams.update({'font.size': 14})
mpl.rcParams['font.sans-serif'] = 'Arev Sans, Bitstream Vera Sans, Lucida Grande, Verdana, Geneva, Lucid, Helvetica, Avant Garde, sans-serif'
mpl.rcParams['mathtext.fontset'] = 'custom'
mpl.rcParams['mathtext.cal'] = 'cursive'
mpl.rcParams['mathtext.rm'] = 'sans'
mpl.rcParams['mathtext.tt'] = 'monospace'
mpl.rcParams['mathtext.it'] = 'sans:italic'
mpl.rcParams['mathtext.bf'] = 'sans:bold'
mpl.rcParams['mathtext.sf'] = 'sans'
mpl.rcParams['mathtext.fallback_to_cm'] = 'True'

# degree True for across-shelf rotation angle (rotated x axis is offshore)
angle = {'B': 145, 'K': 90, 'D': 140, 'F': 155, 'J': 90, 'N': 155, 'R': 145,
         'V': 173, 'W': 173, 'X': 90}

# locations for buoys
locs = {'B': {'lon': '94 53.943W', 'lat': '28 58.938N'}, 'K': {'lon': '96 29.988W', 'lat': '26 13.008N'},
        'D': {'lon': '96 50.574W', 'lat': '27 56.376N'}, 'F': {'lon': '94 14.496W', 'lat': '28 50.550N'},
        'J': {'lon': '97 03.042W', 'lat': '26 11.484N'}, 'N': {'lon': '94 02.202W', 'lat': '27 53.418N'},
        'R': {'lon': '93 38.502W', 'lat': '29 38.100N'}, 'V': {'lon': '93 35.838W', 'lat': '27 53.796N'},
        'W': {'lon': '96 00.348W', 'lat': '28 21.042N'}, 'X': {'lon': '96 20.298W', 'lat': '27 03.960N'}}

# parse the input arguments
parser = argparse.ArgumentParser()
parser.add_argument('which', type=str, help='which plot function to use ("ven", "met", "eng", "salt")')
parser.add_argument('dataname', type=str, help='datafile name, found in /tmp')
args = parser.parse_args()

buoy = args.dataname.split('/')[-1][0]


def ven(dataname):
    '''Plot ven data.

    Find data in dataname and save fig, both in /tmp.
    '''

    ## Load in data already saved into /tmp file by tabsquery.php ##
    # time in UTC, velocities in cm/s, direction in deg T, temp in deg C
    names = ['Date', 'Time', 'East', 'North', 'Speed', 'Dir', 'WaterT']
    df = pd.read_table(dataname, parse_dates=[[0,1]], delim_whitespace=True, names=names, index_col=0)
    # Calculate along- and across-shelf
    # along-shelf rotation angle in math angle convention
    theta = np.deg2rad(-(angle[buoy]-90))  # convert from compass to math angle
    df['Across'] = df['East']*np.cos(-theta) - df['North']*np.sin(-theta)
    df['Along'] = df['East']*np.sin(-theta) + df['North']*np.cos(-theta)

    # max current value
    cmax = 60  # cm/s
    kmax = cmax/51.4444444444  # knots
    lw = 1.5

    # plot
    fig, axes = plt.subplots(4, 1, figsize=(8.5,11), sharex=True)
    # bottom controlled later
    fig.subplots_adjust(top=0.96, right=0.90, left=0.22, hspace=0.1)
    # fig.suptitle('TGLO TABS Buoy B: ' + locs['B'][0] + ', ' + locs['B'][1], fontsize=18)

    # current arrows
    ax = axes[0]
    # can't use datetime index directly unfortunately here, so can't use pandas later either
    idx = mpl.dates.date2num(df.index.to_pydatetime())

    # arrows with no heads for lines
    # http://stackoverflow.com/questions/37154071/python-quiver-plot-without-head
    ax.quiver(idx, np.zeros(df.index.size), df.East, df.North,
              headaxislength=0, headlength=0, width=0.1,
              units='y', scale_units='y', scale=1)
    ax.set_ylim(-cmax, cmax)
    ax.set_ylabel('Currents\n' + r'$\left[ \mathrm{cm} \cdot \mathrm{s}^{-1} \right]$')
    ax.set_title('TGLO TABS Buoy ' + buoy + ': ' + locs[buoy]['lat'] + ', ' + locs[buoy]['lon'], fontsize=18)

    # compass arrow
    ax.annotate("", xy=(0.97, 0.95), xytext=(0.97, 0.83),
            arrowprops=dict(arrowstyle="->"), xycoords='axes fraction')
    ax.text(0.97, 0.77, 'N', transform=ax.transAxes,
            horizontalalignment='center', fontsize=10)
    # convert to knots
    axknots = ax.twinx()
    axknots.set_ylim(-kmax, kmax)
    axknots.set_ylabel(r'[knots]')

    ## cross-shelf flow ##
    ax = axes[1]
    ax.plot(idx, df.Across, 'k', lw=lw)
    ax.plot(idx, np.zeros(idx.size), 'k:')
    # ax.set_ylim(-cmax-15, cmax+15)
    ylim = ax.get_ylim()
    ax.set_ylim(ylim[0]*0.9, ylim[1]*1.1)
    ax.set_ylabel('Cross-shelf flow\n' + r'$\left[ \mathrm{cm} \cdot \mathrm{s}^{-1} \right]$')
    # convert to knots
    axknots = ax.twinx()
    axknots.set_ylim(-kmax, kmax)
    axknots.set_ylabel('[knots]')
    ax.text(0.02, 0.91, 'OFFSHORE', fontsize=10, transform=ax.transAxes)
    ax.text(0.02, 0.04, 'ONSHORE', fontsize=10, transform=ax.transAxes)
    ax.text(0.9, 0.9, str(angle[buoy]) + '$^\circ$T', fontsize=11, transform=ax.transAxes)
    ####

    # along-shelf flow
    ax = axes[2]
    ax.plot(idx, df.Along, 'k', lw=lw)
    ax.plot(idx, np.zeros(idx.size), 'k:')
    ax.set_ylim(-cmax-15, cmax+15)
    ax.set_ylabel('Along-shelf flow\n' + r'$\left[ \mathrm{cm} \cdot \mathrm{s}^{-1} \right]$')
    # ax.grid(which='major', color='k', linestyle='-', linewidth=0.05, alpha=0.5)
    # convert to knots
    axknots = ax.twinx()
    ylim = ax.get_ylim()
    axknots.set_ylim(ylim[0], ylim[1])
    axknots.set_ylabel('[knots]')
    ax.text(0.02, 0.91, 'UPCOAST', fontsize=10, transform=ax.transAxes)
    ax.text(0.02, 0.04, 'DOWNCOAST', fontsize=10, transform=ax.transAxes)
    ax.text(0.9, 0.9, str(angle[buoy]-90) + '$^\circ$T', fontsize=11, transform=ax.transAxes)

    # T/S
    cmicro = '0.6'
    cDCS = '0.0'
    ax = axes[3]
    ax.plot(idx, df.WaterT, lw=lw, color=cDCS, linestyle='-')
    ax.set_ylabel(r'Temperature $\left[^\circ\mathrm{C}\right]$')
    # set bottom ylim a little large to make room for text
    ylim = ax.get_ylim()
    ax.set_ylim(ylim[0]*0.98, ylim[1])
    # Fahrenheit
    axF = ax.twinx()
    axF.spines["left"].set_position(("axes", -0.16))
    # make spine visible
    # http://matplotlib.org/examples/pylab_examples/multiple_yaxis_with_spines.html
    def make_patch_spines_invisible(ax):
        ax.set_frame_on(True)
        ax.patch.set_visible(False)
        for sp in ax.spines.values():
            sp.set_visible(False)
    make_patch_spines_invisible(axF)
    # put spine on left, and shift farther to the left too
    # http://stackoverflow.com/questions/20146652/two-y-axis-on-the-left-side-of-the-figure
    axF.spines["left"].set_visible(True)
    axF.yaxis.set_label_position('left')
    axF.yaxis.set_ticks_position('left')
    axF.set_ylabel(r'$\left[^\circ\mathrm{F}\right]$')
    ylim = ax.get_ylim()
    # convert to fahrenheit
    axF.set_ylim(ylim[0]*(9/5.)+32, ylim[1]*(9/5.)+32)

    # # hourly minor ticks
    # hours = mpl.dates.HourLocator()
    # ax.xaxis.set_minor_locator(hours)
    # halfdays = mpl.dates.HourLocator(byhour=[0,12])
    # ax.xaxis.set_major_locator(halfdays)
    ax.xaxis.set_major_formatter(mpl.dates.DateFormatter('%b %d, %H:%M'))

    # Year for first entry
    ax.text(0.98, -0.25, datetime.strftime(df.index[0], '%Y'),
            transform=ax.transAxes, rotation=30)


    # rotates and right aligns the x labels, and moves the bottom of the
    # axes up to make room for them
    fig.autofmt_xdate(bottom=0.125)

    # text at bottom
    # right hand side
    text = 'Oceanography and GERG at Texas A&M University\n' \
           + time.strftime('%a %b %d, %Y %H:%M GMT%z')
    fig.text(0.95, 0.035, text, fontsize=8, transform=fig.transFigure,
             horizontalalignment='right', verticalalignment='top')
    # left hand side
    text = 'TGLO, GERG, Oceanography, and Texas A&M make no representations\n' \
           + 'or any other warranty with regard to this data.\n' \
           + 'These data are not suitable for navigation purposes.'
    fig.text(0.08, 0.035, text, fontsize=8, transform=fig.transFigure,
             horizontalalignment='left', verticalalignment='top')

    fig.savefig(dataname + '.pdf')
    fig.savefig(dataname + '.png')



def plot_buoy(loc):
    '''Make plot of most relevant buoy data.'''


    ## Load in data, from txt page or php ##
    # velocity
    # loc = 'http://tabs.gerg.tamu.edu/tglo/DailyData/Data/tabs_B_ven.txt'
    # time in UTC, velocities in cm/s, direction in deg T, temp in deg C
    names = ['Date', 'Time', 'East', 'North', 'Speed', 'Dir', 'WaterT']
    df = pd.read_table(loc, parse_dates=[[0,1]], delim_whitespace=True, names=names, index_col=0)
    # Calculate along- and across-shelf
    # along-shelf rotation angle in math angle convention
    theta = np.deg2rad(-(angle['B']-90))  # convert from compass to math angle
    # # rotation matrix
    # rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    # vec = np.array([[df['East']], [df['North']]])
    # output = np.dot(rot, vec)
    # # define these from the output array
    # df['Across'] = output[0,0]
    # df['Along'] = output[1,0]
    # why do I need a negative sign for theta?
    df['Across'] = df['East']*np.cos(-theta) - df['North']*np.sin(-theta)
    df['Along'] = df['East']*np.sin(-theta) + df['North']*np.cos(-theta)
    # df['Along'] = df['East']*np.cos(theta) - df['North']*np.sin(theta)
    # df['Across'] = -df['East']*np.sin(theta) - df['North']*np.cos(theta)
    # df['Along'] = df['Speed']*np.cos(np.deg2rad(theta))
    # # the across dimension seems to be inverse of what I'd expect, so need negative sign
    # df['Across'] = -df['Speed']*np.sin(np.deg2rad(theta))

    # salinity
    loc = 'http://tabs.gerg.tamu.edu/tglo/DailyData/Data/tabs_B_salt.txt'
    # time in UTC, temp in deg C, Cond in ms/cm, density in kg/m^3, soundvel in m/s
    names = ['Date', 'Time', 'Temp', 'Cond', 'Salinity', 'Density', 'SoundVel']
    dfsalt = pd.read_table(loc, parse_dates=[[0,1]], delim_whitespace=True, names=names, index_col=0)

    # max current value
    cmax = 60  # cm/s
    kmax = cmax/51.4444444444  # knots
    lw = 1.5


    # plot
    fig, axes = plt.subplots(4, 1, figsize=(8.5,11), sharex=True)
    # bottom controlled later
    fig.subplots_adjust(top=0.96, right=0.90, left=0.22, hspace=0.1)
    # fig.suptitle('TGLO TABS Buoy B: ' + locs['B'][0] + ', ' + locs['B'][1], fontsize=18)

    # current arrows
    ax = axes[0]
    # can't use datetime index directly unfortunately here, so can't use pandas later either
    idx = mpl.dates.date2num(df.index.to_pydatetime())

    # arrows with no heads for lines
    # http://stackoverflow.com/questions/37154071/python-quiver-plot-without-head
    ax.quiver(idx, np.zeros(df.index.size), df.East, df.North,
              headaxislength=0, headlength=0, width=0.001)
    ax.set_ylim(-cmax, cmax)
    ax.set_ylabel('Currents\n' + r'$\left[ \mathrm{cm} \cdot \mathrm{s}^{-1} \right]$')
    ax.set_title('TGLO TABS Buoy B: ' + locs['B'][0] + ', ' + locs['B'][1], fontsize=18)

    # compass arrow
    ax.annotate("", xy=(0.97, 0.95), xytext=(0.97, 0.83),
            arrowprops=dict(arrowstyle="->"), xycoords='axes fraction')
    ax.text(0.97, 0.77, 'N', transform=ax.transAxes,
            horizontalalignment='center', fontsize=10)
    # convert to knots
    axknots = ax.twinx()
    axknots.set_ylim(-kmax, kmax)
    axknots.set_ylabel(r'[knots]')

    ## cross-shelf wind ##
    ax = axes[1]
    idx = mpl.dates.date2num(df.index.to_pydatetime())
    ax.plot(idx, df.Across, 'k', lw=lw)
    ax.plot(idx, np.zeros(idx.size), 'k:')
    ax.set_ylim(-cmax-15, cmax+15)
    ax.set_ylabel('Cross-shelf flow\n' + r'$\left[ \mathrm{cm} \cdot \mathrm{s}^{-1} \right]$')
    # convert to knots
    axknots = ax.twinx()
    axknots.set_ylim(-kmax, kmax)
    axknots.set_ylabel('[knots]')
    ax.text(0.02, 0.91, 'OFFSHORE', fontsize=10, transform=ax.transAxes)
    ax.text(0.02, 0.04, 'ONSHORE', fontsize=10, transform=ax.transAxes)
    ax.text(0.9, 0.9, str(angle['B']) + '$^\circ$T', fontsize=11, transform=ax.transAxes)
    ####

    # along-shelf wind
    ax = axes[2]
    ax.plot(idx, df.Along, 'k', lw=lw)
    ax.plot(idx, np.zeros(idx.size), 'k:')
    ax.set_ylim(-cmax-15, cmax+15)
    ax.set_ylabel('Along-shelf flow\n' + r'$\left[ \mathrm{cm} \cdot \mathrm{s}^{-1} \right]$')
    # ax.grid(which='major', color='k', linestyle='-', linewidth=0.05, alpha=0.5)
    # convert to knots
    axknots = ax.twinx()
    axknots.set_ylim(-kmax, kmax)
    axknots.set_ylabel('[knots]')
    ax.text(0.02, 0.91, 'UPCOAST', fontsize=10, transform=ax.transAxes)
    ax.text(0.02, 0.04, 'DOWNCOAST', fontsize=10, transform=ax.transAxes)
    ax.text(0.9, 0.9, str(angle['B']-90) + '$^\circ$T', fontsize=11, transform=ax.transAxes)

    # T/S
    cmicro = '0.6'
    cDCS = '0.0'
    csalt = 'm'
    ax = axes[3]
    idx = mpl.dates.date2num(df.index.to_pydatetime())
    ax.plot(idx, df.WaterT, lw=lw, color=cDCS, linestyle='-')
    idx = mpl.dates.date2num(dfsalt.index.to_pydatetime())
    ax.plot(idx, dfsalt.Temp, lw=lw, color=cmicro, linestyle='-')
    ax.set_ylabel(r'Temperature $\left[^\circ\mathrm{C}\right]$')
    # set bottom ylim a little large to make room for text
    ylim = ax.get_ylim()
    ax.set_ylim(ylim[0]*0.98, ylim[1])
    # Fahrenheit
    axF = ax.twinx()
    axF.spines["left"].set_position(("axes", -0.16))
    # make spine visible
    # http://matplotlib.org/examples/pylab_examples/multiple_yaxis_with_spines.html
    def make_patch_spines_invisible(ax):
        ax.set_frame_on(True)
        ax.patch.set_visible(False)
        for sp in ax.spines.values():
            sp.set_visible(False)
    make_patch_spines_invisible(axF)
    # put spine on left, and shift farther to the left too
    # http://stackoverflow.com/questions/20146652/two-y-axis-on-the-left-side-of-the-figure
    axF.spines["left"].set_visible(True)
    axF.yaxis.set_label_position('left')
    axF.yaxis.set_ticks_position('left')
    axF.set_ylabel(r'$\left[^\circ\mathrm{F}\right]$')
    ylim = ax.get_ylim()
    # convert to fahrenheit
    axF.set_ylim(ylim[0]*(9/5.)+32, ylim[1]*(9/5.)+32)


    # salinity
    axS = ax.twinx()
    idx = mpl.dates.date2num(dfsalt.index.to_pydatetime())
    axS.plot(idx, dfsalt.Salinity, lw=lw, color=csalt, linestyle='--')
    axS.set_ylabel('\nSalinity', color='m')
    axS.tick_params(axis='y', colors='m')
    # labels with lines
    ax.text(0.01, 0.01, 'DCS', color=cDCS, transform=ax.transAxes, fontsize=11)
    ax.text(0.1, 0.01, 'Microcat', color=cmicro, transform=ax.transAxes, fontsize=11)
    # set bottom ylim a little large to make room for text
    ylim = axS.get_ylim()
    axS.set_ylim(ylim[0]*0.98, ylim[1])

    # hourly minor ticks
    hours = mpl.dates.HourLocator()
    ax.xaxis.set_minor_locator(hours)
    halfdays = mpl.dates.HourLocator(byhour=[0,12])
    ax.xaxis.set_major_locator(halfdays)
    ax.xaxis.set_major_formatter(mpl.dates.DateFormatter('%b %d, %H:%M'))

    # Year for first entry
    ax.text(0.98, -0.25, datetime.strftime(df.index[0], '%Y'),
            transform=ax.transAxes, rotation=30)


    # rotates and right aligns the x labels, and moves the bottom of the
    # axes up to make room for them
    fig.autofmt_xdate(bottom=0.125)

    # text at bottom
    # right hand side
    text = 'Oceanography and GERG at Texas A&M University\n' \
           + time.strftime('%a %b %d, %Y %H:%M GMT%z')
    fig.text(0.95, 0.035, text, fontsize=8, transform=fig.transFigure,
             horizontalalignment='right', verticalalignment='top')
    # left hand side
    text = 'TGLO, GERG, Oceanography, and Texas A&M make no representations\n' \
           + 'or any other warranty with regard to this data.\n' \
           + 'These data are not suitable for navigation purposes.'
    fig.text(0.08, 0.035, text, fontsize=8, transform=fig.transFigure,
             horizontalalignment='left', verticalalignment='top')

    fig.savefig('test.pdf')



if __name__ == "__main__":

    if args.which == 'ven':
        ven(args.dataname)
