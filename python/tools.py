'''
Useful functions
'''


import numpy as np
import pandas as pd
from matplotlib.dates import date2num
import buoy_data as bd
from prettypandas import PrettyPandas
from sqlalchemy import create_engine
import xarray as xr
import gsw


def convert(vin, which):
    '''Convert units.'''

    if which == 'c2f':  # celsius to fahrenheit
        return vin*1.8+32
    elif which == 'mps2kts':  # m/s to knots
        return vin*1.943844
    elif which == 'cps2kts':  # cm/s to knots
        return vin*0.0194384
    elif which == 'mb2hg':  # MB to inHg
        return vin*0.029529983071415973
    elif which == 'm2ft':  # meters to feet
        return vin*3.28084


def degrees_to_cardinal(d):
    '''
    note: this is highly approximate...
    https://gist.github.com/RobertSudwarts/acf8df23a16afdb5837f
    '''
    dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
            "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    ix = int((d + 11.25)/22.5)
    return dirs[ix % 16]


def read(dataname, units='M', tz='UTC'):
    '''Load in data already saved into /tmp file by tabsquery.php

    Time from database is in UTC.

    if dataname is a string, it is a file location. If it is a list with two
    entries, they give the query string and the mysql engine.
    '''

    # read method: from a file or from mysql
    if isinstance(dataname, str):
        # columns have already been processed previously and can be inferred
        df = pd.read_table(dataname, parse_dates=[0], index_col=0, na_values='-999')
    elif len(dataname) == 2:
        query = dataname[0]; engine = dataname[1]
        df = pd.read_sql_query(query, engine, index_col=['obs_time'])
        if 'tabs' in query:
            buoy = query.split(' ')[3].split('_')[1]
            which = query.split(' ')[3].split('_')[2]
        elif 'ndbc' in query:
            buoy = query.split(' ')[3].split('_')[1]
            which = query.split(' ')[3].split('_')[0]

        if which == 'ven':# or which == 'sum':
            ind = df['tx']==-99
            df.drop(df.index[ind], inplace=True)  # drop bad rows
            names = ['East [cm/s]', 'North [cm/s]', 'Dir [deg T]', 'WaterT [deg C]', 'Tx', 'Ty', 'Speed [cm/s]', 'Across [cm/s]', 'Along [cm/s]']            # df.columns = names
            df['Speed [cm/s]'] = np.sqrt(df['veast']**2 + df['vnorth']**2)
            df['Speed [cm/s]'] = df['Speed [cm/s]'].round(2)
            # Calculate along- and across-shelf
            # along-shelf rotation angle in math angle convention
            theta = np.deg2rad(-(bd.angle(buoy)-90))  # convert from compass to math angle
            df['Across [cm/s]'] = df['veast']*np.cos(-theta) - df['vnorth']*np.sin(-theta)
            df['Along [cm/s]'] = df['veast']*np.sin(-theta) + df['vnorth']*np.cos(-theta)
            # dictionary for rounding decimal places
            rdict = {'Speed [cm/s]': 2, 'Across [cm/s]': 2, 'Along [cm/s]': 2, 'Dir [deg T]': 0}

        elif which == 'eng':
            names = ['VBatt [Oper]', 'SigStr [dB]', 'Comp [deg M]', 'Nping', 'Tx', 'Ty', 'ADCP Volt', 'ADCP Curr', 'VBatt [sleep]']
            rdict = {}

        elif which == 'met':
            names = ['East [m/s]', 'North [m/s]', 'AirT [deg C]', 'AtmPr [MB]', 'Gust [m/s]', 'Comp [deg M]', 'Tx', 'Ty', 'PAR ', 'RelH [%]', 'Speed [m/s]', 'Dir from [deg T]']
            df['Speed [m/s]'] = np.sqrt(df['veast']**2 + df['vnorth']**2)
            df['Dir from [deg T]'] = 90 - np.rad2deg(np.arctan2(-df['vnorth'], -df['veast']))
            rdict = {'Speed [m/s]': 2, 'Dir from [deg T]': 0}

        elif which == 'salt':
            names = ['Temp [deg C]', 'Cond [ms/cm]', 'Salinity', 'Density [kg/m^3]', 'SoundVel [m/s]']
            rdict = {}

            # density is all 0s, so need to overwrite
            df['density'] = gsw.rho(df['salinity'], df['twater'], np.zeros(len(df)))

        elif which == 'wave':
            names = ['WaveHeight [m]', 'MeanPeriod [s]', 'PeakPeriod [s]']
            rdict = {}

        elif which == 'ndbc':
            names = ['Speed [m/s]', 'Dir from [deg T]', 'Gust [m/s]', 'AtmPr [MB]', 'AirT [deg C]', 'Dew pt [deg C]', 'WaterT [deg C]', 'RelH [%]', 'Wave Ht [m]', 'Wave Pd [s]', 'East [m/s]', 'North [m/s]']
            df = df.drop(['station', 'windgust2'], axis=1)
            rdict = {'East [m/s]': 2, 'North [m/s]': 2}

            # angle needs to be in math convention for trig and between 0 and 360
            # also have to switch wind from direction from to direction to with 180 switch
            theta = 90 - (df['winddir'] - 180)
            theta[theta<0] += 360
            df['East [m/s]'] = df['windspeed']*np.cos(np.deg2rad(theta))
            df['North [m/s]'] = df['windspeed']*np.sin(np.deg2rad(theta))

            # first remove calculate values (East, North) if associated with nan's
            ind = (df['windspeed']==-99.0) | (df['winddir']==-99.0)
            df.loc[ind, 'East [m/s]'] = np.nan
            df.loc[ind, 'North [m/s]'] = np.nan
            # remove original missing values
            df.replace('-99.0', np.nan, inplace=True)

        if 'date' in df.columns:
            df = df.drop(['date','time'], axis=1)
        df.columns = names
        df.index.name = 'Dates [UTC]'
        df = df.round(rdict)

    if units == 'E':
        units_to_change = ['[cm/s]', '[m/s]', '[deg C]', '[MB]', '[m]']
        conversions = ['cps2kts', 'mps2kts', 'c2f', 'mb2hg', 'm2ft']
        new_units = ['[kts]', '[kts]', '[deg F]', '[inHg]', '[ft]']
        rints = [2, 2, 1, 2, 1]  # integers for number of decimal places for rounding
        for rint, newunit, unit, conversion in zip(rints, new_units, units_to_change, conversions):

            # the columns with these keys need to be converted
            cols_to_change = [col for col in df.columns if unit in col]

            # convert all columns that need converting for unit
            for col in cols_to_change:
                df[col] = convert(df[col], conversion)
                newname = col.replace(unit, newunit)
                df.rename(columns={col: newname}, inplace=True)
                df = df.round({newname: rint})

    if tz == 'central':  # time zone
        # need to first establish a time zone (which it is already in) to change it
        df = df.tz_localize('UTC')  # timezone is UTC
        df.index = df.index.tz_convert('US/Central')
        df.index.rename(df.index.name.replace('UTC', df.tail(1).index.strftime("%Z")[0]), inplace=True)

    return df


def rot2d(x, y, ang):
    '''rotate vectors by geometric angle. For model.'''
    xr = x*np.cos(ang) - y*np.sin(ang)
    yr = x*np.sin(ang) + y*np.cos(ang)
    return xr, yr


def read_model(query, timing='recent'):
    '''Read in model output based on data query q.'''

    if 'tabs' in query:
        buoy = query.split(' ')[3].split('_')[1]
        which = query.split(' ')[3].split('_')[2]
    elif 'ndbc' in query:
        buoy = query.split(' ')[3].split('_')[1]
        which = query.split(' ')[3].split('_')[0]
    dstart = query.split('"')[1]  # start date (beginning of day)
    dend = query.split('"')[3]  # end date and time
    # import pdb; pdb.set_trace()
    if timing == 'recent':
        loc = 'http://copano.tamu.edu:8080/thredds/dodsC/NcML/oof_archive_agg'
        locf = 'http://copano.tamu.edu:8080/thredds/dodsC/NcML/oof_archive_agg_frc'  # forcing info
    elif timing == 'forecast':
        loc = 'http://copano.tamu.edu:8080/thredds/dodsC/oof_other/roms_his_f_previous_day.nc'
        locf = 'http://copano.tamu.edu:8080/thredds/dodsC/oof_other/roms_frc_f_latest.nc'
    try:
        ds = xr.open_dataset(loc)
    except:
        loc = 'barataria'.join(loc.split('copano'))  # change to barataria thredds if copano won't work
        ds = xr.open_dataset(loc)
    if which == 'met' or which == 'ndbc':  # read in forcing info
        try:
            dsf = xr.open_dataset(locf)
        except:
            locf = 'barataria'.join(locf.split('copano'))  # change to barataria thredds if copano won't work
            dsf = xr.open_dataset(locf)

    # only do this if dend is less than or equal to the first date in the model output
    # check if last data datetime is less than 1st model datetime or
    # first data date is greater than last model time, so that time periods overlap
    # sometimes called ocean_time and sometimes time
    # if 'time' in ds:  # ocean_time should be repurposed with info from time
    #     ds['ocean_time'] = ds['time']
    #     ds = ds.swap_dims({'time': 'ocean_time'})
    if pd.datetime.strptime(dend, '%Y-%m-%d %H:%M') <= pd.to_datetime(ds['ocean_time'].isel(ocean_time=0).data) or \
       pd.datetime.strptime(dstart, '%Y-%m-%d') >= pd.to_datetime(ds['ocean_time'].isel(ocean_time=-1).data) :
        df = None
    else:
        # Initialize model dataframe with times
        df = pd.DataFrame(index=ds['ocean_time'].sel(ocean_time=slice(dstart, dend)))

        if which == 'ven':
            # model output needed for image
            j, i = bd.model(buoy, 'u')  # get model indices
            along = ds['u'].sel(ocean_time=slice(dstart, dend))\
                           .isel(s_rho=-1, eta_u=j, xi_u=i)*100  # convert to cm/s
            j, i = bd.model(buoy, 'v')  # get model indices
            across = ds['v'].sel(ocean_time=slice(dstart, dend))\
                            .isel(s_rho=-1, eta_v=j, xi_v=i)*100
            j, i = bd.model(buoy, 'rho')  # get model indices
            df['WaterT [deg C]'] = ds['temp'].sel(ocean_time=slice(dstart, dend)).isel(s_rho=-1, eta_rho=j, xi_rho=i)

            # rotate from curvilinear to cartesian
            anglev = ds['angle'][j,i]  # using at least nearby grid rotation angle
            df['East [cm/s]'], df['North [cm/s]'] = rot2d(along, across, anglev)  # approximately to east, north

            # Project along- and across-shelf velocity rather than use from model
            # so that angle matches buoy
            theta = np.deg2rad(-(bd.angle(buoy)-90))  # convert from compass to math angle
            df['Across [cm/s]'] = df['East [cm/s]']*np.cos(-theta) - df['North [cm/s]']*np.sin(-theta)
            df['Along [cm/s]'] = df['East [cm/s]']*np.sin(-theta) + df['North [cm/s]']*np.cos(-theta)

        elif which == 'salt':
            # model output needed for image
            j, i = bd.model(buoy, 'rho')  # get model indices
            df['temp'] = ds['temp'].sel(ocean_time=slice(dstart, dend)).isel(s_rho=-1, eta_rho=j, xi_rho=i)
            df['salt'] = ds['salt'].sel(ocean_time=slice(dstart, dend)).isel(s_rho=-1, eta_rho=j, xi_rho=i)

            # change names to match data
            df.columns = ['Temp [deg C]', 'Salinity']

            df['Density [kg/m^3]'] = gsw.rho(df['Salinity'], df['Temp [deg C]'], np.zeros(len(df)))

        elif which == 'ndbc':
            # model output needed for image
            j, i = bd.model(buoy, 'rho')  # get model indices
            df['temp'] = ds['temp'].sel(ocean_time=slice(dstart, dend)).isel(s_rho=-1, eta_rho=j, xi_rho=i)
            df['Uwind'] = ds['Uwind'].sel(ocean_time=slice(dstart, dend)).isel(eta_rho=j, xi_rho=i)
            df['Vwind'] = ds['Vwind'].sel(ocean_time=slice(dstart, dend)).isel(eta_rho=j, xi_rho=i)

            # change names to match data
            df.columns = ['WaterT [deg C]', 'East [m/s]', 'North [m/s]']

            df['AtmPr [MB]'] = dsf['Pair'].sel(time=slice(dstart, dend)).isel(eta_rho=j, xi_rho=i).to_dataframe()['Pair'].resample('60T').interpolate()

        elif which == 'met':
            # model output needed for image
            j, i = bd.model(buoy, 'rho')  # get model indices
            df['Uwind'] = ds['Uwind'].sel(ocean_time=slice(dstart, dend)).isel(eta_rho=j, xi_rho=i)
            df['Vwind'] = ds['Vwind'].sel(ocean_time=slice(dstart, dend)).isel(eta_rho=j, xi_rho=i)

            # change names to match data
            df.columns = ['East [m/s]', 'North [m/s]']

            df['AirT [deg C]'] = dsf['Tair'].sel(time=slice(dstart, dend)).isel(eta_rho=j, xi_rho=i).to_dataframe()['Tair'].resample('60T').interpolate()
            df['AtmPr [MB]'] = dsf['Pair'].sel(time=slice(dstart, dend)).isel(eta_rho=j, xi_rho=i).to_dataframe()['Pair'].resample('60T').interpolate()
            df['RelH [%]'] = dsf['Qair'].sel(time=slice(dstart, dend)).isel(eta_rho=j, xi_rho=i).to_dataframe()['Qair'].resample('60T').interpolate()

        # can't use datetime index directly unfortunately here, so can't use pandas later either
        df.idx = date2num(df.index.to_pydatetime())  # in units of days

    return df


def present(df):
    '''Present dataframe df nicely by printing to screen'''

    # formatters={'AtmPr [MB]':'{:,.2f}'.format}
    # myformatter = lambda x: '[%4.1f]' % x
    # formatters={'AtmPr [MB]': myformatter}
    # print(PrettyPandas(df, formatters=formatters).render())
    # twodigits = PrettyPandas.as_unit('', subset=None, precision=None)
    # formats = PrettyPandas(df).as_unit('', )
    # print('<br><br>')
    print(PrettyPandas(df).render())
    # print(df)


def engine():
    '''Setup database engine for mysql querying.'''

    engine = create_engine('mysql+mysqlconnector://tabsweb:tabs@tabs1.gerg.tamu.edu/tabsdb')

    return engine
