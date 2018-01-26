'''Read functions.'''


from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from matplotlib.dates import date2num
import buoy_properties as bp
import xarray as xr
import gsw
from os import system, path
import tools
import requests
import logging

bys = bp.load() # load in buoy data


def read(buoy, dstart, dend, table=None, units=None, tz='utc',
         usemodel=False, userecent=True):
    '''Calls appropriate read function for each table type.

    dstart and dend are datetime objects.
    table is necessary if buoy is a TABS buoy (length=1).
    usemodel can be: False, True (for ports), or 'hindcast', 'recent', 'forecast' (ROMS)
    '''

    # import pdb; pdb.set_trace()
    # read from recent file
    if dstart is None:
        df = pd.read_table(buoy, index_col=0, parse_dates=True)
    # read in model output but not ports model output
    elif isinstance(usemodel,str):
        # assert isinstance(usemodel, str), \
        #     'usemodel should be a string containing "hindcast", "recent", or "forecast"'
        df = read_model(buoy, table, dstart, dend, timing=usemodel, tz=tz, units=units)
    elif bys[buoy]['inmysql']:
        # Call general read function to distribute to correct buoy read function
        df = read_buoy(buoy, dstart, dend, table=table, units=units,
                       tz=tz, userecent=userecent)
    else:

        usefile = True  # initially True, set to False once we've read from the file
        fname = '../daily/' + buoy + '_all.hdf'
        date = dstart
        df = pd.DataFrame()
        # check that we are within normal data frequency
        while date + pd.Timedelta('60 minutes') < dend:
            # print('reading buoy ' + buoy + ': date: ', date, 'dend: ', dend)
            # # if we are using data, dend cannot be in the future
            # dend = min(dend, pd.Timestamp('now', tz='utc'))
            if path.exists(fname) and usefile and not usemodel:  # usemodel here since can't read in model output
                df = pd.read_hdf(fname, where='index>=date&index<=dend')
                usefile = False
                # if dstart > when data in fname ends, just go to the else on the next while loop
                if df is not None and not df.empty:
                    date = df.index[-1].tz_localize('utc').normalize() + pd.Timedelta('1 day')  # bump up to start of next day
            else:
                td = pd.Timedelta('31 days')
                if 'ports' in bys[buoy]['table1'] and usemodel:
                    td = pd.Timedelta('6 days')  # tidal model gives 7 days of output
                # need to make sure dates are all in same time zone
                if date.tzinfo.zone == dend.tzinfo.zone:  # if time zones the same, don't change either
                    daystoread = min(td, dend-date)
                else:  # convert dend to utc
                    daystoread = min(td, dend.tz_convert('utc')-date)
                dftemp = read_buoy(buoy, date, date+daystoread, table=table, units=units,
                                   tz=tz, usemodel=usemodel, userecent=userecent)
                if df is not None:
                    df = df.append(dftemp)
                else:  # if df is None, rename dftemp to df
                    df = dftemp
                date += pd.Timedelta(daystoread) + pd.Timedelta('1 day')

    # return None instead of just header if no data for time period
    if df is not None and not df.empty:
        df.index.name = 'Dates [UTC]'
        df = df.tz_localize('utc')  # all files are read in utc
        df = tools.convert_units(df, units=units, tz=tz)  # change units if necessary
        if dstart is not None:
            df = df.loc[(df.index > dstart) & (df.index < dend)]
        df = df.astype(float)  # makes sure that all columns are floats for consistency
    else:
        df = None

    return df


def read_buoy(buoy, dstart, dend, table=None, units=None, tz=None,
         usemodel=False, userecent=True):

    # need table if TABS buoy
    if len(buoy) == 1:
        assert table is not None, 'need to input table when using TABS buoy'

    # if/elif statements checking which table type buoy has
    if 'tcoon' in bys[buoy]['table1'] or 'nos' in bys[buoy]['table1']:
        df = read_nos(buoy, dstart, dend, usemodel=usemodel)
    elif 'ports' in bys[buoy]['table1']:
        df = read_ports(buoy, dstart, dend, usemodel=usemodel)
    elif 'ndbc' in bys[buoy]['table1']:  # whether or not in mysql database
        df = read_ndbc(buoy, dstart, dend, userecent=userecent)
    elif len(buoy) == 1:  # tabs buoys
        # sum goes across tables
        dfs = []
        if table == 'sum':
            dfs.append(read_tabs('ven', buoy, dstart, dend))
            if isinstance(bys[buoy]['table3'], str) and 'salt' in bys[buoy]['table3']:
                # drop water temp from here so that there aren't two in dataframe
                dfs.append(read_tabs('salt', buoy, dstart, dend).drop(['WaterT [deg C]'], axis=1))
            if isinstance(bys[buoy]['table4'], str) and 'met' in bys[buoy]['table4']:
                dfs.append(read_tabs('met', buoy, dstart, dend))
            # combine tables together
            df = pd.concat([df for df in dfs], axis=1)

        else:
            df = read_tabs(table, buoy, dstart, dend)

    return df


def read_ports(buoy, dstart, dend, usemodel=False):
    '''Set up urls and read from them to get PORTS currents.

    Only data or model is read in during a single call to this function.
    '''

    if not usemodel:
        base = 'https://tidesandcurrents.noaa.gov/cdata/DataPlot?&unit=0&timeZone=UTC&view=csv&id='
        suffix = '&bin=0&bdate=' + dstart.strftime('%Y%m%d') + '&edate=' + (dend).strftime('%Y%m%d')
        url = base + buoy + suffix

    else:  # model
        # tidal prediction (only goes back and forward in time 2 years)
        base = 'https://tidesandcurrents.noaa.gov/noaacurrents/DownloadPredictions?'
        options = 'fmt=csv&t=24hr&i=30min&i=30min&d='+ dstart.strftime('%Y-%m-%d') + '&r=2&tz=GMT&u=2&id='
        url = base + options + buoy

    df = read_ports_df(url)

    return df


def read_ports_df(dataname, dates=None):

    df = pd.read_csv(dataname, parse_dates=True, index_col=0,
                     error_bad_lines=False, warn_bad_lines=False)

    # this catches if data wasn't returned properly
    if df.empty:
        return None

    if 'http' and 'Predictions' in dataname:  # website, model predictions
        df.rename(columns={' Speed (cm/sec)': 'Along [cm/s]'}, inplace=True)

    elif 'http' and 'DataPlot' in dataname:  # reading from website, data
        # find buoy name
        buoy = dataname.split('id=')[1].split('&')[0]

        # angle needs to be in math convention for trig and between 0 and 360
        theta = 90 - df[' Dir (true)']
        theta[theta<0] += 360
        # tidal data needs to be converted into along-channel direction
        # along-channel flood direction (from website for data), converted from compass to math angle
        diralong = 90 - bys[buoy]['angle']
        if diralong < 0:
            diralong += 360
        # first convert to east/west, north/south
        # all speeds in cm/s
        east = df[' Speed (cm/sec)']*np.cos(np.deg2rad(theta))
        north = df[' Speed (cm/sec)']*np.sin(np.deg2rad(theta))
        # then convert to along-channel (mean ebb and mean flood)
        df['Along [cm/s]'] = (east*np.cos(np.deg2rad(diralong)) + north*np.sin(np.deg2rad(diralong)))
        df['Across [cm/s]'] = (-east*np.sin(np.deg2rad(diralong)) + north*np.cos(np.deg2rad(diralong)))

        df.rename(columns={' Speed (cm/sec)': 'Speed [cm/s]',
                           ' Dir (true)': 'Dir [deg T]'}, inplace=True)

    df.index.rename('Dates [UTC]', inplace=True)

    return df


def read_nos(buoy, dstart, dend, usemodel=False):
    '''Set up urls and then read from them to get TCOON and NOS data.

    Most stations have several data sources, so they are aggregated here.
    This calls to read_tcoon_df() to do the reading and rearranging.
    dstart and dend are datetime objects.'''

    if not usemodel:
        # tide, met, and phys data
        prefixes = ['https://tidesandcurrents.noaa.gov/api/datagetter?product=water_level&application=NOS.COOPS.TAC.WL&station=',
                    'https://tidesandcurrents.noaa.gov/cgi-bin/newdata.cgi?type=met&id=',
                    'https://tidesandcurrents.noaa.gov/cgi-bin/newdata.cgi?type=phys&id=']
        # dstart and dend need to be in format YYYYMMDD
        dstarts = dstart.strftime('%Y%m%d')
        dends = dend.strftime('%Y%m%d')
        suffixes = ['&begin_date=' + dstarts + '&end_date=' + dends + '&datum=MSL&units=metric&time_zone=GMT&format=csv',
                    '&begin=' + dstarts + '&end=' + dends + '&units=metric&timezone=GMT&mode=csv&interval=6',
                    '&begin=' + dstarts + '&end=' + dends + '&units=metric&timezone=GMT&mode=csv&interval=6']
        dfs = []
        for prefix, suffix in zip(prefixes, suffixes):
            url = prefix + buoy + suffix
            dft = read_nos_df(url)
            if dft is not None:
                dft = dft[~dft.index.duplicated(keep='first')]  # remove any duplicated indices
            dfs.append(dft)
        # combine the dataframes together
        # don't append if all df are empty
        if [df.empty for df in dfs].count(True) != len(dfs):
            df = pd.concat([df for df in dfs if not df.empty], axis=1)
        else:
            df = pd.concat([df for df in dfs], axis=1)

        # calculate salinity from conductivity, if available
        if 'Conductivity [mS/cm]' in df.keys():
            if not 'AtmPr [MB]' in df.keys():
                pr = np.zeros(len(df))
            else:
                pr = df['AtmPr [MB]']/100. - 10.1325
            df['Salinity'] = gsw.SP_from_C(df['Conductivity [mS/cm]'],
                                           df['WaterT [deg C]'],
                                           pr)
            # dictionary for rounding decimal places
            rdict = {'Salinity': 2}
            df = df.round(rdict)
    else:  # use model

        prefix = 'https://tidesandcurrents.noaa.gov/api/datagetter?product=predictions&application=NOS.COOPS.TAC.WL&station='
        dstarts = dstart.strftime('%Y%m%d')
        dends = dend.strftime('%Y%m%d')
        suffix = '&begin_date=' + dstarts + '&end_date=' + dends + '&datum=MSL&time_zone=GMT&units=metric&interval=h&format=csv'
        url = prefix + buoy + suffix
        df = read_nos_df(url)

    return df


def read_nos_df(dataname):
    '''Read in individual tcoon datasets and arrange variables.'''

    df = pd.read_csv(dataname, parse_dates=[0], index_col=0)
    if 'type=met' in dataname:
        names = ['Speed [m/s]', 'Dir from [deg T]', 'Gust [m/s]', 'AirT [deg C]', 'AtmPr [MB]', 'RelH [%]', 'East [m/s]', 'North [m/s]']
        df = df.drop([' VIS'], axis=1, errors='ignore')
        # dictionary for rounding decimal places
        rdict = {'East [m/s]': 2, 'North [m/s]': 2}

        # angle needs to be in math convention for trig and between 0 and 360
        # also have to switch wind from direction from to direction to with 180 switch
        theta = 90 - (df[' DIR'] - 180)
        theta[theta<0] += 360
        df['East [m/s]'] = df[' WINDSPEED']*np.cos(np.deg2rad(theta))
        df['North [m/s]'] = df[' WINDSPEED']*np.sin(np.deg2rad(theta))

    elif 'product=water_level' in dataname:
        names = ['Water Level [m]']
        df = df.drop([' Sigma', ' O', ' F', ' R', ' L', ' Quality '], axis=1, errors='ignore')
        # dictionary for rounding decimal places
        rdict = {}

    elif 'type=phys' in dataname:
        buoy = dataname.split('id=')[1][:7]
        if 'cond' in bys[buoy]['table1']:
            names = ['WaterT [deg C]', 'Conductivity [mS/cm]']
        else:
            names = ['WaterT [deg C]']
            df = df.drop(['CONDUCTIVITY'], axis=1)
        rdict = {}

    elif 'prediction' in dataname:  # tidal height prediction
        names = ['Water Level [m]']
        # dictionary for rounding decimal places
        rdict = {}

    # remove error message from when data is missing
    if not df.empty:
        if isinstance(df.index[0], str):
            df = df.drop(df.index[0], axis=0)
            df = pd.DataFrame()
    if not df.empty:
        df.columns = names
        df.index.name = 'Dates [UTC]'
        df = df.round(rdict)

    return df


def read_ndbc(buoy, dstart, dend, userecent=True):
    '''Set up to read in NDBC buoy data (from mysql or website).

    Call to read_ndbc_df to do actually reading in.
    userecent=True will use recent 45 days of data. userecent=False will not.
    '''

    if bys[buoy]['inmysql']:  # mysql

        engine = tools.setup_engine()
        q = tools.query_setup(engine, buoy, 'ndbc',
                              dstart.strftime("%Y-%m-%d"),
                              dend.strftime("%Y-%m-%d %H:%M"))
        df = read_ndbc_df([q, engine])
        engine.dispose()

    else:

        date = dstart; df = pd.DataFrame()  # initialize
        while date < dend:

            year = date.year; month = date.month

            # check if desired time window is within the last 45 days, in which case
            # use the "realtime" data from ndbc
            if (pd.Timestamp('now', tz='utc') - pd.Timedelta('45 days') < date) and userecent:
                url = 'http://www.ndbc.noaa.gov/data/realtime2/' + buoy + '.txt'
                date = dend

            elif year == pd.Timestamp('now', tz='utc').year:  # this year but not within 45 days of now
                monthname = date.strftime('%b')
                if month == pd.Timestamp('now', tz='utc').month - 1:
                    # this url is used by their system for the month before the present month
                    url = 'http://www.ndbc.noaa.gov/data/stdmet/' + monthname + '/' + buoy.lower() + '.txt'
                else:
                    url = 'http://www.ndbc.noaa.gov/data/stdmet/' + monthname + '/' + buoy.lower() + str(month) + str(year) + '.txt.gz'
                date += pd.Timedelta('31 days')  # close enough to 1 month, for next loop

            else:  # older than present year
                url = 'http://www.ndbc.noaa.gov/data/historical/stdmet/' + buoy.lower() + 'h' + str(year) + '.txt.gz'
                date += pd.Timedelta(str(367 - date.dayofyear) + ' days')  # get to early following year, for next loop

            if requests.get(url).ok:  # only try url if it exists
                dftemp = read_ndbc_df(url)
                if dftemp.index[-1] < dftemp.index[0]:  # backward order
                    dftemp = dftemp[::-1]
                df = df.combine_first(dftemp)  # combine with preference for df if overlapping

    return df


def read_ndbc_df(dataname):
    '''Read in individual ndbc datasets from website (or either?) and arrange variables.

    if dataname is a string, it is a file location. If it is a list with two
    entries, they give the query string and the mysql engine.'''

    if len(dataname) == 2:  # mysql

        query = dataname[0]; engine = dataname[1]
        df = pd.read_sql_query(query, engine, index_col=['obs_time'])
        df = df.drop(['station', 'date', 'time', 'windgust2'], axis=1)
        names = ['Speed [m/s]', 'Dir from [deg T]', 'Gust [m/s]', 'AtmPr [MB]', 'AirT [deg C]', 'Dew pt [deg C]', 'WaterT [deg C]', 'RelH [%]', 'Wave Ht [m]', 'Wave Pd [s]', 'East [m/s]', 'North [m/s]']
        df[df == -99.0] = np.nan  # replace missing values

    elif isinstance(dataname, str):  # go to ndbc
        # these are for two different formats
        try:
            df = pd.read_table(dataname, header=0, skiprows=[1],
                               delim_whitespace=True,
                               na_values=['MM',-99.0, 999.00, 9999.00],
                               parse_dates=[[0,1,2,3,4]], index_col=0)
            df.index = pd.to_datetime(df.index, format='%Y %m %d %H %M')
        except:
            df = pd.read_table(dataname, header=0, skiprows=[1],
                               delim_whitespace=True,
                               na_values=['MM',-99.0, 999.00, 9999.00],
                               parse_dates=[[0,1,2,3]], index_col=0)
            # this catches the 2 digit year with no minutes case
            df.index = pd.to_datetime(df.index, format='%y %m %d %H')
        df = df.drop(['WVHT', 'DPD', 'APD', 'MWD', 'VIS', 'PTDY', 'TIDE'], axis=1, errors='ignore')
        # rename to match mysql because using below
        if 'WDIR' in df.keys():
            df.rename(columns={'WDIR': 'winddir', 'WSPD': 'windspeed'}, inplace=True)
        else:
            df.rename(columns={'WD': 'winddir', 'WSPD': 'windspeed'}, inplace=True)
        names = ['Dir from [deg T]', 'Speed [m/s]', 'Gust [m/s]', 'AtmPr [MB]', 'AirT [deg C]', 'WaterT [deg C]', 'Dew pt [deg C]', 'East [m/s]', 'North [m/s]']

    rdict = {'East [m/s]': 2, 'North [m/s]': 2}

    # angle needs to be in math convention for trig and between 0 and 360
    # also have to switch wind from direction from to direction to with 180 switch
    theta = 90 - (df['winddir'] - 180)
    theta[theta<0] += 360
    df['East [m/s]'] = df['windspeed']*np.cos(np.deg2rad(theta))
    df['North [m/s]'] = df['windspeed']*np.sin(np.deg2rad(theta))

    df.columns = names
    df.index.name = 'Dates [UTC]'
    df = df.round(rdict)

    return df


def read_tabs(table, buoy, dstart, dend):
    '''Read in TABS data from mysql. Also process variables as needed.

    Time from database is in UTC. dstart, dend are datetime objects.'''

    engine = tools.setup_engine()
    query = tools.query_setup(engine, buoy, table, dstart.strftime("%Y-%m-%d"),
                              dend.strftime("%Y-%m-%d %H:%M"))
    df = pd.read_sql_query(query, engine, index_col=['obs_time'])
    engine.dispose()
    df.drop(df.index[df.index.isnull()], inplace=True)  # drop bad rows
    df[(df == -99.0) | (df == -999.0) | (df == -999.00)] = np.nan  # replace missing values

    if 'date' in df.keys():
        df.drop(['date', 'time'], inplace=True, axis=1)
    for key in df.keys():
        if (df[key]==0).all():
            df.loc[:, key] = np.nan
        # if more than a quarter of the entries are 0, must be wrong
        elif (df[key][1::2]==0).sum() > len(df)/4:
            df.loc[1::2, key] = np.nan
        elif (df[key][::2]==0).sum() > len(df)/4:
            df.loc[::2, key] = np.nan

    if table == 'ven':
        ind = df.tx.isnull()
        df.drop(df.index[ind], inplace=True)  # drop bad rows
        names = ['East [cm/s]', 'North [cm/s]', 'Dir [deg T]', 'WaterT [deg C]', 'Tx', 'Ty', 'Speed [cm/s]', 'Across [cm/s]', 'Along [cm/s]']            # df.columns = names
        df['Speed [cm/s]'] = np.sqrt(df['veast']**2 + df['vnorth']**2)
        df['Speed [cm/s]'] = df['Speed [cm/s]'].round(2)
        # Calculate along- and across-shelf
        # along-shelf rotation angle in math angle convention
        theta = np.deg2rad(-(bys[buoy]['angle']-90))  # convert from compass to math angle
        df['Across [cm/s]'] = df['veast']*np.cos(-theta) - df['vnorth']*np.sin(-theta)
        df['Along [cm/s]'] = df['veast']*np.sin(-theta) + df['vnorth']*np.cos(-theta)
        # dictionary for rounding decimal places
        rdict = {'Speed [cm/s]': 2, 'Across [cm/s]': 2, 'Along [cm/s]': 2, 'Dir [deg T]': 0}

    elif table == 'eng':
        names = ['VBatt [Oper]', 'SigStr [dB]', 'Comp [deg M]', 'Nping', 'Tx', 'Ty', 'ADCP Volt', 'ADCP Curr', 'VBatt [sleep]']
        rdict = {}

    elif table == 'met':
        names = ['East [m/s]', 'North [m/s]', 'AirT [deg C]', 'AtmPr [MB]', 'Gust [m/s]', 'Comp [deg M]', 'Tx', 'Ty', 'PAR ', 'RelH [%]', 'Speed [m/s]', 'Dir from [deg T]']
        df['Speed [m/s]'] = np.sqrt(df['veast']**2 + df['vnorth']**2)
        df['Dir from [deg T]'] = 90 - np.rad2deg(np.arctan2(-df['vnorth'], -df['veast']))
        rdict = {'Speed [m/s]': 2, 'Dir from [deg T]': 0}

    elif table == 'salt':
        names = ['WaterT [deg C]', 'Cond [ms/cm]', 'Salinity', 'Density [kg/m^3]', 'SoundVel [m/s]']
        rdict = {}

        # density is all 0s, so need to overwrite
        df['density'] = gsw.rho(df['salinity'], df['twater'], np.zeros(len(df)))

    elif table == 'wave':
        names = ['WaveHeight [m]', 'MeanPeriod [s]', 'PeakPeriod [s]']
        rdict = {}

    df.columns = names
    df.index.name = 'Dates [UTC]'
    df = df.round(rdict)

    return df


def read_model(buoy, which, dstart, dend, timing='recent', units='Metric', tz='utc'):
    '''Read in model output.

    dstart and dend are datetime objects.'''

    dostations = False  # this is updated if buoy is in stations list on reading

    # separate out which model type we want
    if timing == 'hindcast':
        if not bp.station(buoy) == -999:  # can read faster from stations file if buoy included
            loc = 'http://copano.tamu.edu:8080/thredds/dodsC/NcML/txla_hindcast_sta'
            dostations = True
        else:
            loc = 'http://copano.tamu.edu:8080/thredds/dodsC/NcML/txla_hindcast_agg'
        locf = 'http://copano.tamu.edu:8080/thredds/dodsC/NcML/txla_hindcast_frc'  # forcing info
    elif timing == 'recent':
        loc = 'http://copano.tamu.edu:8080/thredds/dodsC/NcML/oof_archive_agg'
        locf = 'http://copano.tamu.edu:8080/thredds/dodsC/NcML/oof_archive_agg_frc'  # forcing info
    elif timing == 'forecast':
        loc = 'http://copano.tamu.edu:8080/thredds/dodsC/oof_other/roms_his_f_previous_day.nc'
        locf = 'http://copano.tamu.edu:8080/thredds/dodsC/oof_other/roms_frc_f_latest.nc'


    # Try two different locations for model output. If won't work, give up.
    try:
        try:  # try copano thredds first
            ds = xr.open_dataset(loc)
        except IOError as e:  # if copano thredds is not working
            logging.exception(e)
            logging.warning('For model timing %s, loc %s did not work. Trying with barataria instead...' % (timing, loc))
            try:  # try barataria thredds
                loc = 'barataria'.join(loc.split('copano'))  # change to barataria thredds if copano won't work
                ds = xr.open_dataset(loc)
            except IOError as e:  # if this also doesn't work, send email and give up
                logging.exception(e)
                logging.warning('For model timing %s, loc %s did not work. Giving up.' % (timing, loc))
                # skip model output but do data
                ds = None
    except Exception as e:
        logging.exception(e)
        logging.warning('For model timing %s, some weird error happened. Giving up.' % (timing))
        ds = None

    # use modeling forcing information instead of model output. If won't work, give up.
    try:
        try:
            dsf = xr.open_dataset(locf)
        except IOError as e:  # if copano thredds is not working
            logging.exception(e)
            logging.warning('For model timing %s, forcing loc %s did not work. Trying with barataria instead...' % (timing, loc))
            try:
                locf = 'barataria'.join(locf.split('copano'))  # change to barataria thredds if copano won't work
                dsf = xr.open_dataset(locf)
            except IOError as e:  # if barataria thredds is also not working
                logging.exception(e)
                logging.warning('For model timing %s, forcing loc %s did not work. Trying with barataria instead...' % (timing, loc))
                # skip model output but do data
                dsf = None
    # This is an overall catch in case forcing can't be read in due to unknown error
    except Exception as e:
        logging.exception(e)
        logging.warning('For model timing %s for forcing information, some weird error happened. Giving up.' % (timing))
        # skip model output but do data
        dsf = None

    # only do this if dend is less than or equal to the first date in the model output
    # check if last data datetime is less than 1st model datetime or
    # first data date is greater than last model time, so that time periods overlap
    # sometimes called ocean_time and sometimes time
    # this case catches when the timing of the model is output the desired times
    if ds is None or dend <= pd.Timestamp(ds['ocean_time'].isel(ocean_time=0).data, tz='utc') or \
       dstart >= pd.Timestamp(ds['ocean_time'].isel(ocean_time=-1).data, tz='utc'):
        df = None
        return df
    else:
        # Initialize model dataframe with times
        df = pd.DataFrame(index=ds['ocean_time'].sel(ocean_time=slice(dstart, dend)))

        # need separate code for dostations
        if dostations:
            i = bp.station(buoy)
            along = ds['u'].sel(ocean_time=slice(dstart, dend))\
                           .isel(s_rho=-1, station=i)*100  # convert to cm/s
            across = ds['v'].sel(ocean_time=slice(dstart, dend))\
                            .isel(s_rho=-1, station=i)*100
            df['WaterT [deg C]'] = ds['temp'].sel(ocean_time=slice(dstart, dend)).isel(s_rho=-1, station=i)
            df['Salinity'] = ds['salt'].sel(ocean_time=slice(dstart, dend)).isel(s_rho=-1, station=i)
            df['East [m/s]'] = ds['Uwind'].sel(ocean_time=slice(dstart, dend)).isel(station=i)
            df['North [m/s]'] = ds['Vwind'].sel(ocean_time=slice(dstart, dend)).isel(station=i)

            # rotate from curvilinear to cartesian
            anglev = ds['angle'][i]  # using at least nearby grid rotation angle
        else:
            try:
                if which in ['ven', 'sum']:
                    j, i = bp.model(buoy, 'u')  # get model indices
                    along = ds['u'].sel(ocean_time=slice(dstart, dend))\
                                   .isel(s_rho=-1, eta_u=j, xi_u=i)*100  # convert to cm/s
                    j, i = bp.model(buoy, 'v')  # get model indices
                    across = ds['v'].sel(ocean_time=slice(dstart, dend))\
                                    .isel(s_rho=-1, eta_v=j, xi_v=i)*100
                    # rotate from curvilinear to cartesian
                    anglev = ds['angle'][j,i]  # using at least nearby grid rotation angle
                if not bp.model(buoy, 'rho'):  # no model indices saved
                    return None
                else:
                    j, i = bp.model(buoy, 'rho')  # get model indices
                df['WaterT [deg C]'] = ds['temp'].sel(ocean_time=slice(dstart, dend)).isel(s_rho=-1, eta_rho=j, xi_rho=i)
                if which in ['salt', 'sum'] or 'cond' in which:
                    df['Salinity'] = ds['salt'].sel(ocean_time=slice(dstart, dend)).isel(s_rho=-1, eta_rho=j, xi_rho=i)
                df['East [m/s]'] = ds['Uwind'].sel(ocean_time=slice(dstart, dend)).isel(eta_rho=j, xi_rho=i)
                df['North [m/s]'] = ds['Vwind'].sel(ocean_time=slice(dstart, dend)).isel(eta_rho=j, xi_rho=i)

            except Exception as e:
                logging.exception(e)
                logging.warning('Model timing %s. This warning should be more specific.' % timing)
                return df

        # Project along- and across-shelf velocity rather than use from model
        # so that angle matches buoy
        if which in ['ven', 'sum']:
            df['East [cm/s]'], df['North [cm/s]'] = tools.rot2d(along, across, anglev)  # approximately to east, north
            theta = np.deg2rad(-(bys[buoy]['angle']-90))  # convert from compass to math angle
            df['Across [cm/s]'] = df['East [cm/s]']*np.cos(-theta) - df['North [cm/s]']*np.sin(-theta)
            df['Along [cm/s]'] = df['East [cm/s]']*np.sin(-theta) + df['North [cm/s]']*np.cos(-theta)
        if which in ['salt', 'sum']:
            df['Density [kg/m^3]'] = gsw.rho(df['Salinity'], df['WaterT [deg C]'], np.zeros(len(df)))

    # check meteorological timing separately since can be different
    if dsf is None or dend <= pd.Timestamp(dsf['time'].isel(time=0).data, tz='utc') or \
       dstart >= pd.Timestamp(dsf['time'].isel(time=-1).data, tz='utc'):
        # fill in met keys so they exist
        keys = ['AtmPr [MB]', 'AirT [deg C]']
        if which == 'met': keys += ['RelH [%]']
        for key in keys:
            df[key] = np.nan
        return df
    else:
        j, i = bp.model(buoy, 'rho')  # get model indices
        df['AtmPr [MB]'] = dsf['Pair'].sel(time=slice(dstart, dend)).isel(eta_rho=j, xi_rho=i).to_dataframe()['Pair'].resample('60T').interpolate()
        df['AirT [deg C]'] = dsf['Tair'].sel(time=slice(dstart, dend)).isel(eta_rho=j, xi_rho=i).to_dataframe()['Tair'].resample('60T').interpolate()
        if which == 'met':
            df['RelH [%]'] = dsf['Qair'].sel(time=slice(dstart, dend)).isel(eta_rho=j, xi_rho=i).to_dataframe()['Qair'].resample('60T').interpolate()

    return df
