'''
Set up header and save to file.
'''

import buoy_data as bd
import pandas as pd
import tools
import os

relloc = '../'
def make(buoy):
    '''Make header'''

    if len(buoy) == 1:  # TABS
        # read in vel file
        which = 'ven'
        fname = relloc + 'daily/tabs_' + buoy + '_' + which
        df = tools.read(fname)
        df = df.tz_localize('UTC')  # timezone is UTC
        tail = df.tail(1)
        time = tail.index.strftime("%Y-%m-%d %H:%M %Z")[0]
        time2 = tail.index.tz_convert('US/Central').strftime("%Y-%m-%d %H:%M %Z")[0]
        speed = tail['Speed [cm/s]'].values[0]
        direct = tail['Dir [deg T]'].values[0]
        temp = tail['WaterT [deg C]'].values[0]

        # read in eng file
        which = 'eng'
        fname = relloc + 'daily/tabs_' + buoy + '_' + which
        df = tools.read(fname)
        tail = df.tail(1)
        volt = tail['VBatt [Oper]'].values[0]
        sigstr = tail['SigStr [dB]'].values[0]
        ping = tail['Nping'].values[0]

        # read in met file
        which = 'met'
        fname = relloc + 'daily/tabs_' + buoy + '_' + which
        domet = False
        if os.path.exists(fname):
            domet = True
            df = tools.read(fname)
            tail = df.tail(1)
            wind = tail['Speed [m/s]'].values[0]
            airtemp = tail['AirT [deg C]'].values[0]
            press = tail['AtmPr [MB]'].values[0]
            wdirect = tail['Dir from [deg T]'].values[0]
            humid = tail['RelH [%]'].values[0]

        # read in wave file
        which = 'wave'
        fname = relloc + 'daily/tabs_' + buoy + '_' + which
        dowave = False
        if os.path.exists(fname):
            dowave = True
            df = tools.read(fname)
            tail = df.tail(1)
            # time = tail.index.strftime("%Y-%m-%d %H:%M")[0]
            wheight = tail['WaveHeight [m]'].values[0]
            wperiod = tail['MeanPeriod [s]'].values[0]

        # buoy specs
        loc = bd.locs(buoy)['lat'][0] + '&deg; ' +\
            bd.locs(buoy)['lat'][1] + '\'' +\
            bd.locs(buoy)['lat'][2] + '&nbsp;&nbsp;' +\
            bd.locs(buoy)['lon'][0] + '&deg; ' +\
            bd.locs(buoy)['lon'][1] + '\'' +\
            bd.locs(buoy)['lon'][2]
        kind = bd.kind(buoy)
        sensor = bd.sensor(buoy)
        d = bd.depth(buoy)
        a = bd.anemometer(buoy)  # 0 if doesn't exist
        doeng = True
        dosensor = True
        dodepth = True
        dotemp = True
        fname = relloc + 'daily/tabs_' + buoy + '_header'

    elif len(buoy) > 1:  # NBDC buoys
        fname = relloc + 'daily/ndbc_' + buoy
        df = tools.read(fname)
        df = df.tz_localize('UTC')  # timezone is UTC
        tail = df.tail(1)
        time = tail.index.strftime("%Y-%m-%d %H:%M %Z")[0]
        time2 = tail.index.tz_convert('US/Central').strftime("%Y-%m-%d %H:%M %Z")[0]
        speed = None
        direct = None
        dotemp = True
        temp = tail['WaterT [deg C]'].values[0]
        if temp == -99:
            dotemp = False
        wind = tail['Speed [m/s]'].values[0]
        airtemp = tail['AirT [deg C]'].values[0]
        press = tail['AtmPr [MB]'].values[0]
        wdirect = tail['Dir from [deg T]'].values[0]
        humid = tail['RelH [%]'].values[0]
        wheight = tail['Wave Ht [m]'].values[0]
        wperiod = tail['Wave Pd [s]'].values[0]
        loc = bd.locs(buoy)['lat'][0] + '&deg; ' +\
            bd.locs(buoy)['lat'][1] + '\'' +\
            bd.locs(buoy)['lat'][2] + '&nbsp;&nbsp;' +\
            bd.locs(buoy)['lon'][0] + '&deg; ' +\
            bd.locs(buoy)['lon'][1] + '\'' +\
            bd.locs(buoy)['lon'][2]
        # kind = bd.kind(buoy)
        try:
            d = bd.depth(buoy)
            dodepth = True
        except:
            dodepth = False
        a = bd.anemometer(buoy)  # 0 if doesn't exist
        doeng = False
        domet = True
        dowave = True
        dosensor = False
        fname = relloc + 'daily/ndbc_' + buoy + '_header'


    # html
    head = []
    head.append('<table id=header width=750px>')  # id is for test_tabsquery.py
    # this is to buffer the left side
    head.append('<tr>')
    head.append('<td><b><big>Buoy %s </big></b>&nbsp;&nbsp;%s</td>' % (buoy, loc))
    head.append('<TD colspan=3 style="text-align:right"><b>' + time + '</b> (' + time2 + ')</td>')
    head.append('</TR>')
    head.append('<tr></tr>')  # blank row

    head.append('<tr>')
    if speed is not None:
        head.append('<td><b>Water speed: %2.2f cm/s (%2.2f kts)&nbsp;&nbsp;&nbsp;</b></td>' % (speed, tools.convert(speed, 'cps2kts')))
    if direct is not None:
        head.append('<td><b>Direction: %3.0f&deg;T (%s)&nbsp;&nbsp;&nbsp;</b></td>' % (direct, tools.degrees_to_cardinal(direct)))
    if dotemp:
        head.append('<td><b>Temp: %2.1f&deg;C (%2.0f&deg;F)</b></td>' % (temp, tools.convert(temp, 'c2f')))
    head.append('</tr>')

    if doeng:
        head.append('<tr>')
        head.append('<td><small>System voltage: ' + str(volt) + ' V</small></td>')
        head.append('<td><small>Signal strength: ' + str(sigstr) + ' dB</small></td>')
        head.append('<td><small>Ping count: ' + str(ping) + '</small></td>')
        head.append('</tr>')

    if domet:
        head.append('<tr>')
        head.append('<td><small>Wind: %2.2f m/s (%2.2f kts) from %3.0f&deg;T (%s)</small></td>' % (wind, tools.convert(wind, 'mps2kts'), wdirect, tools.degrees_to_cardinal(wdirect)))
        head.append('<td><small>Air temp: %2.1f&deg;C (%2.0f&deg;F)</td>' % (airtemp, tools.convert(airtemp, 'c2f')))
        head.append('<td><small>Pressure: %4.1fmb (%2.2f inHg)</td>' % (press, tools.convert(press, 'mb2hg')))
        head.append('</tr>')

    head.append('<tr>')
    if domet:
        head.append('<td><small>Relative humidity: %2.0f&#37;</small></td>' % (humid))
    if dowave:
        head.append('<td><small>Waves: %2.1fm (%2.1f ft) @ %2.1f sec</small></td>' % (wheight, tools.convert(wheight, 'm2ft'), wperiod))
    head.append('</tr>')

    head.append('<tr></tr>')  # blank row

    head.append('<tr>')
    if dosensor:
        head.append('<td><small>%s - sensor depth: %1im</small></td>' % (kind, sensor))
    if a:
        head.append('<td><small>Anemometer height %1im</small></td>' % (a))
    else:
        head.append('<td><small>No anemometer</small></td>')

    if dodepth:
        head.append('<td><small>Water depth: %3.0fm (%3.0f ft)</small></td>' % (d, tools.convert(d, 'm2ft')))
    head.append('</tr>')

    head.append('</table>')

    f = open(fname, 'w')
    for headline in head:
        f.write('%s' % (headline))
    f.close()
