'''
Make plot of recent buoy data.

Easier to access through get_data.py
'''

import matplotlib as mpl
from sys import platform
if platform == 'linux':
    mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import tools
from matplotlib.dates import date2num, num2date
import pandas as pd
import pytz

mpl.rcParams.update({'font.size': 14})

# constants
cmax = 65  # cm/s, max water arrow value
wmax = 15  # m/s, max wind arrow value
lw = 1.5
c2 = 'cornflowerblue'  # #6495ed
c1 = '#4B70B2'  # darker shade of cornflowerblue
c3 = '#7764ED'

bys = pd.read_csv('../includes/buoys.csv', index_col=0)


def shifty(ax, N=0.05, which='both'):
    '''Shift y limit to give some space to data in plot.

    N   decimal between 0 and 1 of range of y data to add onto y limits.
    N=0 is a special case for shifting one y limit so that 0 is included in view.
    This is used when currents need 0 as a reference.
    which says whether to impact 'both' the top and bottom, 'top', or 'bottom'.
     this only applies when N!=0
    '''

    ylims = ax.get_ylim()
    dy = ylims[1] - ylims[0]

    if N == 0:  # to shift around 0
        if ylims[0]>=0:
            ax.set_ylim(-dy*0.05, ylims[1])
        elif ylims[1]<=0:
            ax.set_ylim(ylims[0], dy*0.05)
    else:  # to expand the space at top and bottom of plot
        if which == 'both':
            ax.set_ylim(ylims[0] - dy*N, ylims[1] + dy*N)
        elif which == 'top':
            ax.set_ylim(ylims[0], ylims[1] + dy*N)
        elif which == 'bottom':
            ax.set_ylim(ylims[0] - dy*N, ylims[1])


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


def setylimsintlims(ax, df, dfs, key, tlims):
    '''Adjusts ylimits to only account for plots visible in axes.'''

    if tlims is not None:
        ymins = []; ymaxs = []
        for dft in dfs:
            if dft is not None:
                ymins.append(dft[key].min())
                ymaxs.append(dft[key].max())
        # if df2 is not None:
        #     ymins.append(df2[key].min())
        #     ymaxs.append(df2[key].max())
        # if df3 is not None:
        #     ymins.append(df3[key].min())
        #     ymaxs.append(df3[key].max())
        if df is not None:
            # check if data df is contained in tlims
            # 1st: if nothing in df is larger than the first tlims value, or
            # 2nd: if nothing in df is smaller than the last tlims value,
            # use df to set y range since df is contained in tlims
            if not ((df['idx'] >= tlims[0]).sum() == 0) or ((df['idx'] <= tlims[-1]).sum() == 0):
                # then range also set by df
                ymins.append(df[key].min())
                ymaxs.append(df[key].max())
        if ymins != []:
            ymin = min(ymins)
            ymax = max(ymaxs)
            ax.set_ylim(ymin, ymax)


def ss(data, model):
    '''Calculate skill score between data and model.'''

    return 1 - ((data - model)**2).sum() / (data**2).sum()


def r2(data, model):
    '''Calculate r^2 for data and model.'''

    # create a local dataframe so that can calculate correlation while ignoring nan's
    df = pd.DataFrame(index=data.index, data={'data': data, 'model': model})
    return df.corr().loc['data','model']


def add_r2(ax, df, dfs, key, N=0.05):
    '''Make adjustments and add r^2 to subplot.'''

    shifty(ax, N=N, which='bottom')  # most functions already have one of these, do another for space
    # note don't do this if df is None or there is no model output
    if df is not None and sum([dft is not None for dft in dfs]) > 0:
    # if df is not None and (df1 is not None or df2 is not None or df3 is not None):
        # https://github.com/pandas-dev/pandas/issues/14297
        dfnew = pd.concat(dfs, sort=False)  # combine model output
        # remove any duplicated rows
        dfnew = dfnew[~dfnew.index.duplicated()]
        # interpolate on union of old and new index
        dfnew = dfnew.reindex(dfnew.index.union(df.index)).interpolate(method='time')
        # reindex to the new index
        dfnew = dfnew.reindex(df.index)

        if not df[key].isnull().all() and not dfnew[key].isnull().all():
                # ax.text(0.8, 0.04, 'skill score: %1.2f' % ss(df, dfnew)[which], color=c2, fontsize=10, transform=ax.transAxes)
            r2_use = r2(df[key], dfnew[key])
            if not np.isnan(r2_use):
                ax.text(0.85, 0.015, 'r$^2$: %1.2f' % r2_use, color=c2, fontsize=12, transform=ax.transAxes)


def add_rhs(ax1, label, con):
    '''Add axis to right hand side of subplot.'''

    ax2 = ax1.twinx()
    ax2.set_ylabel(label)
    ax2.get_yaxis().get_major_formatter().set_useOffset(False)  # no shift for yaxis
    ylim = ax1.get_ylim()
    ax2.set_ylim(tools.convert(ylim[0], con), tools.convert(ylim[1], con))


def add_legend(ax, df, df1, df2, df3, tlims, df4=None):
    '''Add legend for data vs. model.'''

    if df is not None:
        if (tlims is not None and df['idx'].iloc[-1]>tlims[0]) or tlims is None:
            ax.text(0.21, 0.015, 'data', color='k', fontsize=12, transform=ax.transAxes)
    if df1 is not None:
        ax.text(0.3, 0.015, "{}".format("\u2014 hindcast"), color=c1, fontsize=12, transform=ax.transAxes)
    if df2 is not None:
        ax.text(0.48, 0.015, "{}".format("\u2014 nowcast"), color=c2, fontsize=12, transform=ax.transAxes)
    if df3 is not None:
        ax.text(0.65, 0.015, '-- forecast', color=c2, fontsize=12, transform=ax.transAxes)
    # df4 overlaps with other labels because won't be on at the same time
    if df4 is not None:
        ax.text(0.55, 0.015, "{}".format("\u2014 NOAA prediction"), color=c3, fontsize=12, transform=ax.transAxes)


def add_zero(ax):
    '''Add dotted line at y=0.'''

    idxmin, idxmax = ax.get_xlim()
    ax.hlines(0, idxmin, idxmax, linestyles='dotted')


def add_currents(ax, df, which, east, north, compass=True, df1=None, df2=None, df3=None, tlims=None):
    '''Add current arrows to plot

    which   'water' or 'wind'
    '''
    color = 'k'  # color of data arrows

    # TCOON has too high frequency information to plot nicely
    if df is not None and (df.index[1] - df.index[0]).seconds/60. < 30:
        # want 30 min
        df = df.resample('30T').mean()  # was .asfreq()
    # if data is None, use model output (if model output not all None)
    if (df is None or east not in df.keys() or df[east].isnull().all()) and not all([dft is None for dft in [df1, df2, df3]]):
        # now model output saved into df
        df = pd.concat([df1, df2, df3], sort=False)  # in case there is a df3
        color = c2
    # this catches when TCOON data is temporarily unavailable and model output is not available
    if (df is None or east not in df.keys() or df[east].isnull().all()) and all([dft is None for dft in [df1, df2, df3]]):
        ax.text(0.1, 0.5, 'Wind data not available at this time.', transform=ax.transAxes)
        ax.get_yaxis().set_ticks([])
        return
    # if data is not within input time range, use model output instead
    if tlims is not None and (df1 is not None or df2 is not None or df3 is not None):
        if df['idx'][-1] < tlims[0] or df['idx'][0] > tlims[-1]:
            df = pd.concat([df1, df2, df3], sort=False)  # in case there is a df3
            color = c2

    # arrows with no heads for lines
    # http://stackoverflow.com/questions/37154071/python-quiver-plot-without-head
    # collect dataframes that are not None
    dfs = [dft for dft in [df, df1, df2, df3] if dft is not None and not dft.empty]
    tmin = min([min(dft.index) for dft in dfs])
    tmax = max([max(dft.index) for dft in dfs])
    dT = tmax - tmin
    if dT <= pd.Timedelta('2 days'):  # less than or equal to two days
        width = 1.0
        if which == 'wind':
            width /= 3
    elif dT <= pd.Timedelta('6 days'):  # less than or equal to 6 days
        width = 0.5
        if which == 'wind':
            width /= 3
    elif dT <= pd.Timedelta('9 days'):
        width = 0.4
        if which == 'wind':
            width /= 3
    elif dT <= pd.Timedelta('12 days'):
        width = 0.3
        if which == 'wind':
            width /= 3
    else:
        width = 0.2
        if which == 'wind':
            width /= 3
    # decimate temporally
    if dT < pd.Timedelta('150 days'):
        ddt = 1
    elif dT < pd.Timedelta('210 days'):
        ddt = 2
    elif dT < pd.Timedelta(str(11*30) + ' days'):
        ddt = 3
    elif dT < pd.Timedelta(str(15*30) + ' days'):
        ddt = 4
    else:
        ddt = 5

    # replace
    ax.quiver(df['idx'][::ddt], np.zeros(len(df[::ddt])), df[::ddt][east], df[::ddt][north], headaxislength=0,
              headlength=0, width=width, units='y', scale_units='y', scale=1, color=color)

    # use hindcast currents to fill in before data (in case there has been a gap)
    if tlims is not None:
        dfs = []; colors = []
        for dft, c in zip([df1, df2, df3], [c1, c2, c2]):
            if dft is not None and not dft.empty:
                dfs.append(dft); colors.append(c)
        # dfs = [dft for dft in [df1, df2, df3] if dft is not None and not dft.empty]
        # min and max datetime values for non-nan data
        idxmin = df.loc[(~df[east].isnull())]['idx'].min()
        idxmax = df.loc[(~df[east].isnull())]['idx'].max()
        # fill in before the data if more than an hour gap
        if (idxmin - tlims[0]) > 1./24:  # more than an hour
            plotmodel = True
            for dft, c in zip(dfs, colors):
                dft = dft.loc[(dft['idx'] > tlims[0]) & (dft['idx'] < idxmin - 0.5/24)]
                if plotmodel and not dft[east].isnull().all():  # only plot model in this area once
                    ax.quiver(dft['idx'][::ddt], np.zeros(len(dft[::ddt])), dft[::ddt][east], dft[::ddt][north], headaxislength=0,
                              headlength=0, width=width, units='y', scale_units='y', scale=1, color=c)
                    plotmodel = False
        # fill in after the data if more than an hour gap
        if (tlims[1] - idxmax) > 1./24:  # more than an hour
            plotmodel = True
            idxmaxsave = idxmax  # initialize max data value, might be updated
            for dft, c in zip(dfs, colors):
                dft = dft.loc[(dft['idx'] < tlims[1]) & (dft['idx'] > idxmaxsave + 0.5/24)]
                if plotmodel and not dft[east].isnull().all():  # only plot model in this area once
                    ax.quiver(dft['idx'][::ddt], np.zeros(len(dft[::ddt])),
                              dft[::ddt][east], dft[::ddt][north],
                              headaxislength=0, headlength=0, width=width,
                              units='y', scale_units='y', scale=1, color=c)
                    # plotmodel = False
                    # update max so that can plot multiple model output sources
                    idxmaxsave = max((dft.loc[(~dft[east].isnull())]['idx'].max(),idxmaxsave))

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


def add_vel(ax, df, buoy, which, ymaxrange=None, df1=None, df2=None, df3=None,
            label=None):
    '''Add along- or across-shelf velocity to plot

    which   'Across' or 'Along'
    '''

    if df is not None:
        ax.plot(df['idx'], df[which], 'k', lw=lw)
    if df1 is not None:
        ax.plot(df1['idx'], df1[which], color=c1, lw=lw)
    if df2 is not None:
        ax.plot(df2['idx'], df2[which], color=c2, lw=lw)
    if df3 is not None:
        ax.plot(df3['idx'], df3[which], color=c2, lw=lw, ls='--')
    # add line at zero for reference.
    add_zero(ax)
    # add r^2 to subplot
    add_r2(ax, df, [df1, df2, df3], which)
    # Enforce max limits for y axis in case data is very large or small
    if ymaxrange is not None:
        setymaxrange(ax, ymaxrange)
    # give some extra space along top and bottom of subplot
    shifty(ax, N=0.1)
    # force 0 line to be within y limits
    shifty(ax, N=0)
    if label is None:
        if which == 'Across [cm/s]':
            label = 'Cross-shelf flow\n' + r'$\left[ \mathrm{cm} \cdot \mathrm{s}^{-1} \right]$'
        elif which == 'Along [cm/s]':
            label = 'Along-shelf flow\n' + r'$\left[ \mathrm{cm} \cdot \mathrm{s}^{-1} \right]$'
    ax.set_ylabel(label)
    # convert to knots on rhs
    add_rhs(ax, '[knots]', 'cps2kts')
    if which == 'Across [cm/s]':
        ax.text(0.02, 0.9, 'OFFSHORE', fontsize=10, transform=ax.transAxes)
        ax.text(0.02, 0.03, 'ONSHORE', fontsize=10, transform=ax.transAxes)
        # add angle
        ax.text(0.9, 0.9, str(bys.loc[buoy,'angle']) + '˚T', fontsize=10, transform=ax.transAxes)
    elif which == 'Along [cm/s]':
        ax.text(0.02, 0.9, 'UPCOAST (to LA)', fontsize=10, transform=ax.transAxes)
        ax.text(0.02, 0.03, 'DOWNCOAST (to MX)', fontsize=10, transform=ax.transAxes)
        # add angle
        ax.text(0.9, 0.9, str(bys.loc[buoy,'angle']-90) + '˚T', fontsize=10, transform=ax.transAxes)


def add_var_2units(ax1, df, key, label1, con, label2, ymaxrange=None, df1=None,
                   df2=None, df3=None, df4=None, tlims=None, dolegend=False,
                   add0=False, doebbflood=False, dodepth=False, dodepthm=np.nan,
                   doangle=False, dodistance=False):
    '''Plot with units on both left and right sides of plot.

    dodepth should be a depth in meters if you want to write on the sensor depth.
    use dodepthm for adding model depth, if relevant.'''

    if df is not None and not df[key].isnull().all():
        ax1.plot(df['idx'], df[key], lw=lw, color='k', linestyle='-')
    # this catches when TCOON data is temporarily unavailable and model output is not available
    if (df is None or key not in df.keys() or df[key].isnull().all()) \
         and all([dft is None for dft in [df1, df2, df3, df4]]):
        ax1.text(0.1, 0.5, label1.replace('\n','').split('[')[0].split('$')[0] + ' data not available at this time.', transform=ax1.transAxes)
        ax1.get_yaxis().set_ticks([])
        return
    if df1 is not None:
        ax1.plot(df1['idx'], df1[key], lw=lw, color=c1, linestyle='-')
    if df2 is not None:
        ax1.plot(df2['idx'], df2[key], lw=lw, color=c2, linestyle='-')
    if df3 is not None:
        ax1.plot(df3['idx'], df3[key], lw=lw, color=c2, linestyle='--')
    if df4 is not None:
        ax1.plot(df4['idx'], df4[key], lw=lw, color=c3, linestyle='-')
    ax1.set_ylabel(label1)
    ax1.get_yaxis().get_major_formatter().set_useOffset(False)  # no shift for pressure
    # set y range by signal within tlims (in case data off-screen changing it)
    setylimsintlims(ax1, df, [df1, df2, df3, df4], key, tlims)
    if ymaxrange is not None:  # Have max limits for y axis
        setymaxrange(ax1, ymaxrange)
    shifty(ax1, N=0.07)
    # add r^2 to subplot
    add_r2(ax1, df, [df1, df2, df3, df4], key, N=0.1)
    # add data/model legend
    if dolegend:
        add_legend(ax1, df, df1, df2, df3, tlims, df4=df4)
    # add line at 0
    if add0:
        add_zero(ax1)
    # right side units
    add_rhs(ax1, label2, con)
    # Add ebb/flood text labels
    if doebbflood:
        ax1.text(0.02, 0.95, 'FLOOD', fontsize=10, transform=ax1.transAxes)
        ax1.text(0.02, 0.015, 'EBB', fontsize=10, transform=ax1.transAxes)
    if not doangle == False:  # add rotation angle onto plot
        ax1.text(0.9, 0.95, str(doangle) + '˚T', fontsize=10, transform=ax1.transAxes)
    if not dodistance == False:  # add distance from pier onto plot
        ax1.text(0.225, 0.95, 'Distance from pier: %2.1fm' % dodistance, color='k', fontsize=10, transform=ax1.transAxes)
    if not dodepth == False:  # data
        ax1.text(0.55, 0.95, 'Depth: %2.1fm' % dodepth, color='k', fontsize=10, transform=ax1.transAxes)
    if not np.isnan(dodepthm):  # model
        ax1.text(0.725, 0.95, 'Depth: %2.1fm' % dodepthm, color=c3, fontsize=10, transform=ax1.transAxes)

def add_var(ax, df, var, varlabel, ymaxrange=None, df1=None, df2=None, df3=None,
            dolegend=False, tlims=None):
    '''Add basic var to plot as line plot with no extra space.'''

    # this catches when data is temporarily unavailable and model output is not available
    if (df is None or var not in df.keys() or df[var].isnull().all()) \
         and all([dft is None for dft in [df1, df2, df3]]):
        ax.text(0.1, 0.5, varlabel.replace('\n','').split('[')[0].split('$')[0] + ' data not available at this time.', transform=ax.transAxes)
        ax.get_yaxis().set_ticks([])
        return
    if df is not None and not df[var].isnull().all():
        ax.plot(df['idx'], df[var], lw=lw, color='k', linestyle='-')
    if df1 is not None:
        ax.plot(df1['idx'], df1[var], lw=lw, color=c1, linestyle='-')
    if df2 is not None:
        ax.plot(df2['idx'], df2[var], lw=lw, color=c2, linestyle='-')
    if df3 is not None:
        ax.plot(df3['idx'], df3[var], lw=lw, color=c2, linestyle='--')
    ax.set_ylabel(varlabel)
    ax.get_yaxis().get_major_formatter().set_useOffset(False)  # no shift for y limits
    # set y range by signal within tlims (in case data off-screen changing it)
    setylimsintlims(ax, df, [df1, df2, df3], var, tlims)
    if ymaxrange is not None:  # Have max limits for y axis
        setymaxrange(ax, ymaxrange)
    shifty(ax)
    # add r^2 to subplot
    add_r2(ax, df, [df1, df2, df3], var)
    # add data/model legend
    if dolegend:
        add_legend(ax, df, df1, df2, df3, tlims)


def add_2var(ax1, df, var1, label1, var2, label2, ymaxrange=None,
             df1=None, df2=None, df3=None,
             tlims=None, sameylim=False, dolegend=False,
             cc1='#559349', cc2='#874993'):
    '''2 variables, one on each y axis. same y limits if set True.

    df1, df2, df3 are all for left side y axis.
    Default colors are green and purple be accept inputs instead.
    '''

    # 1st var
    ax1.plot(df['idx'], df[var1], lw=lw, color=cc1, linestyle='-')
    if df1 is not None:
        ax1.plot(df1['idx'], df1[var1], lw=lw, color=c1, linestyle='-')
    if df2 is not None:
        ax1.plot(df2['idx'], df2[var1], lw=lw, color=c2, linestyle='-')
    if df3 is not None:
        ax1.plot(df3['idx'], df3[var1], lw=lw, color=c2, linestyle='--')
    ax1.set_ylabel(label1, color=cc1)
    ax1.tick_params(axis='y', colors=cc1)
    if ymaxrange is not None:  # Have max limits for y axis
        setymaxrange(ax1, ymaxrange)
    # add r^2 to subplot
    add_r2(ax1, df, [df1, df2, df3], var1)
    # 2nd var
    ax2 = ax1.twinx()
    ax2.plot(df['idx'], df[var2], lw=lw, color=cc2, linestyle='--')
    ax2.set_ylabel(label2, color=cc2)
    ax2.tick_params(axis='y', colors=cc2)
    if ymaxrange is not None:  # Have max limits for y axis
        setymaxrange(ax2, ymaxrange)
    # set y range by signal within tlims (in case data off-screen changing it)
    setylimsintlims(ax1, df, [df1, df2, df3], var1, tlims)
    if sameylim:
        ylim = ax1.get_ylim()
        ax2.set_ylim(ylim[0], ylim[1])
    shifty(ax1)
    shifty(ax2)
    # add data/model legend
    if dolegend:
        add_legend(ax1, df, df1, df2, df3, tlims)


def add_2var_sameplot(ax, df, var1, label1, var2, ymaxrange=None):
    '''2 variables on same y axis.'''

    if var1 in df.keys():
        ax.plot(df['idx'], df[var1], lw=lw, color='k', linestyle='-')
    if var2 in df.keys():
        ax.plot(df['idx'], df[var2], lw=lw, color='k', linestyle='--')

    if (var1 not in df.keys() and var2 not in df.keys()) or (df[var1].isnull().sum() == len(df) and df[var2].isnull().sum() == len(df)):
        ax.text(0.1, 0.5, label1.replace('\n','').split('[')[0].split('$')[0] + ' data not available at this time.', transform=ax.transAxes)
        ax.get_yaxis().set_ticks([])
        return
    ax.set_ylabel(label1, color='k')
    if ymaxrange is not None:  # Have max limits for y axis
        setymaxrange(ax, ymaxrange)
    shifty(ax)

def majorformatter(date, y):
    date = num2date(date)
    if date.hour == 0:  # use full date for start of day
        return date.strftime('%b %d, %H:%M')
    else:  # return only time
        return date.strftime('%H:%M')
def majorformatter_only0hour(date, y):
    date = num2date(date)
    if date.hour == 0:  # use full date for start of day
        return date.strftime('%b %d, %H:%M')
    else:  # return only time
        return ''

def add_xlabels(ax, df, fig, tlims=None):
    '''Add date labels to bottom x axis'''

    # tighten only x axis
    if tlims is not None:
        ax.set_xlim(tlims[0], tlims[1])
    else:
        ax.autoscale(enable=True, axis='x', tight=True)

    # use this because includes forecast model output along with data
    xlim = np.diff(ax.get_xlim())  # x limit length in days

    # varied tick locations and labels for few days
    if xlim <=1:  # less than or equal to one day
        # hourly minor ticks
        hours = mpl.dates.HourLocator()
        ax.xaxis.set_minor_locator(hours)
        sixthdays = mpl.dates.HourLocator(byhour=np.arange(0,24,4))
        ax.xaxis.set_major_locator(sixthdays)
        ax.xaxis.set_major_formatter(mpl.ticker.FuncFormatter(majorformatter))
        if df.index[0].year != df.index[-1].year:
            ax.text(0.98, -0.05, df.index.strftime("%Y")[0] + '-' + df.index.strftime("%Y")[-1],
                    transform=ax.transAxes, rotation=30)
        else:
            ax.text(0.98, -0.15, df.index.strftime("%Y")[-1],
                    transform=ax.transAxes, rotation=30)
    elif xlim <=2:  # less than or equal to two days
        # hourly minor ticks
        hours = mpl.dates.HourLocator()
        ax.xaxis.set_minor_locator(hours)
        quarterdays = mpl.dates.HourLocator(byhour=np.arange(0,24,6))
        ax.xaxis.set_major_locator(quarterdays)
        ax.xaxis.set_major_formatter(mpl.ticker.FuncFormatter(majorformatter))
        if df.index[0].year != df.index[-1].year:
            ax.text(0.98, -0.05, df.index.strftime("%Y")[0] + '-' + df.index.strftime("%Y")[-1],
                    transform=ax.transAxes, rotation=30)
        else:
            ax.text(0.98, -0.15, df.index.strftime("%Y")[-1],
                    transform=ax.transAxes, rotation=30)
    elif xlim <=3:
        hours = mpl.dates.HourLocator(byhour=np.arange(0,24,2))
        ax.xaxis.set_minor_locator(hours)
        halfdays = mpl.dates.HourLocator(byhour=np.arange(0,24,8))
        ax.xaxis.set_major_locator(halfdays)
        ax.xaxis.set_major_formatter(mpl.ticker.FuncFormatter(majorformatter))
        if df.index[0].year != df.index[-1].year:
            ax.text(0.98, -0.05, df.index.strftime("%Y")[0] + '-' + df.index.strftime("%Y")[-1],
                    transform=ax.transAxes, rotation=30)
        else:
            ax.text(0.98, -0.15, df.index.strftime("%Y")[-1],
                    transform=ax.transAxes, rotation=30)
    elif xlim <=4:
        hours = mpl.dates.HourLocator(byhour=np.arange(0,24,3))
        ax.xaxis.set_minor_locator(hours)
        halfdays = mpl.dates.HourLocator(byhour=np.arange(0,24,12))
        ax.xaxis.set_major_locator(halfdays)
        ax.xaxis.set_major_formatter(mpl.ticker.FuncFormatter(majorformatter))
        if df.index[0].year != df.index[-1].year:
            ax.text(0.98, -0.05, df.index.strftime("%Y")[0] + '-' + df.index.strftime("%Y")[-1],
                    transform=ax.transAxes, rotation=30)
        else:
            ax.text(0.98, -0.15, df.index.strftime("%Y")[-1],
                    transform=ax.transAxes, rotation=30)
    elif xlim <=5:
        minor = mpl.dates.HourLocator(byhour=np.arange(0,24,4))
        ax.xaxis.set_minor_locator(minor)
        major = mpl.dates.HourLocator(byhour=np.arange(0,24,12))
        ax.xaxis.set_major_locator(major)
        ax.xaxis.set_major_formatter(mpl.ticker.FuncFormatter(majorformatter_only0hour))
        if df.index[0].year != df.index[-1].year:
            ax.text(0.98, -0.05, df.index.strftime("%Y")[0] + '-' + df.index.strftime("%Y")[-1],
                    transform=ax.transAxes, rotation=30)
        else:
            ax.text(0.98, -0.15, df.index.strftime("%Y")[-1],
                    transform=ax.transAxes, rotation=30)
    elif xlim <=8:
        minor = mpl.dates.HourLocator(byhour=np.arange(0,24,6))
        ax.xaxis.set_minor_locator(minor)
        major = mpl.dates.HourLocator(byhour=np.arange(0,24,24))
        ax.xaxis.set_major_locator(major)
        ax.xaxis.set_major_formatter(mpl.dates.DateFormatter('%b %d'))
        if df.index[0].year != df.index[-1].year:
            ax.text(0.98, -0.05, df.index.strftime("%Y")[0] + '-' + df.index.strftime("%Y")[-1],
                    transform=ax.transAxes, rotation=30)
        else:
            ax.text(0.98, -0.15, df.index.strftime("%Y")[-1],
                    transform=ax.transAxes, rotation=30)
    elif xlim <=10:
        minor = mpl.dates.HourLocator(byhour=np.arange(0,24,12))
        ax.xaxis.set_minor_locator(minor)
        major = mpl.dates.HourLocator(byhour=np.arange(0,24,24))
        ax.xaxis.set_major_locator(major)
        ax.xaxis.set_major_formatter(mpl.dates.DateFormatter('%b %d'))
        if df.index[0].year != df.index[-1].year:
            ax.text(0.98, -0.05, df.index.strftime("%Y")[0] + '-' + df.index.strftime("%Y")[-1],
                    transform=ax.transAxes, rotation=30)
        else:
            ax.text(0.98, -0.15, df.index.strftime("%Y")[-1],
                    transform=ax.transAxes, rotation=30)
    elif xlim <=20:  # less than or equal to 20 days
        # 12 hourly minor ticks
        minor = mpl.dates.HourLocator(byhour=np.arange(0,24,12))
        ax.xaxis.set_minor_locator(minor)
        major = mpl.dates.HourLocator(byhour=np.arange(0,24,24))
        ax.xaxis.set_major_locator(major)
        ax.xaxis.set_major_formatter(mpl.dates.DateFormatter('%b %d'))
        # turn off every other tick label but will still get grid lines
        # at all major ticks
        plt.setp(ax.get_xticklabels()[1::2], visible=False)
        if df.index[0].year != df.index[-1].year:
            ax.text(0.98, -0.05, df.index.strftime("%Y")[0] + '-' + df.index.strftime("%Y")[-1],
                    transform=ax.transAxes, rotation=30)
        else:
            ax.text(0.98, -0.15, df.index.strftime("%Y")[-1],
                    transform=ax.transAxes, rotation=30)
    elif xlim <= 80:
        # daily minor ticks
        minor = mpl.dates.DayLocator(bymonthday=range(1,32))
        ax.xaxis.set_minor_locator(minor)
        # weekly major ticks
        major = mpl.dates.DayLocator(interval=7)
        ax.xaxis.set_major_locator(major)
        ax.xaxis.set_major_formatter(mpl.dates.DateFormatter('%b %d'))
        if df.index[0].year != df.index[-1].year:
            ax.text(0.98, -0.05, df.index.strftime("%Y")[0] + '-' + df.index.strftime("%Y")[-1],
                    transform=ax.transAxes, rotation=30)
        else:
            ax.text(0.98, -0.15, df.index.strftime("%Y")[-1],
                    transform=ax.transAxes, rotation=30)
    elif xlim <= 90:
        # weekly major ticks
        major = mpl.dates.DayLocator(interval=7)
        ax.xaxis.set_major_locator(major)
        ax.xaxis.set_major_formatter(mpl.dates.DateFormatter('%b %d'))
        if df.index[0].year != df.index[-1].year:
            ax.text(0.98, -0.05, df.index.strftime("%Y")[0] + '-' + df.index.strftime("%Y")[-1],
                    transform=ax.transAxes, rotation=30)
        else:
            ax.text(0.98, -0.15, df.index.strftime("%Y")[-1],
                    transform=ax.transAxes, rotation=30)
    elif xlim < 6*30:  # less than 8 months
        # weekly minor ticks
        minor = mpl.dates.DayLocator(interval=7)
        ax.xaxis.set_minor_locator(minor)
        major = mpl.dates.DayLocator(interval=14)
        ax.xaxis.set_major_locator(major)
        ax.xaxis.set_major_formatter(mpl.dates.DateFormatter('%b %d'))
        if df.index[0].year != df.index[-1].year:
            ax.text(0.98, -0.05, df.index.strftime("%Y")[0] + '-' + df.index.strftime("%Y")[-1],
                    transform=ax.transAxes, rotation=30)
        else:
            ax.text(0.98, -0.15, df.index.strftime("%Y")[-1],
                    transform=ax.transAxes, rotation=30)
    elif xlim < 366:  # less than 12 months
        # weekly minor ticks
        minor = mpl.dates.MonthLocator(interval=1, bymonthday=15)
        ax.xaxis.set_minor_locator(minor)
        major = mpl.dates.MonthLocator(interval=1, bymonthday=1)
        ax.xaxis.set_major_locator(major)
        ax.xaxis.set_major_formatter(mpl.dates.DateFormatter('%b %d'))
        if df.index[0].year != df.index[-1].year:
            ax.text(0.98, -0.05, df.index.strftime("%Y")[0] + '-' + df.index.strftime("%Y")[-1],
                    transform=ax.transAxes, rotation=30)
        else:
            ax.text(0.98, -0.15, df.index.strftime("%Y")[-1],
                    transform=ax.transAxes, rotation=30)
    else:
        ax.xaxis.set_major_formatter(mpl.dates.DateFormatter('%b %d, %Y'))

    # this gives number of rows or subplots since always one column
    nsubplots = fig.get_axes()[0].numRows
    if nsubplots == 1:
        textlocUTC = 1.03, -0.25
        textloc1 = 0.95, 0.06
        textloc2 = 0.08, 0.075
    elif nsubplots == 2:
        textlocUTC = 1.03, -0.3
        textloc1 = 0.95, 0.035
        textloc2 = 0.08, 0.045
    elif nsubplots == 4:
        textlocUTC = 1.03, -0.35
        textloc1 = 0.95, 0.025
        textloc2 = 0.08, 0.035
    elif nsubplots == 6:
        textlocUTC = 1.03, -0.45
        textloc1 = 0.95, 0.025
        textloc2 = 0.08, 0.035
    else:
        textlocUTC = 1.03, -0.35
        textloc1 = 0.95, 0.025
        textloc2 = 0.08, 0.035

    # put in GMT as time zone
    # import pdb; pdb.set_trace()
    if df.index.tzinfo.zone == 'UTC':
        ax.text(*textlocUTC, 'UTC', transform=ax.transAxes, fontsize=10)
    elif df.index.tzinfo.zone == 'US/Central':
        ax.text(*textlocUTC, 'CST/CDT', transform=ax.transAxes, fontsize=10)
    elif df.index.tzinfo.zone == 'Etc/GMT+6':
        ax.text(*textlocUTC, 'CST', transform=ax.transAxes, fontsize=10)

    # rotates and right aligns the x labels
    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')

    # text at bottom
    # right hand side
    text = 'Oceanography and GERG at Texas A&M University\n' \
           + datetime.utcnow().strftime('%a %b %d, %Y %H:%M UTC')
    fig.text(*textloc1, text, fontsize=8, transform=fig.transFigure,
             horizontalalignment='right', verticalalignment='top')
    # left hand side
    text = '''TGLO, GERG, Oceanography, and Texas A&M make no representations
or any other warranty with regard to this data
These data are not suitable for navigation purposes.'''
    fig.text(*textloc2, text, fontsize=8, transform=fig.transFigure,
             horizontalalignment='left', verticalalignment='top')


def setup(nsubplots, table=None, buoy=None, title=True):
    '''Set up plot'''

    if nsubplots == 1:
        figsize = (8.5, 5)
        props = {'top': 0.88, 'right': 0.9, 'left': 0.15, 'hspace': 0.1, 'bottom': 0.275}
    elif nsubplots == 2:
        figsize = (8.5, 8.5)
        props = {'top': 0.93, 'right': 0.88, 'left': 0.12, 'hspace': 0.08, 'bottom': 0.175}
    else:
        figsize = (8.5, 11)
        if len(buoy) == 1:  # don't need as much space at top for TABS buoys
            props = {'top': 0.96, 'right': 0.88, 'left': 0.15, 'hspace': 0.1, 'bottom': 0.125}
        else:
            props = {'top': 0.94, 'right': 0.88, 'left': 0.15, 'hspace': 0.1, 'bottom': 0.125}

    # plot
    fig, axes = plt.subplots(nsubplots, 1, figsize=figsize, sharex=True)
    if not isinstance(axes, np.ndarray):
        axes = [axes]  # change to list when 1 subplot to be consistent with others
    # bottom controlled later
    fig.subplots_adjust(**props)
    # title
    if title:
        if buoy is not None:
            lat = tools.dd2dm(bys.loc[buoy,'lat'])
            lon = tools.dd2dm(bys.loc[buoy,'lon'])
            ll = str(lat[0]) + r'$\!^\circ$' + str(lat[1]) + '\'N' + '  ' \
                    + str(abs(lon[0])) + r'$\!^\circ$' + str(lon[1]) + '\'W'
            if len(buoy) == 1:
                prefix = 'TABS Buoy'
            elif len(buoy) == 5:  # NDBC
                prefix = 'NDBC Station'
            elif 'tcoon' in table:
                prefix = 'TCOON Station'
            elif 'nos' in table:
                prefix = 'NOS Station'
            elif 'ports' in table:
                prefix = 'PORTS Station'

            title = '%s %s' % (prefix, buoy)
            # add other name for buoy if exists
            if isinstance(bys.loc[buoy,'alias'], str):
                title += '/%s' % bys.loc[buoy,'alias']
            title += ': %s' % ll  # add on lat/lon
            # add description of buoy location if exists
            if isinstance(bys.loc[buoy,'description'], str):
                title += '\n%s' % bys.loc[buoy,'description']

            # title = '%s %s: %s\n%s, %s' % \
            #         (prefix, buoy, ll, bys.loc[buoy,'alias'], bys.loc[buoy,'description'])
            axes[0].set_title(title, fontsize=18)

    return fig, axes


def plot(df, buoy, which=None, df1=None, df2=None, df3=None, df4=None, tlims=None):
    '''Plot data.

    Find data in dataname and save fig, both in /tmp.
    Optional df1 (hindcast), df2 (nowcast), df3 (forecast). If given, also plot on each axis.
    '''

    if which is None:  # can read in table if not tabs buoy
        which = bys.loc[buoy,'table1']

    if which in ['tcoon-tide', 'ports']:
        if buoy == 'cc0101':
            nsubplots = 3
        else:
            nsubplots = 1
    elif which in ['nos-water']:
        nsubplots = 2
    elif which in ['salt', 'wave', 'nos-met', 'ndbc-met']:
        nsubplots = 3
    elif which in ['ven', 'eng', 'met', 'ndbc-nowave']:
        nsubplots = 4
    elif which in ['tcoon', 'nos']:
        nsubplots = 5
    elif which in ['ndbc', 'nos-cond', 'sum']:
        nsubplots = 6

    if len(buoy) == 1 and which != 'wave' and df is not None:
        # for TABS buoys
        # fill in missing data at 30 min frequency as nans so not plotted
        # if df is not None:
        # interpolate to 30 min for TABS so that small gaps are filled
        # only 1 time point will be interpolated into
        df = df.resample('30T').interpolate(method='time', limit=1)
            # df = df.resample('30T').asfreq()
    elif which == 'wave':  # TABS
        # accounting for known issue for interpolation after sampling if indices changes
        # https://github.com/pandas-dev/pandas/issues/14297
        # first obtain the desired new index
        newindex = df.resample('1H', base=0).asfreq().index
        # interpolate on union of old and new index
        # use limit=1 so that only one row of nan is filled in
        df_union = df.reindex(df.index.union(newindex)).interpolate(method='time', limit=1)
        # reindex to the new index
        df2 = df_union.reindex(newindex)

    elif 'ndbc' in which and df is not None and 'Wave Ht [m]' in df.keys() and not df['Wave Ht [m]'].isnull().all():  # NDBC with wave
        # fill in missing data with nan's so not plotted across.
        base = 50
        df = df.resample('60 T', base=base).interpolate(method='time', limit=1)

    # set up datetime number indices since quiver doesn't work otherwise
    for dft in [df, df1, df2, df3, df4]:
        if dft is not None:
            # have to implement timezone to get shift into idx
            dft.insert(0, 'idx', date2num(dft.index.tz_localize(None).to_pydatetime()))

    # change length of df2 if df1 overlaps with it to prioritize df1
    if df1 is not None and df2 is not None and (df1.size>0) and (df2.size>0):
        if df1.index[-1] > df2.index[0]:
            stemp = df1.index[-1] + pd.Timedelta('10 minutes')
            df2 = df2[stemp:]

    # change length of df3 if df2 overlaps with it to prioritize df2
    if df2 is not None and df3 is not None and (df2.size>0) and (df3.size>0):
        if df2.index[-1] > df3.index[0]:
            stemp = df2.index[-1] + pd.Timedelta('10 minutes')
            df3 = df3[stemp:]

    fig, axes = setup(nsubplots=nsubplots, table=which, buoy=buoy)

    if which == 'ven':
        add_currents(axes[0], df, 'water', 'East [cm/s]', 'North [cm/s]',
                     df1=df1, df2=df2, df3=df3, tlims=tlims)
        add_vel(axes[1], df, buoy, 'Across [cm/s]', ymaxrange=[-110, 110],
                df1=df1, df2=df2, df3=df3)
        add_vel(axes[2], df, buoy, 'Along [cm/s]', ymaxrange=[-110, 110],
                df1=df1, df2=df2, df3=df3)
        add_var_2units(axes[3], df, 'WaterT [deg C]',
                       'Water temperature\n' + r'$\left[\!^\circ\! \mathrm{C} \right]$',
                       'c2f', r'$\left[\!^\circ\! \mathrm{F} \right]$',
                       ymaxrange=[5, 32], df1=df1, df2=df2, df3=df3,
                       tlims=tlims, dolegend=True)

    elif which == 'eng':
        add_2var_sameplot(axes[0], df, 'VBatt [Oper]', 'V$_\mathrm{batt}$',
                          'VBatt [sleep]', ymaxrange=[0, 15])
        add_var(axes[1], df, 'SigStr [dB]', 'Sig Str [dB]', ymaxrange=[-25, 0],
                tlims=tlims)
        add_var(axes[2], df, 'Nping', 'Ping Cnt', ymaxrange=[30, 210], tlims=tlims)
        add_2var(axes[3], df, 'Tx', 'Tx', 'Ty', 'Ty [--]', ymaxrange=[-20, 20])

    elif which == 'met':
        add_currents(axes[0], df, 'wind', 'East [m/s]', 'North [m/s]', df1=df1,
                     df2=df2, df3=df3, tlims=tlims)
        add_var_2units(axes[1], df, 'AirT [deg C]',
                       'Air temperature ' + r'$\left[\!^\circ\! \mathrm{C} \right]$',
                       'c2f', r'$\left[\!^\circ\! \mathrm{F} \right]$',
                        ymaxrange=[-25,40], df1=df1, df2=df2,
                       df3=df3, tlims=tlims)
        add_var_2units(axes[2], df, 'AtmPr [mb]', 'Atmospheric pressure\n[mb]',
                       'mb2hg', '[inHg]', ymaxrange=[1000,1060], df1=df1,
                       df2=df2, df3=df3, tlims=tlims)
        add_var(axes[3], df, 'RelH [%]', 'Relative Humidity [%]',
                ymaxrange=[0,110], df1=df1, df2=df2, df3=df3, dolegend=True, tlims=tlims)

    elif which == 'salt':
        add_var_2units(axes[0], df, 'WaterT [deg C]',
                       'Water temperature\n' + r'$\left[\!^\circ\! \mathrm{C} \right]$',
                       'c2f', r'$\left[\!^\circ\! \mathrm{F} \right]$',
                       ymaxrange=[5, 32], df1=df1, df2=df2, df3=df3,
                       tlims=tlims)
        add_var(axes[1], df, 'Salinity', 'Salinity', ymaxrange=[12, 37], df1=df1,
                df2=df2, df3=df3, tlims=tlims)
        # add_var(axes[2], df, 'Cond [ms/cm]', 'Conductivity [ms/cm]', ymaxrange=[3, 60])
        add_var(axes[2], df, 'Density [kg/m^3]',
                'Density ' + r'$\left[ \mathrm{kg} \cdot \mathrm{m}^{-3} \right]$',
                df1=df1, df2=df2, df3=df3, ymaxrange=[1005, 1036], dolegend=True, tlims=tlims)

    elif which == 'sum':
        add_currents(axes[0], df, 'water', 'East [cm/s]', 'North [cm/s]',
                     df1=df1, df2=df2, df3=df3, tlims=tlims)
        add_vel(axes[1], df, buoy, 'Across [cm/s]', ymaxrange=[-110, 110],
                df1=df1, df2=df2, df3=df3,
                label='Cross-shelf\nflow ' + r'$\left[ \mathrm{cm} \cdot \mathrm{s}^{-1} \right]$')
        add_vel(axes[2], df, buoy, 'Along [cm/s]', ymaxrange=[-110, 110],
                df1=df1, df2=df2, df3=df3,
                label='Along-shelf\nflow ' + r'$\left[ \mathrm{cm} \cdot \mathrm{s}^{-1} \right]$')
        add_var_2units(axes[3], df, 'WaterT [deg C]',
                       'Water\ntemp ' + r'$\left[\!^\circ\! \mathrm{C} \right]$',
                       'c2f', r'$\left[\!^\circ\! \mathrm{F} \right]$',
                       ymaxrange=[5, 32], df1=df1, df2=df2, df3=df3,
                       tlims=tlims, dolegend=True)
        add_var(axes[4], df, 'Salinity', 'Salinity', ymaxrange=[12, 37], df1=df1,
                df2=df2, df3=df3, tlims=tlims)
        add_currents(axes[5], df, 'wind', 'East [m/s]', 'North [m/s]', df1=df1,
                     df2=df2, df3=df3, tlims=tlims)

    elif which == 'wave':
        add_var_2units(axes[0], df, 'WaveHeight [m]', 'Wave Height [m]',
                       'm2ft', '[ft]', ymaxrange=[0,5], tlims=tlims)
        add_var(axes[1], df, 'MeanPeriod [s]', 'Mean Period [s]', tlims=tlims)
        add_var(axes[2], df, 'PeakPeriod [s]', 'Peak Period [s]', ymaxrange=[2,12], tlims=tlims)

    elif which == 'ndbc':
        add_currents(axes[0], df, 'wind', 'East [m/s]', 'North [m/s]', df1=df1,
                     df2=df2, df3=df3, tlims=tlims)
        add_var_2units(axes[1], df, 'AtmPr [mb]', 'Atmospheric\npressure [mb]',
                       'mb2hg', '[inHg]', ymaxrange=[1000,1060], df1=df1,
                       df2=df2, df3=df3, tlims=tlims)
        add_var_2units(axes[2], df, 'AirT [deg C]',
                       'Air temp ' + r'$\left[\!^\circ\! \mathrm{C} \right]$',
                       'c2f', r'$\left[\!^\circ\! \mathrm{F} \right]$',
                        ymaxrange=[-25,40], df1=df1, df2=df2,
                       df3=df3, tlims=tlims)
        add_var_2units(axes[3], df, 'Wave Ht [m]', 'Wave height\n[m]',
                       'm2ft', '[ft]', ymaxrange=[0,5], tlims=tlims)
        add_var(axes[4], df, 'Wave Pd [s]', 'Wave period\n[s]', ymaxrange=[0,12], tlims=tlims)
        add_var_2units(axes[5], df, 'WaterT [deg C]',
                       'Water\ntemperature ' + r'$\left[\!^\circ\! \mathrm{C} \right]$',
                       'c2f', r'$\left[\!^\circ\! \mathrm{F} \right]$',
                       ymaxrange=[5, 32], df1=df1, df2=df2, df3=df3,
                       tlims=tlims, dolegend=True)

    elif which == 'ndbc-nowave':
        add_currents(axes[0], df, 'wind', 'East [m/s]', 'North [m/s]', df1=df1,
                     df2=df2, df3=df3, tlims=tlims)
        add_var_2units(axes[1], df, 'AtmPr [mb]', 'Atmospheric pressure\n[mb]',
                       'mb2hg', '[inHg]', ymaxrange=[1000,1060], df1=df1,
                       df2=df2, df3=df3, tlims=tlims)
        add_var_2units(axes[2], df, 'AirT [deg C]',
                       'Air temp ' + r'$\left[\!^\circ\! \mathrm{C} \right]$',
                       'c2f', r'$\left[\!^\circ\! \mathrm{F} \right]$',
                        ymaxrange=[-25,40], df1=df1, df2=df2,
                       df3=df3, tlims=tlims)
        add_var_2units(axes[3], df, 'WaterT [deg C]',
                       'Water temperature\n' + r'$\left[\!^\circ\! \mathrm{C} \right]$',
                       'c2f', r'$\left[\!^\circ\! \mathrm{F} \right]$',
                       ymaxrange=[5, 32], df1=df1, df2=df2, df3=df3,
                       tlims=tlims, dolegend=True)

    elif which in ['ndbc-met', 'nos-met']:
        add_currents(axes[0], df, 'wind', 'East [m/s]', 'North [m/s]', df1=df1,
                     df2=df2, df3=df3, tlims=tlims)
        add_var_2units(axes[1], df, 'AtmPr [mb]', 'Atmospheric pressure\n[mb]',
                       'mb2hg', '[inHg]', ymaxrange=[1000,1060], df1=df1,
                       df2=df2, df3=df3, tlims=tlims)
        add_var_2units(axes[2], df, 'AirT [deg C]',
                       'Air temp ' + r'$\left[\!^\circ\! \mathrm{C} \right]$',
                       'c2f', r'$\left[\!^\circ\! \mathrm{F} \right]$',
                        ymaxrange=[-25,40], df1=df1, df2=df2,
                       df3=df3, dolegend=True, tlims=tlims)

    elif which == 'tcoon-tide':
        # will be something like 'Water Level [m, MSL]'
        sshcol = [col for col in df.columns if 'Water Level' in col][0]
        sshlabel = sshcol[:11] + '\n' + sshcol[12:]  # adds line break
        add_var_2units(axes[0], df, sshcol, sshlabel,
                       'm2ft', '[ft]', ymaxrange=[-3,3], tlims=tlims, dolegend=True)

    elif which == 'tcoon' or which == 'nos':
        add_currents(axes[0], df, 'wind', 'East [m/s]', 'North [m/s]', df1=df1,
                     df2=df2, df3=df3, tlims=tlims)
        add_var_2units(axes[1], df, 'AtmPr [mb]', 'Atmospheric pressure\n[mb]',
                       'mb2hg', '[inHg]', ymaxrange=[1000,1060], df1=df1,
                       df2=df2, df3=df3, tlims=tlims)
        add_var_2units(axes[2], df, 'AirT [deg C]',
                       'Air temp ' + r'$\left[\!^\circ\! \mathrm{C} \right]$',
                       'c2f', r'$\left[\!^\circ\! \mathrm{F} \right]$',
                        ymaxrange=[-25,40], df1=df1, df2=df2,
                       df3=df3, tlims=tlims)
        # df4 is an optional input containing NOAA tidal height prediction
        if df4 is not None:  # only show legend here if needed
            dolegend = True
        else:
            dolegend = False
        # have code here to catch if variable/data is not available
        if (df is None) and (df4 is None):
            axes[3].text(0.1, 0.5, 'Water level data not available at this time.', transform=axes[3].transAxes)
            axes[3].get_yaxis().set_ticks([])
        else:
            # will be something like 'Water Level [m, MSL]'
            sshcol = [col for col in df.columns if 'Water Level' in col][0]
            sshlabel = sshcol[:11] + '\n' + sshcol[12:]  # adds line break
            add_var_2units(axes[3], df, sshcol, sshlabel,
                           'm2ft', '[ft]', ymaxrange=[-3,3], tlims=tlims, df4=df4,
                           dolegend=dolegend)
        add_var_2units(axes[4], df, 'WaterT [deg C]',
                       'Water temp\n' + r'$\left[\!^\circ\! \mathrm{C} \right]$',
                       'c2f', r'$\left[\!^\circ\! \mathrm{F} \right]$',
                       ymaxrange=[5, 32], df1=df1, df2=df2, df3=df3,
                       tlims=tlims, dolegend=True)

    elif which == 'nos-water':
        if df4 is None:  # legend for NOAA model
            dolegend = False
        else:
            dolegend = True
        # df4 is an optional input containing NOAA tidal height prediction
        # will be something like 'Water Level [m, MSL]'
        sshcol = [col for col in df.columns if 'Water Level' in col][0]
        sshlabel = sshcol[:11] + '\n' + sshcol[12:]  # adds line break
        add_var_2units(axes[0], df, sshcol, sshlabel,
                       'm2ft', '[ft]', ymaxrange=[-3,3], tlims=tlims, df4=df4,
                       dolegend=dolegend)
        add_var_2units(axes[1], df, 'WaterT [deg C]',
                       'Water temp ' + r'$\left[\!^\circ\! \mathrm{C} \right]$',
                       'c2f', r'$\left[\!^\circ\! \mathrm{F} \right]$',
                       ymaxrange=[5, 32], df1=df1, df2=df2, df3=df3,
                       tlims=tlims, dolegend=True)

    elif which == 'nos-cond':
        add_currents(axes[0], df, 'wind', 'East [m/s]', 'North [m/s]', df1=df1,
                     df2=df2, df3=df3, tlims=tlims)
        add_var_2units(axes[1], df, 'AtmPr [mb]', 'Atmospheric\npressure [MB]',
                       'mb2hg', '[inHg]', ymaxrange=[1000,1060], df1=df1,
                       df2=df2, df3=df3, tlims=tlims)
        add_var_2units(axes[2], df, 'AirT [deg C]',
                       'Air temp ' + r'$\left[\!^\circ\! \mathrm{C} \right]$',
                       'c2f', r'$\left[\!^\circ\! \mathrm{F} \right]$',
                        ymaxrange=[-25,40], df1=df1, df2=df2,
                       df3=df3, tlims=tlims)
        # df4 is an optional input containing NOAA tidal height prediction
        # will be something like 'Water Level [m, MSL]'
        sshcol = [col for col in df.columns if 'Water Level' in col][0]
        sshlabel = sshcol[:11] + '\n' + sshcol[12:]  # adds line break
        add_var_2units(axes[3], df, sshcol, sshlabel,
                       'm2ft', '[ft]', ymaxrange=[-3,3], tlims=tlims, df4=df4,
                       dolegend=True)
        add_var_2units(axes[4], df, 'WaterT [deg C]',
                       'Water temp\n' + r'$\left[\!^\circ\! \mathrm{C} \right]$',
                       'c2f', r'$\left[\!^\circ\! \mathrm{F} \right]$',
                       ymaxrange=[5, 32], df1=df1, df2=df2, df3=df3,
                       tlims=tlims, dolegend=True)
        add_2var(axes[5], df, 'Salinity', 'Salinity',
                       'Conductivity [mS/cm]',
                       'Conductivity\n' + r'$\left[\mathrm{mS}\cdot\mathrm{cm}^{-1} \right]$',
                       ymaxrange=[0, 30], df1=df1, df2=df2, df3=df3,
                       tlims=tlims, cc1='k', cc2='#559349')

    elif which == 'ports':
        if ~np.isnan(bys.loc[buoy,'Distance to center of bin [m]']):
            dodistance = bys.loc[buoy,'Distance to center of bin [m]']  # label it on plot
        else:
            dodistance = False
        if buoy == 'cc0101':  # this buoy is on the shelf and is not along-channel
            add_currents(axes[0], df, 'water', 'Along [cm/s]', 'Across [cm/s]',
                         df1=df1, df2=df2, df3=df3, tlims=tlims)
            add_vel(axes[1], df, buoy, 'Across [cm/s]', ymaxrange=[-110, 110],
                    df1=df1, df2=df2, df3=df3,
                    label='Cross-shelf\nflow ' + r'$\left[ \mathrm{cm} \cdot \mathrm{s}^{-1} \right]$')
            add_vel(axes[2], df, buoy, 'Along [cm/s]', ymaxrange=[-110, 110],
                    df1=df1, df2=df2, df3=df3,
                    label='Along-shelf\nflow ' + r'$\left[ \mathrm{cm} \cdot \mathrm{s}^{-1} \right]$')
        else:  # all other ports buoys
            add_var_2units(axes[0], df, 'Along [cm/s]', 'Along-channel speed ' +
                           r'$\left[ \mathrm{cm} \cdot \mathrm{s}^{-1} \right]$',
                           'cps2kts', '[knots]', ymaxrange=[-150,150],
                           df4=df4,
                           dolegend=True, add0=True, tlims=tlims, doebbflood=True,
                           doangle=bys.loc[buoy,'angle'],
                           dodepth=bys.loc[buoy,'Depth to center of bin [m]'],
                           dodepthm=bys.loc[buoy,'Model depth to center of bin [m]'],
                           dodistance=dodistance)

    # use longer dataframe in case data or model are cut short
    if df1 is not None or df2 is not None or df3 is not None or df4 is not None and tlims is not None:
        dfm = pd.concat([df1, df2, df3, df4], sort=False)

        if df is None:  # if no data
            df = dfm
        if (dfm.index[-1]-dfm.index[0]) > (df.index[-1]-df.index[0]):
            df = dfm  # use the longer dataframe for labeling x axis

    add_xlabels(axes[nsubplots-1], df, fig, tlims=tlims)

    # add grid lines
    for ax in axes:
        ax.grid(which='major', lw=1.5, color='k', alpha=0.05)
        ax.grid(which='minor', lw=1, color='k', alpha=0.05)

    return fig


def currents(dfs, buoys):
    '''Plot currents for all active buoys.'''

    fig, axes = setup(nsubplots=len(dfs), buoy=buoys[0], title=False)

    # initialize this to be sure one is defined
    dfsave = pd.DataFrame(index=pd.date_range(pd.Timestamp.now() - pd.Timedelta('4 days'), pd.Timestamp.now()))
    tz = 'UTC'  # default choice
    dfsave = dfsave.tz_localize(tz)  # get tz
    first = True  # flag for first currents plot
    for ax, df, buoy in zip(axes, dfs, buoys):

        # label buoy plots
        if len(dfs) == 5:
            ax.text(0.95, 0.75, buoy, transform=ax.transAxes,
                    horizontalalignment='center', fontsize=30, alpha=0.3)
        elif len(dfs) == 4:
            ax.text(0.95, 0.8, buoy, transform=ax.transAxes,
                    horizontalalignment='center', fontsize=30, alpha=0.3)

        if df is None or df.empty or df['East [cm/s]'].isnull().all():
            ax.text(0.2, 0.5, 'Data not available for buoy ' + buoy + ' at this time.', transform=ax.transAxes)
            ax.get_yaxis().set_ticks([])
            continue

        # have to implement timezone to get shift into idx
        df.insert(0, 'idx', date2num(df.index.tz_localize(None).to_pydatetime()))

        if first:
            add_currents(ax, df, 'water', 'East [cm/s]', 'North [cm/s]', compass=True)
            first = False
        else:
            add_currents(ax, df, 'water', 'East [cm/s]', 'North [cm/s]', compass=False)

        # save a df for labeling the bottom axis if it has at least 4 days of data
        # otherwise it squishes up the labels a lot
        if (df.index[-1] - df.index[0]) > (dfsave.index[-1] - dfsave.index[0]):
            dfsave = df  # save for using with bottom labeling

    add_xlabels(axes[len(dfs)-1], dfsave, fig)

    # add grid lines
    for ax in axes:
        ax.grid(which='major', lw=1.5, color='k', alpha=0.05)
        ax.grid(which='minor', lw=1, color='k', alpha=0.05)

    return fig
