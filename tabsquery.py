'''
MySQL query in python
'''

import argparse
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
# had to install mysqlclient
# https://stackoverflow.com/questions/4960048/python-3-and-mysql/25724855#25724855
from prettypandas import PrettyPandas

# parse the input arguments
parser = argparse.ArgumentParser()
parser.add_argument('tablename', type=str, help='mysql query')
parser.add_argument('dstart', type=str, help='mysql query')
parser.add_argument('Prevdays', type=str, help='mysql query')
parser.add_argument('Nextdays', type=str, help='mysql query')
args = parser.parse_args()

# create query
query = 'SELECT * FROM ' + args.tablename + ' WHERE (date BETWEEN "' + args.dstart + '" - interval ' + args.Prevdays + ' day AND "' + args.dstart + '" + interval ' + args.Nextdays + ' day) order by obs_time'

# print(args.query)
# import pdb; pdb.set_trace()
# $dbh=mysql_connect('tabs1.gerg.tamu.edu','tabsweb','tabs')
# engine = create_engine('postgresql://scott:tiger@localhost:5432/mydatabase')
# query = "SELECT * FROM tabs_D_ven WHERE (date BETWEEN '2016-1-1' - interval 0 day AND '2016-1-1' + interval 0 day) order by obs_time"
# query = args.query
engine = create_engine('mysql+mysqldb://tabsweb:tabs@tabs1.gerg.tamu.edu/tabsdb')
df = pd.read_sql_query(query, engine, index_col=['obs_time'])
# remove extra date/time columns
df = df.drop(['date','time'], axis=1)
df.columns = ['East [cm/s]', 'North [cm/s]', 'Dir to [&deg;T]',
              'WaterT [&deg;C]', 'Tx', 'Ty']
df.index.name = 'Dates [UTC]'
# df['Speed [cm/s]']
# ALSO ROTATED

# # df = pd.read_table('tmp/Dven0kjrpw', delim_whitespace=True, index_col=[0],
# df = pd.read_table(args.result, delim_whitespace=True, index_col=[0],
#                    header=0, names=['Date', 'Time', 'East [cm/s]', 'North [cm/s]', 'Speed [cm/s]',
#                                     'Dir to [&deg;T]', 'WaterT [&deg;C]'],
#                    parse_dates={'Dates [UTC]': ['Date', 'Time']})
# html = df.to_html()
# import pdb; pdb.set_trace()
# print(html)
print(PrettyPandas(df).render())
# return table
# print(df)
print('e')
