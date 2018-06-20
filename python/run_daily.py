'''
Create text files and plots of recent data.

Have both use/show 5 days of data if possible, and use the same mysql query.
Run on a cron job.
'''

import pandas as pd
import numpy as np
import plot_buoy
from os import path
from matplotlib.pyplot import close
import tools
import buoy_properties as bp
import buoy_header as bh
import read
from matplotlib.dates import date2num
import logging

bys = bp.load() # load in buoy data

tz = 'US/Central'

# Email flag. Set to true in script if anything notable is wrong.
eflag = False

if __name__ == "__main__":

    logging.basicConfig(filename=path.join('..', 'logs', 'run_daily.log'),
                        level=logging.WARNING,
                        format='%(asctime)s %(message)s',
                        datefmt='%a %b %d %H:%M:%S %Z %Y')

    engine = tools.setup_engine()
    tablekeys = ['table1', 'table2', 'table3', 'table4', 'table5', 'table6']

    # loop through buoys: query, make text file, make plot
    for buoy in bys.keys():
        # pulls out the non-nan table values to loop over valid table names
        # exclude "tidepredict" since it is not a separate table
        tables = [bys[buoy][table] for table in tablekeys if not pd.isnull(bys[buoy][table]) and 'predict' not in bys[buoy][table]]

        for table in tables:  # loop through tables for each buoy
            # only do this for active buoys
            if not bys[buoy]['active']:
                continue
            # print(buoy)
            # read in data in UTC
            if bys[buoy]['inmysql']:  # mysql tables
                if table == 'sum':
                    # need to have this choose most recent data available
                    # choose to look for ven since sum mostly shows ven data
                    dend = tools.query_setup_recent(engine, buoy, 'ven').tz_localize('utc')
                else:
                    dend = tools.query_setup_recent(engine, buoy, table).tz_localize('utc')
            else:
                dend = pd.Timestamp('now', tz='utc')
            # start 5 days earlier from 00:00 on day of last data, and account for time zones
            # so that enough data is read in for time zone conversion
            tzoffset = (dend.tz_localize(None) - dend.tz_convert(tz).tz_localize(None)).seconds/3600.
            dstart = (dend - pd.Timedelta('5 days')).normalize() + pd.Timedelta(str(tzoffset) + ' hours')
            dend += pd.Timedelta(str(tzoffset) + ' hours')
            df = read.read(buoy, dstart, dend, table=table, usemodel=False,
                           userecent=True, tz=tz)
            if len(buoy) == 1:
                fname = path.join('..', 'daily', 'tabs_' + buoy + '_' + table)
            else:
                fname = path.join('..', 'daily', buoy)
            # write daily data file, for whatever most recent time period
            # data was available
            if df is not None:
                tools.write_file(df, fname)
            # if there are too few rows to plot, set as None
            if df is not None and len(df) < 2:
                df = None
            # no model output for stations in bays or outside domain
            now = pd.Timestamp('now', tz='utc').normalize()
            past = now - pd.Timedelta('5 days')
            future = now + pd.Timedelta('4 days')
            if bp.model(buoy, 'rho') and table != 'eng':
                # read in recent model output, not tied to when data output was found
                dfmodelrecent = read.read(buoy, past, now, table=table,
                                                usemodel='recent', tz=tz)
                # read in forecast model output, not tied to when data output was found
                # subtract a day so that models overlap for sure
                dfmodelforecast = read.read(buoy, now - pd.Timedelta('1 day'),
                                            future, table=table,
                                            usemodel='forecast', tz=tz)
                # Catch if model output isn't working
                if dfmodelrecent is None or dfmodelforecast is None:
                    eflag = True
            else:
                dfmodelrecent = None
                dfmodelforecast = None

            if bys[buoy]['table2'] == 'tidepredict' or bys[buoy]['table2'] == 'currentspredict':
                # import pdb; pdb.set_trace()
                dfmodeltides = read.read(buoy, past, future, usemodel=True, tz=tz)
            else:
                dfmodeltides = None

            # extra time needed in x direction
            if dfmodeltides is not None:  # catches PORTS and tide prediction
                tlims = [date2num(pd.to_datetime(past).to_pydatetime()), date2num(pd.to_datetime(future).to_pydatetime())]
            # none of these use model output, so no forecast and therefore no
            elif table == 'wave' or table == 'eng' or not bp.model(buoy, 'rho'):
                # tlims = None
                tlims = [date2num(pd.to_datetime(past).to_pydatetime()), date2num(pd.to_datetime(now).to_pydatetime())]
            else:
                # tlims = [dfmodelrecent['idx'].iloc[0], dfmodelforecast['idx'].iloc[-1]]
                tlims = [date2num(pd.to_datetime(past).to_pydatetime()), date2num(pd.to_datetime(future).to_pydatetime())]

            # will plot model output from now if available
            # make figure if any df is not equal to None
            if any([dft is not None for dft in [df, dfmodelrecent, dfmodelforecast,dfmodeltides]]):
                fig = plot_buoy.plot(df, buoy, table, df1=None, df2=dfmodelrecent,
                                     df3=dfmodelforecast, df4=dfmodeltides,
                                     tlims=tlims)
                fig.savefig(fname + '.pdf')
                fig.savefig(fname + '.png')
                # save smaller for hover
                fig.savefig(fname + '_low.png', dpi=60)
                close(fig)
            else:
                logging.warning('No figure was created for buoy %s (table %s)' % (buoy, table))


    engine.dispose()


    for buoy in bys.keys():  # loop through buoys separately for buoy headers
        if not bys[buoy]['active']:  # only do this for active buoys
            continue

        # write header
        bh.make(buoy)

    # separate for making currents summaries
    # use data that was calculated previously in this script
    dfs = []; buoys = []
    for buoy in bys.keys():
        if len(buoy) > 1 or not bys[buoy]['active']:  # don't include other buoys
            continue
        fname = 'tabs_' + buoy + '_ven'
        df = pd.read_table(path.join('..', 'daily/', fname), parse_dates=True,
                           index_col=0, na_values=[-999])
        df = df.tz_localize('utc')  # all files are read in utc
        # if dataframe is too short, don't include
        if len(df) < 10:
            dfs.append(None)
        # check if any of dataset is from within the past 5 days before appending
        elif (pd.Timestamp('now', tz='utc') - df.index[-1]).days < 5:
            dfs.append(df)
        else:
            dfs.append(None)
        buoys.append(buoy)
    fig1 = plot_buoy.currents(dfs[:5], buoys[:5])
    fig2 = plot_buoy.currents(dfs[5:], buoys[5:])
    fig1.savefig(path.join('..', 'daily', 'currents1.pdf'))
    fig1.savefig(path.join('..', 'daily', 'currents1.png'))
    fig2.savefig(path.join('..', 'daily', 'currents2.pdf'))
    fig2.savefig(path.join('..', 'daily', 'currents2.png'))
    close(fig1)
    close(fig2)


    # send error email if eflag was set to True somewhere
    if eflag:
        tools.send_email()
