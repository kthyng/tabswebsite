'''
Make plot of recent buoy data.

python plot_buoy.py -h for help
python plot_buoy.py 'ven' '../tmp/FvengV2KrI'
python plot_buoy.py 'ven' '../tmp/Fven7YU0EB'
python plot_buoy.py 'eng' '../tmp/FengUy3wt2'
'''

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import buoy_data as bd
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
wmax = 15  # m/s, max wind arrow value
lw = 1.5
c2 = 'cornflowerblue'


def df_init(df):
    '''Return dataframe df with indices idx and time length dT added.

    Can't use datetime index directly unfortunately here, so can't use pandas later either
    idx and dT are deleted by the resample command
    '''

    df.idx = date2num(df.index.to_pydatetime())  # in units of days
    df.dT = df.idx[-1] - df.idx[0]  # length of dataset in days

    return df


def shifty(ax, N=0.05):
    '''Shift y limit to give some space to data in plot.

    N   decimal between 0 and 1 of range of y data to add onto y limits.
    N=0 is a special case for shifting one y limit so that 0 is included in view.
    This is used when currents need 0 as a reference.
    '''

    ylims = ax.get_ylim()
    dy = ylims[1] - ylims[0]

    if N == 0:  # to shift around 0
        if ylims[0]>=0:
            ax.set_ylim(-dy*0.05, ylims[1])
        elif ylims[1]<=0:
            ax.set_ylim(ylims[0], dy*0.05)
    else:  # to expand the space at top and bottom of plot
        ax.set_ylim(ylims[0] - dy*N, ylims[1] + dy*N)


def setymaxrange(ax, ymaxrange):
    '''Set max allowed range of y if limits are over.'''

    ylim = np.asarray(ax.get_ylim())
    if ylim[0] < ymaxrange[0]:
        ylim[0] = ymaxrange[0]
    if ylim[1] > ymaxrange[1]:
        ylim[1] = ymaxrange[1]
    if ylim[1] < ymaxrange[0]:  # weird case with missing values
        ylim[1] = ymaxrange[1]
    ax.set_ylim(ylim)

def ss(data, model):
    '''Calculate skill score between data and model.'''

    return 1 - ((data - model)**2).sum() / (data**2).sum()


def r2(data, model):
    '''Calculate r^2 for data and model.'''

    return (np.corrcoef(data, model)**2)[0,1]


def add_r2(ax, df, df2, df3, key):
    '''Make adjustments and add r^2 to subplot.'''

    shifty(ax)  # most functions already have one of these, do another for space
    if df2 is not None or df3 is not None:
        # account for if df2 and df3 overlap
        dfnew = pd.concat([df2, df3]).resample('30T').interpolate()  # in case there is a df3
        # reindex model dfnew to match data df for calculations
        dfnew = dfnew.reindex_like(df)#.interpolate()
        if dfnew[key].sum():
                # ax.text(0.8, 0.04, 'skill score: %1.2f' % ss(df, dfnew)[which], color=c2, fontsize=10, transform=ax.transAxes)
            ax.text(0.85, 0.04, 'r$^2$: %1.2f' % r2(df[key], dfnew[key]), color=c2, fontsize=10, transform=ax.transAxes)


def add_rhs(ax1, label, con):
    '''Add axis to right hand side of subplot.'''

    ax2 = ax1.twinx()
    ax2.set_ylabel(label)
    ax2.get_yaxis().get_major_formatter().set_useOffset(False)  # no shift for yaxis
    ylim = ax1.get_ylim()
    ax2.set_ylim(tools.convert(ylim[0], con), tools.convert(ylim[1], con))


def add_legend(ax, df2, df3):
    '''Add legend for data vs. model.'''

    ax.text(0.4, 0.04, 'data', color='k', fontsize=10, transform=ax.transAxes)
    if df2 is not None:
        ax.text(0.5, 0.04, "{}".format("\u2014 hindcast"), color=c2, fontsize=10, transform=ax.transAxes)
    if df3 is not None:
        ax.text(0.65, 0.04, '-- forecast', color=c2, fontsize=10, transform=ax.transAxes)


def add_currents(ax, df, which, east, north, compass=True, df2=None, df3=None, tlims=None):
    '''Add current arrows to plot

    which   'water' or 'wind'
    '''
    color = 'k'  # color of data arrows

    # if data is not within input time range, use model output instead
    # import pdb; pdb.set_trace()
    # if df is None and tlims is not None:
    if tlims is not None:
        if df.idx[-1] < tlims[0] or df.idx[0] > tlims[-1]:
            df = df_init(pd.concat([df2, df3]))  # in case there is a df3
            color = c2

    # arrows with no heads for lines
    # http://stackoverflow.com/questions/37154071/python-quiver-plot-without-head
    if df.dT <=2:  # less than or equal to two days
        width = 1.0
        if which == 'wind':
            width /= 3
    elif df.dT <=6:  # less than or equal to 6 days
        width = 0.5
        if which == 'wind':
            width /= 3
    else:
        width = 0.2
    # decimate temporally
    if df.dT < 5*30:
        ddt = 1
    elif df.dT < 7*30:
        ddt = 2
    elif df.dT < 11*30:
        ddt = 3
    elif df.dT < 15*30:
        ddt = 4
    else:
        ddt = 5
    ax.quiver(df.idx[::ddt], np.zeros(len(df[::ddt])), df[::ddt][east], df[::ddt][north], headaxislength=0,
              headlength=0, width=width, units='y', scale_units='y', scale=1, color=color)

    # use forecast currents to fill in after data
    if df3 is not None and not df[df3.index[0]:].equals(df3):
        if df.index[-1] > df3.index[0]:
            stemp = df.index[-1] + timedelta(minutes=30)
            df3 = df3[stemp:]
            df3.idx = date2num(df3.index.to_pydatetime())  # in units of days
            df3.dT = df3.idx[-1] - df3.idx[0]  # length of dataset in days

        ax.quiver(df3.idx[::ddt], np.zeros(len(df3[::ddt])), df3[::ddt][east], df3[::ddt][north], headaxislength=0,
                  headlength=0, width=width, units='y', scale_units='y', scale=1, color=c2)

    # if df2 is not None:  # 2nd set of arrows
    #     ax.quiver(df2.idx[::ddt], np.zeros(len(df2[::ddt])), df2[::ddt][east], df2[::ddt][north], headaxislength=0,
    #               headlength=0, width=width, units='y', scale_units='y', scale=1,
    #               color=c2)
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
    if compass:
        ax.annotate("", xy=(1.1, 0.95), xytext=(1.1, 0.83),
                arrowprops=dict(arrowstyle="->"), xycoords='axes fraction')
        ax.text(1.1, 0.77, 'N', transform=ax.transAxes,
                horizontalalignment='center', fontsize=10)
    # knots on right side
    axknots = ax.twinx()
    axknots.set_ylim(-varmax2, varmax2)
    axknots.set_ylabel('[knots]')


def add_vel(ax, df, buoy, which, ymaxrange=None, df2=None, df3=None):
    '''Add along- or across-shelf velocity to plot

    which   'Across' or 'Along'
    '''

    ax.plot(df.idx, df[which], 'k', lw=lw)
    if df2 is not None:
        ax.plot(df2.idx, df2[which], color=c2, lw=lw)
    if df3 is not None:
        ax.plot(df3.idx, df3[which], color=c2, lw=lw, ls='--')
    # add line at zero for reference. First get limits in x direction.
    idxmin = min(df.idx); idxmax = max(df.idx)
    for dftemp in [df2, df3]:
        if dftemp is not None:
            idxmin = min((idxmin, dftemp.idx.min()))
            idxmax = max((idxmax, dftemp.idx.max()))
    ax.plot([idxmin, idxmax], [0,0], 'k:')
    # add r^2 to subplot
    add_r2(ax, df, df2, df3, which)
    # Enforce max limits for y axis in case data is very large or small
    if ymaxrange is not None:
        setymaxrange(ax, ymaxrange)
    # give some extra space along top and bottom of subplot
    shifty(ax, N=0.1)
    # force 0 line to be within y limits
    shifty(ax, N=0)
    if which == 'Across [cm/s]':
        ax.set_ylabel('Cross-shelf flow\n' + r'$\left[ \mathrm{cm} \cdot \mathrm{s}^{-1} \right]$')
    elif which == 'Along [cm/s]':
        ax.set_ylabel('Along-shelf flow\n' + r'$\left[ \mathrm{cm} \cdot \mathrm{s}^{-1} \right]$')
    # convert to knots on rhs
    add_rhs(ax, '[knots]', 'cps2kts')
    # axknots = ax.twinx()
    # axknots.set_ylim(tools.convert(ylim[0], 'cps2kts'), tools.convert(ylim[1], 'cps2kts'))
    # axknots.set_ylabel('[knots]')
    if which == 'Across [cm/s]':
        ax.text(0.02, 0.93, 'OFFSHORE', fontsize=10, transform=ax.transAxes)
        ax.text(0.02, 0.04, 'ONSHORE', fontsize=10, transform=ax.transAxes)
        # add angle
        ax.text(0.9, 0.91, str(bd.angle(buoy)) + '˚T', fontsize=10, transform=ax.transAxes)
    elif which == 'Along [cm/s]':
        ax.text(0.02, 0.93, 'UPCOAST (to LA)', fontsize=10, transform=ax.transAxes)
        ax.text(0.02, 0.04, 'DOWNCOAST (to MX)', fontsize=10, transform=ax.transAxes)
        # add angle
        ax.text(0.9, 0.91, str(bd.angle(buoy)-90) + '˚T', fontsize=10, transform=ax.transAxes)


def add_var_2units(ax1, df, key, label1, con, label2, ymaxrange=None, df2=None,
                   df3=None, tlims=None, dolegend=False):
    '''Plot with units on both left and right sides of plot.'''

    ax1.plot(df.idx, df[key], lw=lw, color='k', linestyle='-')
    if df2 is not None:
        ax1.plot(df2.idx, df2[key], lw=lw, color=c2, linestyle='-')
    if df3 is not None:
        ax1.plot(df3.idx, df3[key], lw=lw, color=c2, linestyle='--')
    ax1.set_ylabel(label1)
    ax1.get_yaxis().get_major_formatter().set_useOffset(False)  # no shift for pressure
    if tlims is not None:  # set y range by signal within tlims (in case data off-screen changing it)
        ymins = []; ymaxs = []
        if df2 is not None:
            ymins.append(df2[key].min())
            ymaxs.append(df2[key].max())
        if df3 is not None:
            ymins.append(df3[key].min())
            ymaxs.append(df3[key].max())
        # check if data df is contained in tlims
        # 1st: if nothing in df is larger than the first tlims value, or
        # 2nd: if nothing in df is smaller than the last tlims value,
        # use df to set y range since df is contained in tlims
        if not ((df.idx >= tlims[0]).sum() == 0) or ((df.idx <= tlims[-1]).sum() == 0):
            # then range also set by df
            ymins.append(df[key].min())
            ymaxs.append(df[key].max())
        if ymins != []:
            ymin = min(ymins)
            ymax = max(ymaxs)
            ax1.set_ylim(ymin, ymax)
    if ymaxrange is not None:  # Have max limits for y axis
        setymaxrange(ax1, ymaxrange)
    shifty(ax1)
    # add r^2 to subplot
    add_r2(ax1, df, df2, df3, key)
    # add data/model legend
    if dolegend:
        add_legend(ax1, df2, df3)
    # right side units
    add_rhs(ax1, label2, con)
    # ax2 = ax1.twinx()
    # ax2.set_ylabel(label2)
    # ax2.get_yaxis().get_major_formatter().set_useOffset(False)  # no shift for pressure
    # ylim = ax1.get_ylim()
    # ax2.set_ylim(tools.convert(ylim[0], con), tools.convert(ylim[1], con))


def add_var(ax, df, var, varlabel, ymaxrange=None, df2=None, df3=None, dolegend=False):
    '''Add basic var to plot as line plot with no extra space.'''

    ax.plot(df.idx, df[var], lw=lw, color='k', linestyle='-')
    if df2 is not None:
        ax.plot(df2.idx, df2[var], lw=lw, color=c2, linestyle='-')
    if df3 is not None:
        ax.plot(df3.idx, df3[var], lw=lw, color=c2, linestyle='--')
    ax.set_ylabel(varlabel)
    ax.get_yaxis().get_major_formatter().set_useOffset(False)  # no shift for y limits
    if ymaxrange is not None:  # Have max limits for y axis
        setymaxrange(ax, ymaxrange)
    shifty(ax)
    # add r^2 to subplot
    add_r2(ax, df, df2, df3, var)
    # add data/model legend
    if dolegend:
        add_legend(ax, df2, df3)


def add_2var(ax1, df, var1, label1, var2, label2, ymaxrange=None, sameylim=False):
    '''2 variables, one on each y axis. same y limits if set True.'''

    c1, c2 = '#559349', '#874993'
    # 1st var
    ax1.plot(df.idx, df[var1], lw=lw, color=c1, linestyle='-')
    ax1.set_ylabel(label1, color=c1)
    ax1.tick_params(axis='y', colors=c1)
    if ymaxrange is not None:  # Have max limits for y axis
        setymaxrange(ax1, ymaxrange)
    shifty(ax1)
    # 2nd var
    ax2 = ax1.twinx()
    ax2.plot(df.idx, df[var2], lw=lw, color=c2, linestyle='--')
    ax2.set_ylabel(label2 + ' [--]', color=c2)
    ax2.tick_params(axis='y', colors=c2)
    if ymaxrange is not None:  # Have max limits for y axis
        setymaxrange(ax2, ymaxrange)
    shifty(ax2)
    if sameylim:
        ylim = ax1.get_ylim()
        ax2.set_ylim(ylim[0], ylim[1])


def add_2var_sameplot(ax, df, var1, label1, var2, ymaxrange=None):
    '''2 variables, one on each y axis. same y limits if set True.'''

    ax.plot(df.idx, df[var1], lw=lw, color='k', linestyle='-')
    ax.plot(df.idx, df[var2], lw=lw, color='k', linestyle='--')
    ax.set_ylabel(label1, color='k')
    if ymaxrange is not None:  # Have max limits for y axis
        setymaxrange(ax, ymaxrange)
    shifty(ax)


def add_xlabels(ax, df, fig, tlims=None):
    '''Add date labels to bottom x axis'''

    # varied tick locations and labels for few days
    if df.dT <=1:  # less than or equal to one day
        # hourly minor ticks
        hours = mpl.dates.HourLocator()
        ax.xaxis.set_minor_locator(hours)
        sixthdays = mpl.dates.HourLocator(byhour=np.arange(0,24,4))
        ax.xaxis.set_major_locator(sixthdays)
        ax.xaxis.set_major_formatter(mpl.dates.DateFormatter('%b %d, %H:%M'))
        if df.index[0].year != df.index[-1].year:
            ax.text(0.98, -0.05, df.index.strftime("%Y")[0] + '-' + df.index.strftime("%Y")[-1],
                    transform=ax.transAxes, rotation=30)
        else:
            ax.text(0.98, -0.15, df.index.strftime("%Y")[-1],
                    transform=ax.transAxes, rotation=30)
    elif df.dT <=2:  # less than or equal to two days
        # hourly minor ticks
        hours = mpl.dates.HourLocator()
        ax.xaxis.set_minor_locator(hours)
        quarterdays = mpl.dates.HourLocator(byhour=np.arange(0,24,6))
        ax.xaxis.set_major_locator(quarterdays)
        ax.xaxis.set_major_formatter(mpl.dates.DateFormatter('%b %d, %H:%M'))
        if df.index[0].year != df.index[-1].year:
            ax.text(0.98, -0.05, df.index.strftime("%Y")[0] + '-' + df.index.strftime("%Y")[-1],
                    transform=ax.transAxes, rotation=30)
        else:
            ax.text(0.98, -0.15, df.index.strftime("%Y")[-1],
                    transform=ax.transAxes, rotation=30)
    elif df.dT < 12*30:  # less than 12 months
        ax.xaxis.set_major_formatter(mpl.dates.DateFormatter('%b %d'))
        if df.index[0].year != df.index[-1].year:
            ax.text(0.98, -0.05, df.index.strftime("%Y")[0] + '-' + df.index.strftime("%Y")[-1],
                    transform=ax.transAxes, rotation=30)
        else:
            ax.text(0.98, -0.15, df.index.strftime("%Y")[-1],
                    transform=ax.transAxes, rotation=30)
    else:
        ax.xaxis.set_major_formatter(mpl.dates.DateFormatter('%b %d, %Y'))

    # put in GMT as time zone
    ax.text(1.05, -0.35, 'UTC', transform=ax.transAxes, fontsize=10)

    # tighten only x axis
    if tlims is not None:
        ax.set_xlim(tlims[0], tlims[1])
    else:
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


def setup(nsubplots, buoy=None):
    '''Set up plot'''

    # plot
    fig, axes = plt.subplots(nsubplots, 1, figsize=(8.5,11), sharex=True)
    # bottom controlled later
    fig.subplots_adjust(top=0.96, right=0.88, left=0.15, hspace=0.1)
    # title
    if buoy is not None:
        if len(buoy) == 1:
            title = 'TGLO TABS Buoy ' + buoy + ': ' + bd.locs(buoy)['lat'][0] +\
                    '˚' + bd.locs(buoy)['lat'][1] + '\'' + bd.locs(buoy)['lat'][2]\
                    + '  ' + bd.locs(buoy)['lon'][0] + '˚' + bd.locs(buoy)['lon'][1]\
                    + '\'' + bd.locs(buoy)['lon'][2]
        else:  # NDBC
            title = 'NDBC Station ' + buoy + ': ' + bd.locs(buoy)['lat'][0] +\
                    '˚' + bd.locs(buoy)['lat'][1] + '\'' + bd.locs(buoy)['lat'][2]\
                    + '  ' + bd.locs(buoy)['lon'][0] + '˚' + bd.locs(buoy)['lon'][1]\
                    + '\'' + bd.locs(buoy)['lon'][2]
        axes[0].set_title(title, fontsize=18)

    return fig, axes


def plot(df, buoy, which, df2=None, df3=None, tlims=None):
    '''Plot data.

    Find data in dataname and save fig, both in /tmp.
    Optional df2. If given, also plot on each axis.
    '''

    if which == 'ven' or which == 'eng' or which == 'met' or which == 'sum':
        nsubplots = 4
    elif which == 'salt' or which == 'wave':
        nsubplots = 3
    elif which == 'ndbc':
        nsubplots = 5

    if which != 'wave' and which !='ndbc':
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
    elif which == 'ndbc':
        # fill in missing data at 60 min frequency as nans so not plotted
        base = df.index[0].minute
        df = df.resample('60T', base=base).asfreq()

    df = df_init(df)

    # change length of df3 if df2 overlaps with it
    if df2 is not None and df3 is not None:
        if df2.index[-1] > df3.index[0]:
            stemp = df2.index[-1] + timedelta(minutes=30)
            df3 = df3[stemp:]
            df3.idx = date2num(df3.index.to_pydatetime())  # in units of days
            df3.dT = df3.idx[-1] - df3.idx[0]  # length of dataset in days

    fig, axes = setup(nsubplots=nsubplots, buoy=buoy)

    if which == 'ven':
        add_currents(axes[0], df, 'water', 'East [cm/s]', 'North [cm/s]', df2=df2, df3=df3, tlims=tlims)
        add_vel(axes[1], df, buoy, 'Across [cm/s]', ymaxrange=[-110, 110], df2=df2, df3=df3)
        add_vel(axes[2], df, buoy, 'Along [cm/s]', ymaxrange=[-110, 110], df2=df2, df3=df3)
        add_var_2units(axes[3], df, 'WaterT [deg C]', 'Water temperature [˚C]',
                       'c2f', '[˚F]', ymaxrange=[10, 32], df2=df2, df3=df3,
                       tlims=tlims, dolegend=True)
    elif which == 'eng':
        add_2var_sameplot(axes[0], df, 'VBatt [Oper]', 'V$_\mathrm{batt}$', 'VBatt [sleep]', ymaxrange=[0, 15])
        add_var(axes[1], df, 'SigStr [dB]', 'Sig Str [dB]', ymaxrange=[-25, 0])
        add_var(axes[2], df, 'Nping', 'Ping Cnt', ymaxrange=[30, 210])
        add_2var(axes[3], df, 'Tx', 'Tx', 'Ty', 'Ty', ymaxrange=[-20, 20])
    elif which == 'met':
        add_currents(axes[0], df, 'wind', 'East [m/s]', 'North [m/s]', df2=df2, df3=df3, tlims=tlims)
        add_var_2units(axes[1], df, 'AirT [deg C]', 'Air temperature [˚C]',
                       'c2f', '[˚F]', ymaxrange=[-25,40], df2=df2, df3=df3, tlims=tlims)
        add_var_2units(axes[2], df, 'AtmPr [MB]', 'Atmospheric pressure\n[MB]',
                       'mb2hg', '[inHg]', ymaxrange=[1000,1040], df2=df2, df3=df3, tlims=tlims)
        add_var(axes[3], df, 'RelH [%]', 'Relative Humidity [%]',
                ymaxrange=[0,110], df2=df2, df3=df3, dolegend=True)
    elif which == 'salt':
        add_var_2units(axes[0], df, 'Temp [deg C]', 'Water temperature [˚C]',
                       'c2f', '[˚F]', ymaxrange=[10, 32], df2=df2, df3=df3, tlims=tlims)
        add_var(axes[1], df, 'Salinity', 'Salinity', ymaxrange=[15, 36], df2=df2, df3=df3)
        # add_var(axes[2], df, 'Cond [ms/cm]', 'Conductivity [ms/cm]', ymaxrange=[3, 60])
        add_var(axes[2], df, 'Density [kg/m^3]', 'Density [kg$\cdot$ m$^{-3}$]',
                df2=df2, df3=df3, ymaxrange=[1015, 1036], dolegend=True)
    elif which == 'wave':
        add_var_2units(axes[0], df, 'WaveHeight [m]', 'Wave Height [m]',
                       'm2ft', '[ft]', ymaxrange=[0,5], tlims=tlims)
        add_var(axes[1], df, 'MeanPeriod [s]', 'Mean Period [s]')
        add_var(axes[2], df, 'PeakPeriod [s]', 'Peak Period [s]', ymaxrange=[2,12])
    elif which == 'ndbc':
        add_currents(axes[0], df, 'wind', 'East [m/s]', 'North [m/s]', df2=df2, df3=df3, tlims=tlims)
        add_var_2units(axes[1], df, 'AtmPr [MB]', 'Atmospheric pressure\n[MB]',
                       'mb2hg', '[inHg]', ymaxrange=[1000,1040], tlims=tlims)
        add_var_2units(axes[2], df, 'Wave Ht [m]', 'Wave Height [m]',
                       'm2ft', '[ft]', ymaxrange=[0,5], tlims=tlims)
        add_var(axes[3], df, 'Wave Pd [s]', 'Wave Period [s]', ymaxrange=[0,12])
        add_var_2units(axes[4], df, 'WaterT [deg C]', 'Water temp [˚C]',
                       'c2f', '[˚F]', ymaxrange=[10, 32], df2=df2, df3=df3, tlims=tlims)
    # use longer dataframe in case data or model are cut short
    if df2 is not None or df3 is not None and tlims is not None:
        dfm = df_init(pd.concat([df2, df3]))

        if dfm.dT > df.dT:
            df = dfm  # use the longer dataframe for labeling x axis

    add_xlabels(axes[nsubplots-1], df, fig, tlims=tlims)

    return fig


def currents(dfs, buoys):
    '''Plot currents for all active buoys.'''

    fig, axes = setup(nsubplots=len(dfs))

    first = True  # flag for first currents plot
    for ax, df, buoy in zip(axes, dfs, buoys):

        if df is None:
            ax.text(0.2, 0.5, 'Data not available for buoy ' + buoy + ' at this time.', transform=ax.transAxes)
            ax.get_yaxis().set_ticks([])
            continue

        # label buoy plots
        if len(dfs) == 5:
            ax.text(0.95, 0.75, buoy, transform=ax.transAxes,
                    horizontalalignment='center', fontsize=30, alpha=0.3)
        elif len(dfs) == 4:
            ax.text(0.95, 0.8, buoy, transform=ax.transAxes,
                    horizontalalignment='center', fontsize=30, alpha=0.3)
        # ax.text(0.97, 0.9, buoy, transform=ax.transAxes,
        #         horizontalalignment='center', fontsize=14)

        df = df_init(df)
        if first:
            add_currents(ax, df, 'water', 'East [cm/s]', 'North [cm/s]', compass=True)
            first = False
        else:
            add_currents(ax, df, 'water', 'East [cm/s]', 'North [cm/s]', compass=False)

        # save a df for labeling the bottom axis if it has at least 4 days of data
        # otherwise it squishes up the labels a lot
        if df.dT > 4:
            dfsave = df  # save for using with bottom labeling

    add_xlabels(axes[len(dfs)-1], dfsave, fig)

    return fig
