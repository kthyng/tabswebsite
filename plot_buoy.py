'''
Make plot of recent buoy data.

python plot_buoy.py -h for help
python plot_buoy.py 'ven' '../tmp/FvengV2KrI'
python plot_buoy.py 'ven' '../tmp/Fven7YU0EB'
python plot_buoy.py 'eng' '../tmp/FengUy3wt2'
'''

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import buoy_data
from datetime import datetime, timedelta
import tools
from matplotlib.dates import date2num
import pandas as pd


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


# constants
cmax = 60  # cm/s, max water arrow value
wmax = 20  # m/s, max wind arrow value
lw = 1.5
c2 = 'cornflowerblue'


def shifty(ax, N=0.05):
    '''Shift y limit to give some space to data in plot.

    N   decimal between 0 and 1 of range of y data to add onto y limits.
    '''

    ylims = ax.get_ylim()
    dy = ylims[1] - ylims[0]
    ax.set_ylim(ylims[0] - dy*N, ylims[1] + dy*N)


def add_currents(ax, df, which, east, north, df2=None):
    '''Add current arrows to plot

    which   'water' or 'wind'
    '''

    # arrows with no heads for lines
    # http://stackoverflow.com/questions/37154071/python-quiver-plot-without-head
    if df.dT <=2:  # less than or equal to two days
        width = 1.0
        if which == 'wind':
            width /= 3
    else:
        width = 0.15
    ax.quiver(df.idx, np.zeros(len(df)), df[east], df[north], headaxislength=0,
              headlength=0, width=width, units='y', scale_units='y', scale=1)
    if df2 is not None:  # 2nd set of arrows
        ax.quiver(df2.idx, np.zeros(len(df2)), df2[east], df2[north], headaxislength=0,
                  headlength=0, width=width, units='y', scale_units='y', scale=1,
                  color=c2)
    if which == 'water':
        varmax = cmax
        label = 'Currents\n' + r'$\left[ \mathrm{cm} \cdot \mathrm{s}^{-1} \right]$'
        varmax2 = tools.convert(varmax, 'cps2kts')  # convert to knots
    elif which == 'wind':
        varmax = wmax
        label = 'Wind velocity\n' + r'$\left[ \mathrm{m} \cdot \mathrm{s}^{-1} \right]$'
        varmax2 = tools.convert(varmax, 'mps2kts')  # convert to knots
    ax.set_ylim(-varmax, varmax)
    ax.set_ylabel(label)

    # compass arrow
    ax.annotate("", xy=(1.1, 0.95), xytext=(1.1, 0.83),
            arrowprops=dict(arrowstyle="->"), xycoords='axes fraction')
    ax.text(1.1, 0.77, 'N', transform=ax.transAxes,
            horizontalalignment='center', fontsize=10)
    # knots on right side
    axknots = ax.twinx()
    axknots.set_ylim(-varmax2, varmax2)
    axknots.set_ylabel('[knots]')


def add_vel(ax, df, buoy, which, df2=None, df3=None):
    '''Add along- or across-shelf velocity to plot

    which   'Across' or 'Along'
    '''

    ax.plot(df.idx, df[which], 'k', lw=lw)
    if df2 is not None:
        ax.plot(df2.idx, df2[which], color=c2, lw=lw)
        # add skill score
        dfnew = pd.concat([df2, df3]).resample('30T').asfreq()  # in case there is a df3
        ind = pd.notnull(df[which]) & pd.notnull(dfnew[which])
        ss = 1 - ((df - dfnew)**2).sum() / (df[ind]**2).sum()
        ax.text(0.8, 0.04, 'skill score: %1.2f' % ss[which], color=c2, fontsize=10, transform=ax.transAxes)
    if df3 is not None:
        ax.plot(df3.idx, df3[which], color=c2, lw=lw, ls='--')
    ax.plot(df.idx, np.zeros(df.idx.size), 'k:')
    shifty(ax, N=0.1)
    # force 0 line to be within y limits
    ylim = ax.get_ylim()
    # adjust shifty to cover this case too
    dy = ylim[1] - ylim[0]

    if ylim[0]>=0:
        # ylim[0] = -2
        ax.set_ylim(-dy*0.05, ylim[1])
    elif ylim[1]<=0:
        # ylim[1] = 2
        ax.set_ylim(ylim[0], dy*0.05)
    if which == 'Across [cm/s]':
        ax.set_ylabel('Cross-shelf flow\n' + r'$\left[ \mathrm{cm} \cdot \mathrm{s}^{-1} \right]$')
    elif which == 'Along [cm/s]':
        ax.set_ylabel('Along-shelf flow\n' + r'$\left[ \mathrm{cm} \cdot \mathrm{s}^{-1} \right]$')
    # convert to knots
    axknots = ax.twinx()
    axknots.set_ylim(tools.convert(ylim[0], 'cps2kts'), tools.convert(ylim[1], 'cps2kts'))
    axknots.set_ylabel('[knots]')
    if which == 'Across [cm/s]':
        ax.text(0.02, 0.93, 'OFFSHORE', fontsize=10, transform=ax.transAxes)
        ax.text(0.02, 0.04, 'ONSHORE', fontsize=10, transform=ax.transAxes)
        # add angle
        ax.text(0.9, 0.91, str(buoy_data.angle(buoy)) + '˚T', fontsize=10, transform=ax.transAxes)
        if df2 is not None:
            # legend for inputs
            ax.text(0.4, 0.04, 'data', color='k', fontsize=10, transform=ax.transAxes)
            ax.text(0.5, 0.04, 'model (-- forecast)', color=c2, fontsize=10, transform=ax.transAxes)
    elif which == 'Along [cm/s]':
        ax.text(0.02, 0.93, 'UPCOAST (to LA)', fontsize=10, transform=ax.transAxes)
        ax.text(0.02, 0.04, 'DOWNCOAST (to MX)', fontsize=10, transform=ax.transAxes)
        # add angle
        ax.text(0.9, 0.91, str(buoy_data.angle(buoy)-90) + '˚T', fontsize=10, transform=ax.transAxes)


def add_var_2units(ax1, df, key, label1, con, label2, df2=None, df3=None):
    '''Plot with units on both left and right sides of plot.'''

    ax1.plot(df.idx, df[key], lw=lw, color='k', linestyle='-')
    if df2 is not None:
        ax1.plot(df2.idx, df2[key], lw=lw, color=c2, linestyle='-')
    if df3 is not None:
        ax1.plot(df3.idx, df3[key], lw=lw, color=c2, linestyle='--')
    ax1.set_ylabel(label1)
    ax1.get_yaxis().get_major_formatter().set_useOffset(False)  # no shift for pressure
    shifty(ax1)
    # right side units
    ax2 = ax1.twinx()
    ax2.set_ylabel(label2)
    ylim = ax1.get_ylim()
    ax2.set_ylim(tools.convert(ylim[0], con), tools.convert(ylim[1], con))


def add_var(ax, df, var, varlabel, df2=None, df3=None):
    '''Add basic var to plot as line plot with no extra space.'''

    ax.plot(df.idx, df[var], lw=lw, color='k', linestyle='-')
    if df2 is not None:
        ax.plot(df2.idx, df2[var], lw=lw, color=c2, linestyle='-')
    if df3 is not None:
        ax.plot(df3.idx, df3[var], lw=lw, color=c2, linestyle='--')
    ax.set_ylabel(varlabel)
    shifty(ax)


def add_2var(ax1, df, var1, label1, var2, label2, sameylim=False):
    '''2 variables, one on each y axis. same y limits if set True.'''

    c1, c2 = '#559349', '#874993'
    # 1st var
    ax1.plot(df.idx, df[var1], lw=lw, color=c1, linestyle='-')
    ax1.set_ylabel(label1, color=c1)
    ax1.tick_params(axis='y', colors=c1)
    shifty(ax1)
    # 2nd var
    ax2 = ax1.twinx()
    ax2.plot(df.idx, df[var2], lw=lw, color=c2, linestyle='--')
    ax2.set_ylabel(label2 + ' [--]', color=c2)
    ax2.tick_params(axis='y', colors=c2)
    shifty(ax2)
    if sameylim:
        ylim = ax1.get_ylim()
        ax2.set_ylim(ylim[0], ylim[1])


def add_2var_sameplot(ax, df, var1, label1, var2):
    '''2 variables, one on each y axis. same y limits if set True.'''

    ax.plot(df.idx, df[var1], lw=lw, color='k', linestyle='-')
    ax.plot(df.idx, df[var2], lw=lw, color='k', linestyle='--')
    ax.set_ylabel(label1, color='k')
    shifty(ax)


def add_xlabels(ax, df, fig):
    '''Add date labels to bottom x axis'''

    # varied tick locations and labels for few days
    if df.dT <=1:  # less than or equal to one day
        # hourly minor ticks
        hours = mpl.dates.HourLocator()
        ax.xaxis.set_minor_locator(hours)
        sixthdays = mpl.dates.HourLocator(byhour=np.arange(0,24,4))
        ax.xaxis.set_major_locator(sixthdays)
        ax.xaxis.set_major_formatter(mpl.dates.DateFormatter('%b %d, %H:%M'))
    elif df.dT <=2:  # less than or equal to two days
        # hourly minor ticks
        hours = mpl.dates.HourLocator()
        ax.xaxis.set_minor_locator(hours)
        quarterdays = mpl.dates.HourLocator(byhour=np.arange(0,24,6))
        ax.xaxis.set_major_locator(quarterdays)
        ax.xaxis.set_major_formatter(mpl.dates.DateFormatter('%b %d, %H:%M'))
    else:
        ax.xaxis.set_major_formatter(mpl.dates.DateFormatter('%b %d'))

    # Year for last entry
    # catch special case of last tick switching over to new year without actual data doing so
    # do this if the data is for december only but the final tick label is for january
    # import pdb; pdb.set_trace()
    # if (df.index[-1].month == 12) and (ax.get_xticklabels(which='major')[-1].get_text()[:3] == 'Jan'):
    #     ax.text(0.98, -0.25, datetime.strftime(df.index[-1].year+1, '%Y'),
    #             transform=ax.transAxes, rotation=30)
    # else:
    # note: I haven't been able to figure out how to update this year in the special case
    ax.text(0.98, -0.25, df.index.strftime("%Y")[-1],
            transform=ax.transAxes, rotation=30)

    # put in GMT as time zone
    ax.text(1.05, -0.25, '[UTC]', transform=ax.transAxes, rotation=30)

    # tighten only x axis
    plt.autoscale(enable=True, axis='x', tight=True)

    # rotates and right aligns the x labels, and moves the bottom of the
    # axes up to make room for them
    fig.autofmt_xdate(bottom=0.125)

    # text at bottom
    # right hand side
    text = 'Oceanography and GERG at Texas A&M University\n' \
           + datetime.utcnow().strftime('%a %b %d, %Y %H:%M UTC')
    fig.text(0.95, 0.035, text, fontsize=8, transform=fig.transFigure,
             horizontalalignment='right', verticalalignment='top')
    # left hand side
    text = 'TGLO, GERG, Oceanography, and Texas A&M make no representations\n' \
           + 'or any other warranty with regard to this data.\n' \
           + 'These data are not suitable for navigation purposes.'
    fig.text(0.08, 0.035, text, fontsize=8, transform=fig.transFigure,
             horizontalalignment='left', verticalalignment='top')


def setup(buoy, nsubplots):
    '''Set up plot'''

    # plot
    fig, axes = plt.subplots(nsubplots, 1, figsize=(8.5,11), sharex=True)
    # bottom controlled later
    fig.subplots_adjust(top=0.96, right=0.88, left=0.15, hspace=0.1)
    # title
    axes[0].set_title('TGLO TABS Buoy ' + buoy + ': ' +
                      buoy_data.locs(buoy)['lat'][0] + '˚' +
                      buoy_data.locs(buoy)['lat'][1] + '\'' +
                      buoy_data.locs(buoy)['lat'][2] + '  ' +
                      buoy_data.locs(buoy)['lon'][0] + '˚' +
                      buoy_data.locs(buoy)['lon'][1] + '\'' +
                      buoy_data.locs(buoy)['lon'][2], fontsize=18)

    return fig, axes


def plot(df, buoy, which, df2=None, df3=None):
    '''Plot data.

    Find data in dataname and save fig, both in /tmp.
    Optional df2. If given, also plot on each axis.
    '''

    if which == 'ven' or which == 'eng' or which == 'met' or which == 'sum':
        nsubplots = 4
    elif which == 'salt' or which == 'wave':
        nsubplots = 3

    if which != 'wave':
        # fill in missing data at 30 min frequency as nans so not plotted
        df = df.resample('30T').asfreq()
    elif which == 'wave':
        idx = df.index
        # check for gap over an hour. factor 1e9 due to nanoseconds.
        ind = (np.diff(idx)/1e9).astype(float) > 3700
        # if big gap, insert nan
        addidx = idx[:-1][ind] + timedelta(hours=1)  # extra indices to add into gaps
        # reindex dataframe with added entries for nans, and sort back into order
        df = df.reindex(np.hstack((idx, addidx))).sort_index()


    # can't use datetime index directly unfortunately here, so can't use pandas later either
    # idx and dT are deleted by the resample command
    df.idx = date2num(df.index.to_pydatetime())  # in units of days
    df.dT = df.idx[-1] - df.idx[0]  # length of dataset in days

    fig, axes = setup(buoy, nsubplots=nsubplots)

    if which == 'ven':
        add_currents(axes[0], df, 'water', 'East [cm/s]', 'North [cm/s]')
        add_vel(axes[1], df, buoy, 'Across [cm/s]', df2, df3)
        add_vel(axes[2], df, buoy, 'Along [cm/s]', df2, df3)
        add_var_2units(axes[3], df, 'WaterT [deg C]', 'Temperature [deg C]', 'c2f', '[˚F]', df2, df3)
    elif which == 'eng':
        add_2var_sameplot(axes[0], df, 'VBatt [Oper]', 'V$_\mathrm{batt}$', 'VBatt [sleep]')
        # add_var(axes[0], df, 'VBatt2', '')  # there are two of these
        # add_var(axes[0], df, 'VBatt', 'V$_\mathrm{batt}$')
        add_var(axes[1], df, 'SigStr [dB]', 'Sig Str [dB]')
        add_var(axes[2], df, 'Nping', 'Ping Cnt')
        add_2var(axes[3], df, 'Tx', 'Tx', 'Ty', 'Ty')
    elif which == 'met':
        add_currents(axes[0], df, 'wind', 'East [m/s]', 'North [m/s]')
        add_var_2units(axes[1], df, 'AirT [deg C]', 'Temperature [˚ C]', 'c2f', '[˚F]')
        add_var_2units(axes[2], df, 'AtmPr [MB]', 'Atmospheric pressure\n[MB]',
            'mb2hg', '[inHg]')
        add_var(axes[3], df, 'RelH [%]', 'Relative Humidity [%]')
    elif which == 'salt':
        add_var_2units(axes[0], df, 'Temp [deg C]', 'Temperature [˚C]', 'c2f', '[˚F]')
        add_var(axes[1], df, 'Salinity', 'Salinity')
        add_var(axes[2], df, 'Cond [ms/cm]', 'Conductivity [ms/cm]')
    elif which == 'wave':
        add_var(axes[0], df, 'WaveHeight [m]', 'Wave Height [m]')
        add_var(axes[1], df, 'MeanPeriod [s]', 'Mean Period [s]')
        add_var(axes[2], df, 'PeakPeriod [s]', 'Peak Period [s]')
    elif which == 'sum':
        add_currents(axes[0], df, 'water')
        add_vel(axes[1], df, 'Across')
        add_vel(axes[2], df, 'Along')
        add_var_2units(axes[3], df, 'WaterT', 'Temperature [˚C]', 'c2f', '[˚F]')

    add_xlabels(axes[nsubplots-1], df, fig)

    return fig


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
    theta = np.deg2rad(-(buoy_data.angle('B')-90))  # convert from compass to math angle
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
    ax.set_title('TGLO TABS Buoy B: ' + buoy_data.locs(buoy)[0] + ', ' + buoy_data.locs(buoy)[1], fontsize=18)

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
    ax.text(0.9, 0.9, str(buoy_data.angle('B')) + '˚T', fontsize=11, transform=ax.transAxes)
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
    ax.text(0.9, 0.9, str(buoy_data.angle('B')-90) + '˚T', fontsize=11, transform=ax.transAxes)

    # T/S
    cmicro = '0.6'
    cDCS = '0.0'
    csalt = 'm'
    ax = axes[3]
    idx = mpl.dates.date2num(df.index.to_pydatetime())
    ax.plot(idx, df.WaterT, lw=lw, color=cDCS, linestyle='-')
    idx = mpl.dates.date2num(dfsalt.index.to_pydatetime())
    ax.plot(idx, dfsalt.Temp, lw=lw, color=cmicro, linestyle='-')
    ax.set_ylabel('Temperature [˚C]')
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
    axF.set_ylabel('[˚F]')
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
