'''
Useful functions
'''


from math import sin, cos
from sqlalchemy import create_engine
import pandas as pd
from csv import QUOTE_NONE
from numpy import sign


def setup_engine():
    '''Setup database engine for mysql querying.'''

    engine = create_engine('mysql+mysqlconnector://tabsweb:tabs@tabs1.gerg.tamu.edu/tabsdb')

    return engine


def query_setup_recent(engine, buoy, table):
    '''return most recent datetime object for buoy that has reasonable data.

    Condition of data being reasonable is based on ven table tx!=-99.
    '''

    # query for last entry
    if 'ndbc' in table:
        lastline = 'SELECT * FROM ndbc_' + buoy + ' order by obs_time DESC limit 1'
    else:
        lastline = 'SELECT * FROM tabs_' + buoy + '_' + table + ' order by obs_time DESC limit 1'
    # read in query
    df = pd.read_sql_query(lastline, engine, index_col=['obs_time'])

    # check for real data, based on tx value - only for ven table
    counter = 1
    # while tx=-99 in the latest database entry, read in more lines from
    # database, 10 by 10, until finding one that has a real value.
    # Return the date time of this entry.
    if table == 'ven':
        while (df.tail(1)['tx'].values[0] == -99):
            counter += 12
            lastline = 'SELECT * FROM tabs_' + buoy + '_' + table + ' order by obs_time DESC limit ' + str(counter)
            df = pd.read_sql_query(lastline, engine, index_col=['obs_time'])

    return df.index[-1]  # date for last available data


def query_setup(engine, buoy, table, dstart, dend):
    '''Query mysql database for data, given end date dend from
    query_setup_recent().'''

    # get 5 days of data
    # want from beginning of first day but only up until data time on final day
    # buoy C doesn't have date and time listed separately which is mostly fine except for when querying for one day
    # ndbc buoys diff too
    if buoy == 'C':
        query = 'SELECT * FROM tabs_' + buoy + '_' + table + ' WHERE (obs_time BETWEEN "' + dstart + '" AND "' + dend + '") order by obs_time'
        # query = 'SELECT * FROM tabs_' + buoy + '_' + table + ' WHERE (obs_time BETWEEN "' + dstart + '" AND "' + dend.strftime("%Y-%m-%d %H:%M") + '") order by obs_time'
    elif len(buoy) > 1:
        query = 'SELECT * FROM ndbc_' + buoy + ' WHERE (date BETWEEN "' + dstart + '" AND "' + dend + '") order by obs_time'
        # query = 'SELECT * FROM ndbc_' + buoy + ' WHERE (date BETWEEN "' + dstart + '" AND "' + dend.strftime("%Y-%m-%d %H:%M") + '") order by obs_time'
    else:
        query = 'SELECT * FROM tabs_' + buoy + '_' + table + ' WHERE (date BETWEEN "' + dstart + '" AND "' + dend + '") order by obs_time'
        # query = 'SELECT * FROM tabs_' + buoy + '_' + table + ' WHERE (date BETWEEN "' + dstart + '" AND "' + dend.strftime("%Y-%m-%d %H:%M") + '") order by obs_time'

    return query


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


def dd2dm(dd):
    '''Convert from decimal degrees to degrees/decimal minutes.'''

    deg, dm = divmod(abs(dd)*60,60)
    return int(sign(dd)*deg), round(dm, 3)


def convert_units(df, units=None, tz=None):
    '''Convert units.'''

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

    if tz == 'US/Central':  # time zone
        # need to first establish a time zone (which it is already in) to change it
        df = df.tz_localize('UTC')  # timezone is UTC
        df.index = df.index.tz_convert(tz)
        df.index.rename(df.index.name.replace('UTC', df.tail(1).index.strftime("%Z")[0]), inplace=True)

    return df


def rot2d(x, y, ang):
    '''rotate vectors by geometric angle. For model.'''
    xr = x*cos(ang) - y*sin(ang)
    yr = x*sin(ang) + y*cos(ang)
    return xr, yr


def present(df):
    '''Present dataframe df nicely by printing to screen'''

    from prettypandas import PrettyPandas
    print(PrettyPandas(df).render())


def write_file(df, fname, filetype='txt', compression=False, mode='w'):
    '''Write text file of data.

    mode is 'w' to write a new file and 'a' to append to existing file.'''

    if mode == 'a':  # don't use header if appending
        header = False
    else:
        header = True

    # Remove the time zone offset from the datetimes before saving and put
    # time zone information in the header instead.
    if filetype == 'hdf':
        # if fname.split('/')[-1].split('_')[0] == '8773259':
        #     import pdb; pdb.set_trace()
        df.tz_localize(None).to_hdf(fname + '.hdf', key='df', mode=mode,
                                    format='table', complib='zlib')#, dropna=True)

    elif filetype == 'txt':
        if compression:
            df.tz_localize(None).to_csv(fname + '.gz', sep='\t', na_rep='-999', float_format='%3.2f',
                      quoting=QUOTE_NONE,  escapechar='', compression='gzip',
                      mode=mode, header=header)
        else:
            df.tz_localize(None).to_csv(fname, sep='\t', na_rep='-999', float_format='%3.2f',
                      quoting=QUOTE_NONE,  escapechar='', mode=mode, header=header)
