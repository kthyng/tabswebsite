'''Read functions.'''


from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from matplotlib.dates import date2num
import xarray as xr
from os import system, path
import tools
import requests
import logging
import netCDF4 as netCDF
import gsw

bys = pd.read_csv('../includes/buoys.csv', index_col=0)

# number of repeats to try for internet and server hiccups
nrepeats = 2

# Capture warnings in log instead of emailing me
logging.captureWarnings(True)

# log for model output messages, since they swamp all others
# formatting for logfile
formatter = logging.Formatter('%(asctime)s %(message)s','%a %b %d %H:%M:%S %Z %Y')
name = 'models'
logfilename = path.join('..', 'logs', name + '.log')
loglevel=logging.WARNING
# set up logger file
handler = logging.FileHandler(logfilename)
handler.setFormatter(formatter)
logger_read = logging.getLogger(name)
logger_read.setLevel(loglevel)
logger_read.addHandler(handler)

def read(buoy, dstart, dend, table=None, units=None, tz='UTC',
         usemodel=False, userecent=True, datum='MSL', s_rho=-1):
    '''Calls appropriate read function for each table type.

    dstart and dend are pd.Timestamp objects.
    table is necessary if buoy is a TABS buoy (length=1).
    usemodel can be: False, True (for ports), or 'hindcast', 'recent', 'forecast' (ROMS)
    userecent is for NDBC data, for using the most recent 45 days of data

    datum (str) can be 'MSL', 'MHHW', 'MHW', 'MLW', 'MLLW', 'MTL'; for tidal height

    Example:
    buoy = '8779770'; dstart = pd.Timestamp('2019-9-5').tz_localize('UTC'); dend = pd.Timestamp('2019-9-9').tz_localize('UTC')
    df = read.read(buoy, dstart, dend)
    '''

    # read from recent file
    if dstart is None:
        df = pd.read_table(buoy, index_col=0, parse_dates=True)
    # read in model output but not ports model output
    elif isinstance(usemodel,str):
        # this does not catch NOAA model case for tides
        # assert isinstance(usemodel, str), \
        #     'usemodel should be a string containing "hindcast", "recent", or "forecast"'
        df = read_model(buoy, table, dstart, dend, timing=usemodel, tz=tz,
                        units=units, s_rho=s_rho)
    elif buoy in bys.index and bys.loc[buoy,'inmysql']:
        # Call general read function to distribute to correct buoy read function
        df = read_buoy(buoy, dstart, dend, table=table, units=units,
                       userecent=userecent)
    else:

        usefile = True  # initially True, set to False once we've read from the file
        fname = '../daily/' + buoy + '_all.hdf'
        date = dstart  # in UTC
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
                    # date is redefined and is in UTC
                    date = df.index[-1].tz_localize('UTC').normalize() + pd.Timedelta('1 day')  # bump up to start of next day
            else:
                td = pd.Timedelta('31 days')
                if buoy in bys.index and 'ports' in bys.loc[buoy,'table1'] and usemodel:
                    td = pd.Timedelta('6 days')  # tidal model gives 7 days of output
                elif 'full' in buoy:  # ADCP full data case
                    td = pd.Timedelta('30 days')
                # need to make sure dates are all in same time zone
                if date.tzinfo.zone == dend.tzinfo.zone:  # if time zones the same, don't change either
                    daystoread = min(td, dend-date)
                else:  # convert dend to utc
                    daystoread = min(td, dend.tz_convert('UTC')-date)
                dftemp = read_buoy(buoy, date, date+daystoread, table=table, units=units,
                                   usemodel=usemodel, userecent=userecent)
                if df is not None:
                    df = df.append(dftemp, sort=False)
                else:  # if df is None, rename dftemp to df
                    df = dftemp
                date += pd.Timedelta(daystoread) + pd.Timedelta('1 day')

    # return None instead of just header if no data for time period
    if df is not None and not df.empty:
        df.index.name = 'Dates [UTC]'
        df = df.tz_localize('UTC')  # all files are read in utc
        df = tools.convert_units(df, units=units, tz=tz)  # change units if necessary
        if dstart is not None:
            df = df.loc[(df.index > dstart) & (df.index < dend)]
        df = df.astype(float)  # makes sure that all columns are floats for consistency
    else:
        df = None

    # Convert sea level datum from MSL to whatever user chose
    if datum != 'MSL' and bys.loc[buoy,'table1'] in ['tcoon', 'tcoon-tide', 'nos', 'nos-water', 'nos-cond']:  # it is 'MSL' by default
        key = 'Water Level [m, MSL]'
        dz = tools.datum(buoy, datum)  # finds delta z between datums
        df[key] += dz
        # Change column label to include new datum
        df.rename(columns={key: key.replace('MSL', datum)}, inplace=True)

    return df


def read_buoy(buoy, dstart, dend, table=None, units=None,
         usemodel=False, userecent=True, datum='MSL'):

    # need table if TABS buoy
    if len(buoy) == 1:
        assert table is not None, 'need to input table when using TABS buoy'

    # if/elif statements checking which table type buoy has
    # ports check more complicated in case reading in full data
    if 'ports' in bys.loc[buoy.split('_')[0],'table1']:
        if 'full' in buoy:
            df = read_ports_depth(buoy, dstart, dend)
        else:
            df = read_ports(buoy, dstart, dend, usemodel=usemodel)
    elif 'tcoon' in bys.loc[buoy,'table1'] or 'nos' in bys.loc[buoy,'table1']:
        df = read_nos(buoy, dstart, dend, usemodel=usemodel)
    elif 'ndbc' in bys.loc[buoy,'table1']:  # whether or not in mysql database
        df = read_ndbc(buoy, dstart, dend, userecent=userecent)
    elif len(buoy) == 1:  # tabs buoys
        # sum goes across tables
        dfs = []
        if table == 'sum':
            dfs.append(read_tabs('ven', buoy, dstart, dend))
            if isinstance(bys.loc[buoy,'table3'], str) and 'salt' in bys.loc[buoy,'table3']:
                # drop water temp from here so that there aren't two in dataframe
                dfs.append(read_tabs('salt', buoy, dstart, dend).drop(['WaterT [deg C]'], axis=1))
            if isinstance(bys.loc[buoy,'table4'], str) and 'met' in bys.loc[buoy,'table4']:
                dfs.append(read_tabs('met', buoy, dstart, dend))
            # combine tables together
            df = pd.concat([df for df in dfs], axis=1, sort=False)

        else:
            df = read_tabs(table, buoy, dstart, dend)

    return df


def read_ports_depth(buoy, dstart, dend):
    '''Set up urls and read from them to get PORTS currents with depth or cross channel.'''

    buoy = buoy.split('_')[0]  # remove '_full' on buoyname

    url = 'https://opendap.co-ops.nos.noaa.gov/ioos-dif-sos/SOS?service=SOS&request=GetObservation&version=1.0.0&observedProperty=sea_water_speed&direction_of_sea_water_velocity&offering=urn:ioos:station:NOAA.NOS.CO-OPS:' + buoy + '&responseFormat=text/csv&eventTime='
    dst = pd.Timestamp(dstart)
    den = pd.Timestamp(dend)
    url += dst.strftime('%Y-%m-%dT00:00:00Z/') + den.strftime('%Y-%m-%dT23:59:00Z')

    # along-channel direction
    diralong = 90 - bys.loc[buoy,'angle']
    if diralong < 0:
        diralong += 360

    df = read_ports_depth_df(url, diralong)

    return df


def read_ports_depth_df(dataname, diralong):

    # read in data for month
    # first check there is data
    try:
        df = pd.read_csv(dataname, parse_dates=True, index_col=4)
    except:
        return None

    if df.empty:
        return None

    theta = df['direction_of_sea_water_velocity (degree)'].copy()
    # convert to math angles
    theta = 90 - theta
    theta[theta<0] += 360

    # calculate u and v
    east = df['sea_water_speed (cm/s)']*np.cos(np.deg2rad(theta))
    north = df['sea_water_speed (cm/s)']*np.sin(np.deg2rad(theta))

    # calculate along and across velocity
    df['Along [cm/s]'] = (east*np.cos(np.deg2rad(diralong)) + north*np.sin(np.deg2rad(diralong)))
    df['Across [cm/s]'] = (-east*np.sin(np.deg2rad(diralong)) + north*np.cos(np.deg2rad(diralong)))

    if df['orientation'][0] == 'downwardLooking':
        dz = df['bin_size (m)'][0]
        # add depth information for center of bins
        df['Depth to center of bin [m]'] = df['bin_distance (m)'] + dz/2
        df.rename(columns={'bin_distance (m)': 'Depth to top of bin [m]'}, inplace=True)
        # change depths to negative
        df['Depth to center of bin [m]'] = -df['Depth to center of bin [m]']
        df['Depth to top of bin [m]'] = -df['Depth to top of bin [m]']

    elif df['orientation'][0] == 'sidewaysLooking':
        df['Depth to center of bin [m]'] = df['sensor_depth (m)']
        df.rename(columns={'bin_distance (m)': 'Distance to center of bin [m]'}, inplace=True)
        # change depths to negative
        df['Depth to center of bin [m]'] = -df['Depth to center of bin [m]']


    df.rename(columns={'sea_water_temperature (C)': 'WaterT [deg C]',
                           'sea_water_speed (cm/s)': 'Speed [cm/s]',
                           'direction_of_sea_water_velocity (degree)': 'Dir [deg T]'}, inplace=True)

    # change this to drop instead
    df = df.drop(['station_id','sensor_id','latitude (degree)',
                   'longitude (degree)','sensor_depth (m)',
                   'platform_orientation (degree)',
                   'platform_pitch_angle (degree)',
                   'platform_roll_angle (degree)','orientation',
                   'sampling_rate (Hz)','reporting_interval (s)',
                   'processing_level','bin_size (m)','first_bin_center (m)',
                   'number_of_bins','bin (count)'], axis=1)

    df.index.rename('Dates [UTC]', inplace=True)
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
        diralong = 90 - bys.loc[buoy,'angle']
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
    This calls to read_nos_df() to do the reading and rearranging.
    dstart and dend are datetime objects.
    '''

    if not usemodel:
        # tide, met, and phys data
        prefixes = ['https://tidesandcurrents.noaa.gov/api/datagetter?product=water_level&application=NOS.COOPS.TAC.WL&station=',
                    'https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?product=air_pressure&application=NOS.COOPS.TAC.MET&station=',
                    'https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?product=air_temperature&application=NOS.COOPS.TAC.MET&station=',
                    'https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?product=wind&application=NOS.COOPS.TAC.MET&station=',
                    'https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?product=water_temperature&application=NOS.COOPS.TAC.PHYSOCEAN&station=',
                    'https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?product=conductivity&application=NOS.COOPS.TAC.PHYSOCEAN&station=']
        # dstart and dend need to be in format YYYYMMDD
        dstarts = dstart.strftime('%Y%m%d')
        dends = dend.strftime('%Y%m%d')
        suffixes = ['&begin_date=' + dstarts + '&end_date=' + dends + '&datum=MSL&units=metric&time_zone=GMT&format=csv',
                    '&begin_date=' + dstarts + '&end_date=' + dends + '&time_zone=GMT&units=english&interval=6&format=csv',
                    '&begin_date=' + dstarts + '&end_date=' + dends + '&time_zone=GMT&units=english&interval=6&format=csv',
                    '&begin_date=' + dstarts + '&end_date=' + dends + '&time_zone=GMT&units=english&interval=6&format=csv',
                    '&begin_date=' + dstarts + '&end_date=' + dends + '&time_zone=GMT&units=english&interval=6&format=csv',
                    '&begin_date=' + dstarts + '&end_date=' + dends + '&time_zone=GMT&units=english&interval=6&format=csv']
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
            df = pd.concat([df for df in dfs if not df.empty], axis=1, sort=False)
        else:
            df = pd.concat([df for df in dfs], axis=1, sort=False)

        # calculate salinity from conductivity, if available
        if 'Conductivity [mS/cm]' in df.keys():
            if not 'AtmPr [mb]' in df.keys():
                pr = np.zeros(len(df))
            else:
                pr = df['AtmPr [mb]']/100. - 10.1325
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
    '''Read in individual tcoon/nos datasets and arrange variables.'''

    df = pd.read_csv(dataname, parse_dates=[0], index_col=0)
         
    if 'product=water_level' in dataname:
        names = ['Water Level [m, MSL]']
        df = df.drop([' Sigma', ' O', ' F', ' R', ' L', ' Quality ', ' O or I (for verified)'], axis=1, errors='ignore')
        # dictionary for rounding decimal places
        rdict = {}

    elif 'air_pressure' in dataname:
        names = ['AtmPr [mb]']
        df = df.drop([' X', ' N', ' R'], axis=1, errors='ignore')
        # dictionary for rounding decimal places
        rdict = {}

    elif 'air_temperature' in dataname:
        names = ['AirT [deg C]']
        df = df.drop([' X', ' N', ' R'], axis=1, errors='ignore')
        # dictionary for rounding decimal places
        rdict = {}

    elif 'wind' in dataname:
        names = ['Speed [m/s]', 'Dir from [deg T]', 'Gust [m/s]', 'East [m/s]', 'North [m/s]']
        df = df.drop([' Direction.1', ' X', ' R'], axis=1, errors='ignore')
        # dictionary for rounding decimal places
        rdict = {'East [m/s]': 2, 'North [m/s]': 2}

        # angle needs to be in math convention for trig and between 0 and 360
        # also have to switch wind from direction from to direction to with 180 switch
        theta = 90 - (df[' Direction'] - 180)
        theta[theta<0] += 360
        df['East [m/s]'] = df[' speed']*np.cos(np.deg2rad(theta))
        df['North [m/s]'] = df[' speed']*np.sin(np.deg2rad(theta))
        # dictionary for rounding decimal places
        rdict = {}
         
    elif 'water_temperature' in dataname:
        names = ['WaterT [deg C]']
        df = df.drop([' X', ' N', ' R'], axis=1, errors='ignore')
        # dictionary for rounding decimal places
        rdict = {}
         
    elif 'conductivity' in dataname:
        names = ['Conductivity [mS/cm]']
        df = df.drop([' X', ' N', ' R'], axis=1, errors='ignore')
        # dictionary for rounding decimal places
        rdict = {}

    elif 'prediction' in dataname:  # tidal height prediction
        names = ['Water Level [m, MSL]']
        # dictionary for rounding decimal places
        rdict = {}

    # remove error message from when data is missing
    if not df.empty:
        if isinstance(df.index[0], str):
            df = df.drop(df.index[0], axis=0)
            df = pd.DataFrame()
    if not df.columns.empty:
        df.columns = names
        df.index.name = 'Dates [UTC]'
        df = df.round(rdict)

    return df


def read_ndbc(buoy, dstart, dend, userecent=True):
    '''Set up to read in NDBC buoy data (from mysql or website).

    Call to read_ndbc_df to do actually reading in.
    userecent=True will use recent 45 days of data. userecent=False will not.
    '''

    if bys.loc[buoy,'inmysql']:  # mysql

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
        names = ['Speed [m/s]', 'Dir from [deg T]', 'Gust [m/s]', 'AtmPr [mb]', 'AirT [deg C]', 'Dew pt [deg C]', 'WaterT [deg C]', 'RelH [%]', 'Wave Ht [m]', 'Wave Pd [s]', 'East [m/s]', 'North [m/s]']
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
        names = ['Dir from [deg T]', 'Speed [m/s]', 'Gust [m/s]', 'AtmPr [mb]', 'AirT [deg C]', 'WaterT [deg C]', 'Dew pt [deg C]', 'East [m/s]', 'North [m/s]']

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

    Time from database is in UTC. dstart, dend are datetime objects.
    Time zone information from dstart,dend is ignored. This is in UTC.'''

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
        # drop compass column — what even is it?
        df.drop(['compass'], inplace=True, axis=1)
        names = ['East [cm/s]', 'North [cm/s]', 'WaterT [deg C]', 'Tx', 'Ty', 'Speed [cm/s]', 'Across [cm/s]', 'Along [cm/s]', 'Dir [deg T]']            # df.columns = names
        df['Speed [cm/s]'] = np.sqrt(df['veast']**2 + df['vnorth']**2)
        df['Speed [cm/s]'] = df['Speed [cm/s]'].round(2)
        # Calculate along- and across-shelf
        # along-shelf rotation angle in math angle convention
        theta = np.deg2rad(-(bys.loc[buoy,'angle']-90))  # convert from compass to math angle
        df['Across [cm/s]'] = df['veast']*np.cos(-theta) - df['vnorth']*np.sin(-theta)
        df['Along [cm/s]'] = df['veast']*np.sin(-theta) + df['vnorth']*np.cos(-theta)
        # calculate direction that currents are pointing toward. This is not "compass".
        # calculate math direction from east/north currents, direction to,
        # then convert to compass angles. Then add 360 if negative.
        dto = 90 - np.rad2deg(np.arctan2(df['vnorth'], df['veast']))
        dto[dto<0] += 360
        df['Dir [deg T]'] = dto
        # dictionary for rounding decimal places
        rdict = {'Speed [cm/s]': 2, 'Across [cm/s]': 2, 'Along [cm/s]': 2, 'Dir [deg T]': 0}

    elif table == 'eng':
        names = ['VBatt [Oper]', 'SigStr [dB]', 'Comp [deg M]', 'Nping', 'Tx', 'Ty', 'ADCP Volt', 'ADCP Curr', 'VBatt [sleep]']
        rdict = {}

    elif table == 'met':
        names = ['East [m/s]', 'North [m/s]', 'AirT [deg C]', 'AtmPr [mb]', 'Gust [m/s]', 'Comp [deg M]', 'Tx', 'Ty', 'PAR ', 'RelH [%]', 'Speed [m/s]', 'Dir from [deg T]']
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



def calc_z(ds, zeta=0):
    '''Calculate depths for model output for mean sea level.

    Can input time-varying sea level height (zeta) if desired.
    '''

    if ds.Vtransform == 1:
        Zo_rho = ds.hc * (ds.s_rho - ds.Cs_r) + ds.Cs_r * ds.h
        z_rho = Zo_rho + zeta * (1 + Zo_rho/ds.h)
        Zo_w = ds.hc * (ds.s_w - ds.Cs_w) + ds.Cs_w * ds.h
        z_w = Zo_w + zeta * (1 + Zo_w/ds.h)
    elif ds.Vtransform == 2:
        Zo_rho = (ds.hc * ds.s_rho + ds.Cs_r * ds.h) / (ds.hc + ds.h)
        z_rho = zeta + (zeta + ds.h) * Zo_rho
        Zo_w = (ds.hc * ds.s_w + ds.Cs_w * ds.h) / (ds.hc + ds.h)
        z_w = zeta + (zeta + ds.h) * Zo_w

    ds.coords['z_rho'] = z_rho.transpose()   # needing transpose seems to be an xarray bug
    ds.coords['z_w'] = z_w.transpose()

    return ds


def read_model(buoy, which, dstart, dend, timing='recent', units='Metric',
               tz='utc', s_rho=-1):
    '''Read in model output.

    dstart and dend are datetime objects.
    s_rho (-1, surface) is the index of model output depth. -1 for surface, a
      number between 0 and 29 for other depth levels, and -999 for all depths.
    '''

    # separate out which model type we want
    # links in list are in order they are tried by the system
    if timing == 'hindcast':
        locs = ['http://barataria.geos.tamu.edu:8080/thredds/dodsC/NcML/txla_hindcast_sta',
                'http://copano.geos.tamu.edu:8080/thredds/dodsC/NcML/txla_hindcast_sta',
                'http://barataria.geos.tamu.edu:6060/thredds/dodsC/NcML/txla_hindcast_sta']
    elif timing == 'recent':
        locs = ['http://barataria.geos.tamu.edu:8080/thredds/dodsC/NcML/forecast_stn_archive_agg.nc',
                'http://barataria.geos.tamu.edu:8080/thredds/dodsC/NcML/forecast_stn_archive2_agg.nc']
    elif timing == 'forecast':
        locs = ['http://barataria.geos.tamu.edu:8080/thredds/dodsC/forecast_latest/txla2_stn_f_latest.nc',
                'http://barataria.geos.tamu.edu:6060/thredds/dodsC/forecast_latest/txla2_stn_f_latest.nc',
                'http://copano.geos.tamu.edu:8080/thredds/dodsC/forecast_latest/txla2_stn_f_latest.nc']


    varstot = ['u', 'v', 'temp', 'salt', 'dye_01', 'dye_02', 'dye_03', 'dye_04',
               'Uwind', 'Vwind', 'Pair', 'Tair', 'Qair', 'zeta', 'shflux', 'sustr', 'svstr']

    # Try different locations for model output. If won't work, give up.
    # loop over station files first since faster if can use, then regular files
    ibuoy = bys.loc[buoy,'station_number']  # get location in stations file for buoy

    # stop if no station for buoy
    if np.isnan(ibuoy):
        return None
    else:
        ibuoy = int(ibuoy)

    for i, loc in enumerate(locs):
        try:
            ds = xr.open_dataset(loc)
            # make sure all variables present
            assert np.asarray([var in ds for var in varstot]).all(), 'required variables are not all present\n'
            # make sure any variable value is accessible to see if there is
            # secretly a netcdf problem
            assert ds['u'][0,0,0], 'actual model value cannot be accessed\n'
            # calculate depths at model layers
            ds = calc_z(ds, zeta=0)
            # make sure desired end date is after model start date
            assert dend >= pd.Timestamp(ds['ocean_time'].isel(ocean_time=0).values, tz='utc'), 'desired start date is not included in model time range\n'
            # make sure desired start date is before model end date
            assert dstart <= pd.Timestamp(ds['ocean_time'].isel(ocean_time=-1).values, tz='utc'), 'desired end date is not included in model time range\n'
            break
        except AssertionError as e:
            logger_read.warning('AssertionError.\n')
            logger_read.exception(e, exc_info=True)
        except KeyError as e:
            logger_read.warning('KeyError.\n')
            logger_read.exception(e, exc_info=True)
        except RuntimeError as e:
            logger_read.warning('RuntimeError.\n')
            logger_read.exception(e, exc_info=True)
        except IOError as e:  # if link tried is not working
            logger_read.warning('IOError.\n')
            logger_read.exception(e, exc_info=True)
        except Exception as e:
            logger_read.warning('Unexpected exception')
            logger_read.exception(e, exc_info=True)

        logger_read.warning('Model timing: %s.\nBuoy %s.\nModel location: %s\n\n' % (timing, buoy, loc))

        if i == len(locs)-1:  # no more options to try
            logger_read.warning('\n\nNo more model input options.\n\n\n')
            ds = None
            df = None
            return df

    vars = ['u', 'v', 'temp', 'salt', 'dye_01', 'dye_02', 'dye_03', 'dye_04']
    varnames = ['Along [cm/s]', 'Across [cm/s]', 'WaterT [deg C]', 'Salinity',
                'Dissolved oxygen concentration [uM]',
                'Mississippi passive tracer', 'Atchafalaya passive tracer',
                'Brazos passive tracer']
    vars_w = ['w']  # on vertical grid w
    varnames_w = ['Vertical velocity [m/s]']
    if s_rho == -999:  # all depths at once
        # don't add 2d variables if all depths requested
        for i in range(nrepeats):  # repeat multiple times if needed
            try:
                df = ds[vars].sel(ocean_time=slice(dstart.tz_localize(None), dend.tz_localize(None))).isel(station=ibuoy).to_dataframe()
                break
            except RuntimeError as e:
                logger_read.warning(e, exc_info=True)
                logger_read.warning('\nAttempt %i: For model timing %s, buoy %s, loc %s, and s_rho %d, extracting model output did not work due to a RuntimeError.\n' % (i+1, timing, buoy, loc, s_rho))
            except Exception as e:
                logger_read.warning(e, exc_info=True)
                logger_read.warning('\nAttempt %i: For model timing %s, buoy %s, loc %s, and s_rho %d, extracting model output did not work due to a different error.\n' % (i+1, timing, buoy, loc, s_rho))
            if i+1 == nrepeats:  # time to give up
                logger_read.warning('No more attempts. For model timing %s, buoy %s, loc %s, and s_rho %d, extracting model output did not work.\n\n\n' % (timing, buoy, loc, s_rho))
                df = None
                return df

        # depths info needed: all depths, one station
        zr = ds.z_rho.isel(station=ibuoy)

        df = df.reset_index(['s_rho'])
        # df['s_rho'] = np.tile(zr, int(len(df)/zr.size))

        df2 = ds[vars_w].sel(ocean_time=slice(dstart, dend)).isel(station=ibuoy).to_dataframe()
        zw = ds.z_w.isel(station=ibuoy)
        df2 = df2.reset_index(['s_w'])
        df2['s_w'] = np.tile(zw, int(len(df2)/zw.size))
        # df2.rename(columns={'s_w': 'Depth [m]'}, inplace=True)
        df2.drop(['lon_rho', 'lat_rho', 's_w'], axis=1, inplace=True, errors='ignore')

        # interpolate ws to rho vertical grid
        df['w'] = np.nan
        ii = 0
        for i in range(0,int(len(df2)/31),31):
            # i is for df2, ii is for df
            df['w'].iloc[ii*30:ii*30+30] = (df2['w'][i:i+30] + df2['w'][i+1:i+31])/2
            ii += 1

    else:
        if s_rho in [-1, 29]:  # surface, more variables
            vars += ['Uwind', 'Vwind', 'Pair',
                    'Tair', 'Qair', 'zeta',
                      'shflux', 'sustr', 'svstr']
            varnames += ['East [m/s]', 'North [m/s]', 'AtmPr [mb]', 'AirT [deg C]',
                        'RelH [%]', 'Free surface [m]', 'Surface net heat flux [W/m^2]',
                        'Surface u-momentum stress [N/m^2]', 'Surface v-momentum stress [N/m^2]']
        for i in range(nrepeats):  # repeat multiple times if needed
            try:
                df = ds[vars].sel(ocean_time=slice(dstart.tz_localize(None), dend.tz_localize(None))).isel(station=ibuoy, s_rho=s_rho).to_dataframe()
                break
            except RuntimeError as e:
                logger_read.warning(e, exc_info=True)
                logger_read.warning('\nAttempt %i: For model timing %s, buoy %s, loc %s, and s_rho %d, extracting model output did not work due to a RuntimeError.\n' % (i+1, timing, buoy, loc, s_rho))
            except Exception as e:
                logger_read.warning(e, exc_info=True)
                logger_read.warning('\nAttempt %i: For model timing %s, buoy %s, loc %s, and s_rho %d, extracting model output did not work due to a different error.\n' % (i+1, timing, buoy, loc, s_rho))
            if i+1 == nrepeats:  # time to give up
                logger_read.warning('No more attempts. For model timing %s, buoy %s, loc %s, and s_rho %d, extracting model output did not work.\n\n\n' % (timing, buoy, loc, s_rho))
                df = None
                return df

        df = df.reset_index(level=0).set_index('ocean_time')

        # depths info needed: all depths, one station
        zr = ds.z_rho.isel(s_rho=s_rho, station=ibuoy)

    # adjustments
    df['s_rho'] = np.tile(zr, int(len(df)/zr.size))
    df.rename(columns={'s_rho': 'Depth [m]'}, inplace=True)
    df.index.rename('Dates [UTC]', inplace=True)
    df.drop(['lon_rho', 'lat_rho', 's_w'], axis=1, inplace=True, errors='ignore')
    df.rename(columns={var: varname for var, varname in zip(vars, varnames)}, inplace=True)
    df['Density [kg/m^3]'] = gsw.rho(df['Salinity'], df['WaterT [deg C]'], np.zeros(len(df)))
    if s_rho in [-1, 29]:
        df['RelH [%]'] *= 100

    # un-rotate velocities, then rerotate to match TABS website angles
    # also convert to cm/s
    df['Along [cm/s]'] *= 100
    df['Across [cm/s]'] *= 100
    # rotate from curvilinear to cartesian
    anglev = ds['angle'][ibuoy]  # using at least nearby grid rotation angle
    # Project along- and across-shelf velocity rather than use from model
    # so that angle matches buoy
    df['East [cm/s]'], df['North [cm/s]'] = tools.rot2d(df['Along [cm/s]'], df['Across [cm/s]'], anglev)  # approximately to east, north
    theta = np.deg2rad(-(bys.loc[buoy,'angle']-90))  # convert from compass to math angle
    if ~np.isnan(theta):
        df['Across [cm/s]'] = df['East [cm/s]']*np.cos(-theta) - df['North [cm/s]']*np.sin(-theta)
        df['Along [cm/s]'] = df['East [cm/s]']*np.sin(-theta) + df['North [cm/s]']*np.cos(-theta)

    return df
