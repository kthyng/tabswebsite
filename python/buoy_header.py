'''
Set up header and save to file.
'''

import buoy_properties as bp
import pandas as pd
import tools
import os
from numpy import isnan

relloc = '../'
bys = bp.load() # load in buoy data
# tables = ['ven', 'wave', 'met', 'salt', 'eng']
tablenames = {'ven': 'Velocities', 'wave': 'Wave', 'met': 'Meteorological',
              'salt': 'Water Properties', 'eng': 'Engineering'}
tablekeys = ['table1', 'table2', 'table3', 'table4', 'table5']

def top(buoy, ll, time, time2):
    head = []
    # html
    head.append('<table id=header width=850px>')  # id is for test_tabsquery.py
    # this is to buffer the left side
    head.append('<tr>')
    head.append('<td><b><big>Buoy %s </big></b>&nbsp;&nbsp;%s</td>' % (buoy, ll))
    head.append('<TD colspan=3 style="text-align:left"><b>' + time + '</b> (' + time2 + ')</td>')
    head.append('</TR>')
    head.append('<tr></tr>')  # blank row

    return head

def html(head, tablename, dftail, dftaile):
    # import pdb; pdb.set_trace()
    if tablename is not None:
        head.append('<tr><td><i>' + tablename + '</i></td></tr>')
    i = 1
    for key, keye in zip(dftail.keys(), dftaile.keys()):
        # import pdb; pdb.set_trace()
        if i == 1:
            head.append('<tr>')
        name = '<b>' + key.split('[')[0] + ': ' + '</b>'
        if '[' in key:
            unit = '[' + key.split('[')[-1]
            unite = '[' + keye.split('[')[-1]
        else:
            unit = ''; unite = ''
        metric = '{:4.2f} {}'.format(dftail[key].values[0], unit)
        head.append('<td>' + name + metric)
        if unit != '':
            head.append(',')
        head.append('&nbsp;')
        if not unit == unite:
            english = '{:4.2f} {}'.format(dftaile[keye].values[0], unite)
            head.append(english)
        head.append('&nbsp;&nbsp;&nbsp;</td>')
        if i != 1 and i%3 == 0:
            head.append('</tr><tr>')
        i += 1
    head.append('<tr></tr><tr></tr>')
    return head


def make(buoy):
    '''Make header'''


    lon, lat = bys[buoy]['lon'], bys[buoy]['lat']
    ll = str(lat) + '&deg; ' + 'N' + '&nbsp;&nbsp;' \
            + str(abs(lon)) + '&deg; ' + 'W'
    # pulls out the non-nan table values to loop over valid table names
    tables = [bys[buoy][table] for table in tablekeys if not pd.isnull(bys[buoy][table])]
    for table in tables:  # loop through tables for each buoy

        # use name for TABS tables but not others
        if table in tablenames.keys():
            tablename = tablenames[table]
        else:
            tablename = None

        # try for tabs
        fname = relloc + 'daily/tabs_' + buoy + '_' + table
        fnameh = relloc + 'daily/tabs_' + buoy + '_header'
        # if files don't exist, then this isn't a tabs buoy
        if not os.path.exists(fname):
            fname = relloc + 'daily/' + buoy
            fnameh = fname + '_header'
            if not os.path.exists(fname):
                continue
        df = pd.read_table(fname, parse_dates=True, index_col=0)
        if df is None or df.empty:
            continue
        df = df.tz_localize('UTC')  # timezone is UTC
        dftail = df.tail(1)
        dftaile = tools.convert_units(dftail, units='E', tz=None)
        # import pdb; pdb.set_trace()
        time = dftail.index.strftime("%Y-%m-%d %H:%M %Z")[0]
        time2 = dftail.index.tz_convert('US/Central').strftime("%Y-%m-%d %H:%M %Z")[0]
        try:
            head = html(head, tablename, dftail, dftaile)
        except:
            head = top(buoy, ll, time, time2)
            head = html(head, tablename, dftail, dftaile)

    head.append('</table>')

    f = open(fnameh, 'w')
    for headline in head:
        f.write('%s' % (headline))
    f.close()
