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
tables = ['ven', 'wave', 'met', 'salt', 'eng']
tablenames = ['Velocities', 'Wave', 'Meteorological', 'Water Properties', 'Engineering']

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

    for table, tablename in zip(tables, tablenames):  # loop through tables for each buoy

        # try for tabs
        fname = relloc + 'daily/tabs_' + buoy + '_' + table
        fnameh = relloc + 'daily/tabs_' + buoy + '_header'
        if not os.path.exists(fname):
            fname = relloc + 'daily/' + buoy
            fnameh = fname + '_header'
            if not os.path.exists(fname):
                continue
        df = pd.read_table(fname, parse_dates=True, index_col=0)
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





    # if len(buoy) == 1:  # TABS
    #     # read in vel file
    #     which = 'ven'
    #     fname = relloc + 'daily/tabs_' + buoy + '_' + which
    #     df = tools.read(fname)
    #     df = df.tz_localize('UTC')  # timezone is UTC
    #     tail = df.tail(1)
    #     time = tail.index.strftime("%Y-%m-%d %H:%M %Z")[0]
    #     time2 = tail.index.tz_convert('US/Central').strftime("%Y-%m-%d %H:%M %Z")[0]
    #     speed = tail['Speed [cm/s]'].values[0]
    #     direct = tail['Dir [deg T]'].values[0]
    #     temp = tail['WaterT [deg C]'].values[0]
    #
    #     # read in eng file
    #     which = 'eng'
    #     fname = relloc + 'daily/tabs_' + buoy + '_' + which
    #     df = tools.read(fname)
    #     tail = df.tail(1)
    #     volt = tail['VBatt [Oper]'].values[0]
    #     sigstr = tail['SigStr [dB]'].values[0]
    #     ping = tail['Nping'].values[0]
    #
    #     # read in met file
    #     which = 'met'
    #     fname = relloc + 'daily/tabs_' + buoy + '_' + which
    #     domet = False
    #     dohum = False
    #     if os.path.exists(fname):
    #         domet = True
    #         dohum = True
    #         df = tools.read(fname)
    #         tail = df.tail(1)
    #         wind = tail['Speed [m/s]'].values[0]
    #         airtemp = tail['AirT [deg C]'].values[0]
    #         press = tail['AtmPr [MB]'].values[0]
    #         wdirect = tail['Dir from [deg T]'].values[0]
    #         humid = tail['RelH [%]'].values[0]
    #
    #     # read in wave file
    #     which = 'wave'
    #     fname = relloc + 'daily/tabs_' + buoy + '_' + which
    #     dowave = False
    #     if os.path.exists(fname):
    #         dowave = True
    #         df = tools.read(fname)
    #         tail = df.tail(1)
    #         # time = tail.index.strftime("%Y-%m-%d %H:%M")[0]
    #         wheight = tail['WaveHeight [m]'].values[0]
    #         wperiod = tail['MeanPeriod [s]'].values[0]
    #
    #     # buoy specs
    #     lat = tools.dd2dm(bys[buoy]['lat'])
    #     lon = tools.dd2dm(bys[buoy]['lon'])
    #     ll = str(lat[0]) + '&deg; ' + str(lat[1]) + '\'N' + '&nbsp;&nbsp;' \
    #             + str(abs(lon[0])) + '&deg; ' + str(lon[1]) + '\'W'
    #     kind = bys[buoy]['kind']
    #     sensor = bys[buoy]['sensor']
    #     d = bys[buoy]['depth']
    #     a = bys[buoy]['anemometer']  # nan if doesn't exist
    #     doeng = True
    #     dosensor = True
    #     dodepth = True
    #     dotemp = True
    #     fname = relloc + 'daily/tabs_' + buoy + '_header'
    #
    # elif len(buoy) == 5:  # NBDC buoys
    #     fname = relloc + 'daily/ndbc_' + buoy
    #     df = tools.read(fname)
    #     df = df.tz_localize('UTC')  # timezone is UTC
    #     tail = df.tail(1)
    #     time = tail.index.strftime("%Y-%m-%d %H:%M %Z")[0]
    #     time2 = tail.index.tz_convert('US/Central').strftime("%Y-%m-%d %H:%M %Z")[0]
    #     speed = None
    #     direct = None
    #     dotemp = True
    #     temp = tail['WaterT [deg C]'].values[0]
    #     if temp == -99:
    #         dotemp = False
    #     wind = tail['Speed [m/s]'].values[0]
    #     airtemp = tail['AirT [deg C]'].values[0]
    #     press = tail['AtmPr [MB]'].values[0]
    #     wdirect = tail['Dir from [deg T]'].values[0]
    #     humid = tail['RelH [%]'].values[0]
    #     wheight = tail['Wave Ht [m]'].values[0]
    #     wperiod = tail['Wave Pd [s]'].values[0]
    #     lat = tools.dd2dm(bys[buoy]['lat'])
    #     lon = tools.dd2dm(bys[buoy]['lon'])
    #     ll = str(lat[0]) + '&deg; ' + str(lat[1]) + '\'N' + '&nbsp;&nbsp;' \
    #             + str(abs(lon[0])) + '&deg; ' + str(lon[1]) + '\'W'
    #     # kind = bd.kind(buoy)
    #     try:
    #         d = bys[buoy]['depth']
    #         dodepth = True
    #     except:
    #         dodepth = False
    #     a = bys[buoy]['anemometer']  # 0 if doesn't exist
    #     doeng = False
    #     domet = True
    #     dohum = True
    #     dowave = True
    #     dosensor = False
    #     fname = relloc + 'daily/ndbc_' + buoy + '_header'
    #
    # elif len(buoy) == 7:  # TCOON buoys
    #     fname = relloc + 'daily/tcoon_' + buoy
    #     df = tools.read(fname)
    #     df = df.tz_localize('UTC')  # timezone is UTC
    #     tail = df.tail(1)
    #     time = tail.index.strftime("%Y-%m-%d %H:%M %Z")[0]
    #     time2 = tail.index.tz_convert('US/Central').strftime("%Y-%m-%d %H:%M %Z")[0]
    #     speed = None
    #     direct = None
    #     dotemp = False
    #     domet = False
    #     if 'WaterT [deg C]' in df.keys():
    #         temp = tail['WaterT [deg C]'].values[0]
    #         dotemp = True
    #     if 'Speed [m/s]' in df.keys():
    #         wind = tail['Speed [m/s]'].values[0]
    #     if 'AirT [deg C]' in df.keys():
    #         airtemp = tail['AirT [deg C]'].values[0]
    #     if 'AtmPr [MB]' in df.keys():
    #         press = tail['AtmPr [MB]'].values[0]
    #     if 'Dir from [deg T]' in df.keys():
    #         wdirect = tail['Dir from [deg T]'].values[0]
    #         if not isnan(wdirect):
    #             domet = True
    #     lat = tools.dd2dm(bys[buoy]['lat'])
    #     lon = tools.dd2dm(bys[buoy]['lon'])
    #     ll = str(lat[0]) + '&deg; ' + str(lat[1]) + '\'N' + '&nbsp;&nbsp;' \
    #             + str(abs(lon[0])) + '&deg; ' + str(lon[1]) + '\'W'
    #     # kind = bd.kind(buoy)
    #     try:
    #         d = bys[buoy]['depth']
    #         dodepth = True
    #     except:
    #         dodepth = False
    #     a = bys[buoy]['anemometer']  # 0 if doesn't exist
    #     doeng = False
    #     dohum = False
    #     dowave = False
    #     dosensor = False
    #     fname = relloc + 'daily/tcoon_' + buoy + '_header'

    # # html
    # head = []
    # head.append('<table id=header width=750px>')  # id is for test_tabsquery.py
    # # this is to buffer the left side
    # head.append('<tr>')
    # head.append('<td><b><big>Buoy %s </big></b>&nbsp;&nbsp;%s</td>' % (buoy, ll))
    # head.append('<TD colspan=3 style="text-align:right"><b>' + time + '</b> (' + time2 + ')</td>')
    # head.append('</TR>')
    # head.append('<tr></tr>')  # blank row
    # # import pdb; pdb.set_trace()
    # i = 1
    # for key, keye in zip(dftail.keys(), dftaile.keys()):
    #     # import pdb; pdb.set_trace()
    #     if i == 1:
    #         head.append('<tr>')
    #     name = '<b>' + key.split('[')[0] + ': ' + '</b>'
    #     if '[' in key:
    #         unit = '[' + key.split('[')[-1]
    #         unite = '[' + keye.split('[')[-1]
    #     else:
    #         unit = ''; unite = ''
    #     metric = '{:4.2f} {}'.format(dftail[key].values[0], unit)
    #     head.append('<td>' + name + metric)
    #     if unit != '':
    #         head.append(',')
    #     head.append('&nbsp;')
    #     if not unit == unite:
    #         english = '{:4.2f} {}'.format(dftaile[keye].values[0], unite)
    #         head.append(english)
    #     head.append('&nbsp;&nbsp;&nbsp;</td>')
    #     if i != 1 and i%3 == 0:
    #         head.append('</tr><tr>')
    #     i += 1
    # head.append('<tr>')
    # if speed is not None:
    #     head.append('<td><b>Water speed: %2.2f cm/s (%2.2f kts)&nbsp;&nbsp;&nbsp;</b></td>' % (speed, tools.convert(speed, 'cps2kts')))
    # if direct is not None:
    #     head.append('<td><b>Direction: %3.0f&deg;T (%s)&nbsp;&nbsp;&nbsp;</b></td>' % (direct, tools.degrees_to_cardinal(direct)))
    # if dotemp:
    #     head.append('<td><b>Temp: %2.1f&deg;C (%2.0f&deg;F)</b></td>' % (temp, tools.convert(temp, 'c2f')))
    # head.append('</tr>')
    #
    # if doeng:
    #     head.append('<tr>')
    #     head.append('<td><small>System voltage: ' + str(volt) + ' V</small></td>')
    #     head.append('<td><small>Signal strength: ' + str(sigstr) + ' dB</small></td>')
    #     head.append('<td><small>Ping count: ' + str(ping) + '</small></td>')
    #     head.append('</tr>')
    #
    # if domet:
    #     head.append('<tr>')
    #     head.append('<td><small>Wind: %2.2f m/s (%2.2f kts) from %3.0f&deg;T (%s)</small></td>' % (wind, tools.convert(wind, 'mps2kts'), wdirect, tools.degrees_to_cardinal(wdirect)))
    #     head.append('<td><small>Air temp: %2.1f&deg;C (%2.0f&deg;F)</td>' % (airtemp, tools.convert(airtemp, 'c2f')))
    #     head.append('<td><small>Pressure: %4.1fmb (%2.2f inHg)</td>' % (press, tools.convert(press, 'mb2hg')))
    #     head.append('</tr>')
    #
    # head.append('<tr>')
    # if dohum:
    #     head.append('<td><small>Relative humidity: %2.0f&#37;</small></td>' % (humid))
    # if dowave:
    #     head.append('<td><small>Waves: %2.1fm (%2.1f ft) @ %2.1f sec</small></td>' % (wheight, tools.convert(wheight, 'm2ft'), wperiod))
    # head.append('</tr>')
    #
    # head.append('<tr></tr>')  # blank row
    #
    # head.append('<tr>')
    # if dosensor:
    #     head.append('<td><small>%s - sensor depth: %1im</small></td>' % (kind, sensor))
    # if a:
    #     head.append('<td><small>Anemometer height %1im</small></td>' % (a))
    # else:
    #     head.append('<td><small>No anemometer</small></td>')
    #
    # if dodepth:
    #     head.append('<td><small>Water depth: %3.0fm (%3.0f ft)</small></td>' % (d, tools.convert(d, 'm2ft')))
    # head.append('</tr>')

    head.append('</table>')

    f = open(fnameh, 'w')
    for headline in head:
        f.write('%s' % (headline))
    f.close()
