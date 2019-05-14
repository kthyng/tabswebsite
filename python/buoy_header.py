'''
Set up header and save to file.
'''

import pandas as pd
import tools
import os
from numpy import isnan
import logging

relloc = '../'
bys = pd.read_csv('../includes/buoys.csv', index_col=0)
# tables = ['ven', 'wave', 'met', 'salt', 'eng']
tablenames = {'ven': 'Velocities', 'wave': 'Wave', 'met': 'Meteorological',
              'salt': 'Water Properties', 'eng': 'Engineering'}
tablekeys = ['table1', 'table2', 'table3', 'table4', 'table5']

def top(buoy, ll, time, time2):
    head = []
    # html
    head.append('<table id=header style="width:900px">')  # id is for test_tabsquery.py
    # this is to buffer the left side
    head.append('<tr>')
    # sum of colspan in following two lines matches mod number in html()
    head.append('<td colspan=2 ><b><big>Buoy %s </big></b>&nbsp;&nbsp;%s</td>' % (buoy, ll))
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
        # create line for header
        value = dftail[key].values[0]  # data value
        if value != -999.00:
            metric = '{:4.2f} {}'.format(value, unit)
            head.append('<td>' + name + metric)
            if (unit != unite):
                head.append(',&nbsp;')
            head.append('<br>&nbsp;')
            if (unit != unite):
                english = '{:4.2f} {}'.format(dftaile[keye].values[0], unite)
                head.append(english)
            head.append('&nbsp;&nbsp;&nbsp;</td>')
            # modulo number controls number of columns
            if i != 1 and i%5 == 0:
                head.append('</tr><tr>')
        i += 1
    head.append('<tr></tr><tr></tr>')
    return head


def make(buoy):
    '''Make header'''

    # initialize head
    head = None

    lon, lat = bys.loc[buoy,['lon','lat']]
    ll = '%2.3f&deg; N &nbsp;&nbsp; %2.3f&deg; W' % (lat, abs(lon))
    # pulls out the non-nan table values to loop over valid table names
    tables = [bys.loc[buoy,table] for table in tablekeys if not pd.isnull(bys.loc[buoy,table])]
    for i, table in enumerate(tables):  # loop through tables for each buoy
        # table entries with "predict" in them are not really separate tables
        if 'predict' in table:
            continue
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
        # import pdb; pdb.set_trace()
        dftail = df.tail(1)
        dftaile = tools.convert_units(dftail, units='E', tz=None)
        time = dftail.index.strftime("%Y-%m-%d %H:%M %Z")[0]
        time2 = dftail.index.tz_convert('US/Central').strftime("%Y-%m-%d %H:%M %Z")[0]
        # catch first TABS table or the one of another type of buoy
        if (tablename is not None and i == 0) or tablename is None:
            head = top(buoy, ll, time, time2)
            head = html(head, tablename, dftail, dftaile)
        elif tablename is not None and i > 0:  # a subsequent TABS table
            head = html(head, tablename, dftail, dftaile)

    # check for case of missing file when head cannot be made
    if head is not None:
        head.append('</table>')

        f = open(fnameh, 'w')
        for headline in head:
            f.write('%s' % (headline))
        f.close()
