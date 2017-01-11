'''
Useful functions
'''


import numpy as np
import pandas as pd
from matplotlib.dates import date2num
import buoy_data
from prettypandas import PrettyPandas
from sqlalchemy import create_engine


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


def read_ind(dataname):
    '''Read from mysql but just to get indices for reading in recent data.'''
    query = dataname[0]; engine = dataname[1]
    df = pd.read_sql_query(query, engine, index_col=['obs_time'])
    return df['tx']==-99  # bad rows in ven table


# def read(dataname, buoy=None, which=None, units='M'):
def read(dataname, units='M', ind=None):
    '''Load in data already saved into /tmp file by tabsquery.php

    Time is in UTC.

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
        if ind is not None:
            df.drop(df.index[ind], inplace=True)
        buoy = query.split(' ')[3].split('_')[1]
        which = query.split(' ')[3].split('_')[2]

        if which == 'ven':# or which == 'sum':
            names = ['East [cm/s]', 'North [cm/s]', 'Dir [deg T]', 'WaterT [deg C]', 'Tx', 'Ty', 'Speed [cm/s]', 'Across [cm/s]', 'Along [cm/s]']            # df.columns = names
            df['Speed [cm/s]'] = np.sqrt(df['veast']**2 + df['vnorth']**2)
            df['Speed [cm/s]'] = df['Speed [cm/s]'].round(2)
            # Calculate along- and across-shelf
            # along-shelf rotation angle in math angle convention
            theta = np.deg2rad(-(buoy_data.angle(buoy)-90))  # convert from compass to math angle
            df['Across [cm/s]'] = df['veast']*np.cos(-theta) - df['vnorth']*np.sin(-theta)
            df['Along [cm/s]'] = df['veast']*np.sin(-theta) + df['vnorth']*np.cos(-theta)
            # dictionary for rounding decimal places
            rdict = {'Speed [cm/s]': 2, 'Across [cm/s]': 2, 'Along [cm/s]': 2, 'Dir [deg T]': 0}
            # rdict = {'Speed [cm/s]': 2, 'Across [cm/s]': 2, 'Along [cm/s]': 2,
            #           'WaterT [deg C]': 1, 'Dir [deg T]': 0}

        elif which == 'eng':
            names = ['VBatt [Oper]', 'SigStr [dB]', 'Comp [deg M]', 'Nping', 'Tx', 'Ty', 'ADCP Volt', 'ADCP Curr', 'VBatt [sleep]']
            rdict = {}

        elif which == 'met':
            names = ['East [m/s]', 'North [m/s]', 'AirT [deg C]', 'AtmPr [MB]', 'Gust [m/s]', 'Comp [deg M]', 'Tx', 'Ty', 'PAR ', 'RelH [%]', 'Speed [m/s]', 'Dir from [deg T]']
            df['Speed [m/s]'] = np.sqrt(df['veast']**2 + df['vnorth']**2)
            df['Dir from [deg T]'] = 90 - np.rad2deg(np.arctan2(-df['vnorth'], -df['veast']))
            rdict = {'Speed [m/s]': 2, 'Dir from [deg T]': 0}
            # rdict = {'East [m/s]': 2, 'North [m/s]': 2, 'AtmPr [MB]': 1,
            #           'Speed [m/s]': 2, 'Dir from [deg T]': 0}

        elif which == 'salt':
            names = ['Temp [deg C]', 'Cond [ms/cm]', 'Salinity', 'Density [kg/m^3]', 'SoundVel [m/s]']
            rdict = {}
            # rdict = {'Temp [deg C]': 1}

        elif which == 'wave':
            names = ['WaveHeight [m]', 'MeanPeriod [s]', 'PeakPeriod [s]']
            rdict = {}
            # rdict = {'WaveHeight [m]': 2, 'MeanPeriod [s]': 0, 'PeakPeriod [s]': 0}

        # if which == 'sum':  # add onto read in from ven if sum
        #     names = ['Date', 'Time', 'Temp', 'Cond', 'Salinity', 'Density', 'SoundVel']
        #     df2 = pd.read_table(dataname, parse_dates=[[0,1]], delim_whitespace=True, names=names, index_col=0, na_values='-999')
        #     df['Salinity'] = df2['Salinity']  # from salt file
        #     df['Temp'] = df2['Temp']  # from salt file

        df = df.drop(['date','time'], axis=1)
        df.columns = names
        df.index.name = 'Dates [UTC]'
        # import pdb; pdb.set_trace()
        df = df.round(rdict)

    # can't use datetime index directly unfortunately here, so can't use pandas later either
    df.idx = date2num(df.index.to_pydatetime())  # in units of days
    df.dT = df.idx[-1] - df.idx[0]  # length of dataset in days

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

    return df


def present(df):
    '''Present dataframe df nicely by printing to screen'''

    # formatters={'AtmPr [MB]':'{:,.2f}'.format}
    # myformatter = lambda x: '[%4.1f]' % x
    # formatters={'AtmPr [MB]': myformatter}
    # print(PrettyPandas(df, formatters=formatters).render())
    # twodigits = PrettyPandas.as_unit('', subset=None, precision=None)
    # formats = PrettyPandas(df).as_unit('', )
    print(PrettyPandas(df).render())
    # print(df)


def engine():
    '''Setup database engine for mysql querying.'''

    engine = create_engine('mysql+mysqldb://tabsweb:tabs@tabs1.gerg.tamu.edu/tabsdb')

    return engine
