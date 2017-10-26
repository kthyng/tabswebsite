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

bys = bp.load() # load in buoy data


if __name__ == "__main__":

    engine = tools.setup_engine()
    tablekeys = ['table1', 'table2', 'table3', 'table4', 'table5']

    # loop through buoys: query, make text file, make plot
    for buoy in bys.keys():
        # pulls out the non-nan table values to loop over valid table names
        tables = [bys[buoy][table] for table in tablekeys if not pd.isnull(bys[buoy][table])]

        for table in tables:  # loop through tables for each buoy
            # if not 'tcoon' in table:
            #     continue
            print(buoy)
            # read in data
            if bys[buoy]['inmysql']:  # mysql tables
                dend = tools.query_setup_recent(engine, buoy, table)
            else:
                dend = pd.Timestamp('now', tz='utc')

            # start 6 days earlier from last data
            dstart = dend - pd.Timedelta('6 days')
            df = read.read(buoy, dstart, dend, table=table)
            if len(buoy) == 1:
                fname = path.join('..', 'daily', 'tabs_' + buoy + '_' + table)
            else:
                fname = path.join('..', 'daily', buoy)
            # elif 'ndbc' in table:
            #     fname = path.join('..', 'daily', 'ndbc_' + buoy)
            # elif 'tcoon' in table:
            #     fname = path.join('..', 'daily', 'tcoon_' + buoy)
            # elif 'nos' in table:
            #     fname = path.join('..', 'daily', 'nos_' + buoy)
            # elif 'ports' in table:
            #     fname = path.join('..', 'daily', 'ports_' + buoy)
            # write daily data file, for whatever most recent time period
            # data was available
            if df is not None:
                tools.write_file(df, fname)
            # if there are too few rows to plot, set as None
            if df is not None and len(df) < 2:
                df = None
            # no model output for stations in bays or outside domain
            now = pd.Timestamp('now', tz='utc')
            past = now - pd.Timedelta('5 days')
            future = pd.Timestamp('now', tz='utc') + pd.Timedelta('5 days')
            if bp.model(buoy, 'rho'):
                # read in recent model output, not tied to when data output was found
                dfmodelrecent = read.read_model(buoy, table, past, now,
                                                timing='recent')
                # read in forecast model output, not tied to when data output was found
                # subtract a day so that models overlap for sure
                dfmodelforecast = read.read_model(buoy, table, now - pd.Timedelta('1 day'), future,
                                                  timing='forecast')
            elif table == 'ports':
                # use tidal current prediction at these sites, from NOAA
                dfmodelrecent = None
                dfmodelforecast = read.read_ports(buoy, now)
            else:
                dfmodelrecent = None
                dfmodelforecast = None

            if table == 'wave' or table == 'eng' or dfmodelrecent is None or dfmodelforecast is None:
                tlims = None
            else:
                tlims = [dfmodelrecent.idx[0], dfmodelforecast.idx[-1]]
            # will plot model output from now if available, otherwise data regardless of how old
            fig = plot_buoy.plot(df, buoy, table, df1=None, df2=dfmodelrecent, df3=dfmodelforecast, tlims=tlims)
            fig.savefig(fname + '.pdf')
            fig.savefig(fname + '.png')
            # save smaller for hover
            fig.savefig(fname + '_low.png', dpi=60)
            close(fig)

    # for buoy in bd.buoys():  # loop through buoys separately for buoy headers
    #     # write header
    #     bh.make(buoy)

    # # separate for making currents summaries
    # # use data that was calculated previously in this script
    # dfs = []; buoys = []
    # for buoy in bd.buoys():
    #     if len(buoy) > 1:  # don't include NDBC buoys
    #         continue
    #     fname = 'tabs_' + buoy + '_ven'
    #     df = tools.read(path.join('..', 'daily/', fname))
    #     # check if any of dataset is from within the past 5 days before appending
    #     if (pd.datetime.now() - df.index[-1]).days < 5:
    #         dfs.append(df)
    #     else:
    #         dfs.append(None)
    #     buoys.append(buoy)
    # fig1 = plot_buoy.currents(dfs[:5], buoys[:5])
    # fig2 = plot_buoy.currents(dfs[5:], buoys[5:])
    # fig1.savefig(path.join('..', 'daily', 'currents1.pdf'))
    # fig1.savefig(path.join('..', 'daily', 'currents1.png'))
    # fig2.savefig(path.join('..', 'daily', 'currents2.pdf'))
    # fig2.savefig(path.join('..', 'daily', 'currents2.png'))
    # close(fig1)
    # close(fig2)
