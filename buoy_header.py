import buoy_data
import argparse
import pandas as pd
import tools
import os

# parse the input arguments
parser = argparse.ArgumentParser()
parser.add_argument('buoy', type=str, help='which buoy')
args = parser.parse_args()
buoy = args.buoy

# read in vel file
which = 'ven'
fname = 'daily/tabs_' + buoy + '_' + which
df = tools.read(buoy, fname, which)
df = df.tz_localize('UTC')  # timezone is UTC
tail = df.tail(1)
time = tail.index.strftime("%Y-%m-%d %H:%M %Z")[0]
time2 = tail.index.tz_convert('US/Central').strftime("%Y-%m-%d %H:%M %Z")[0]
speed = tail['Speed [cm/s]'].values[0]
direct = tail['Dir [deg T]'].values[0]
temp = tail['WaterT [deg C]'].values[0]

# read in eng file
which = 'eng'
fname = 'daily/tabs_' + buoy + '_' + which
df = tools.read(buoy, fname, which)
tail = df.tail(1)
volt = tail['VBatt [Oper]'].values[0]
sigstr = tail['SigStr [dB]'].values[0]
ping = tail['Nping'].values[0]

# read in met file
which = 'met'
fname = 'daily/tabs_' + buoy + '_' + which
domet = False
if os.path.exists(fname):
    domet = True
    df = tools.read(buoy, fname, which)
    tail = df.tail(1)
    wind = tail['Speed [m/s]'].values[0]
    airtemp = tail['AirT [deg C]'].values[0]
    press = tail['AtmPr [MB]'].values[0]
    wdirect = tail['Dir from [deg T]'].values[0]
    humid = tail['RelH [%]'].values[0]

# read in wave file
which = 'wave'
fname = 'daily/tabs_' + buoy + '_' + which
dowave = False
if os.path.exists(fname):
    dowave = True
    df = tools.read(buoy, fname, which)
    tail = df.tail(1)
    # time = tail.index.strftime("%Y-%m-%d %H:%M")[0]
    wheight = tail['WaveHeight [m]'].values[0]
    wperiod = tail['MeanPeriod [s]'].values[0]

# buoy specs
loc = buoy_data.locs(buoy)['lat'][0] + '&deg; ' +\
    buoy_data.locs(buoy)['lat'][1] + '\'' +\
    buoy_data.locs(buoy)['lat'][2] + '&nbsp;&nbsp;' +\
    buoy_data.locs(buoy)['lon'][0] + '&deg; ' +\
    buoy_data.locs(buoy)['lon'][1] + '\'' +\
    buoy_data.locs(buoy)['lon'][2]
kind = buoy_data.kind(buoy)
sensor = buoy_data.sensor(buoy)
d = buoy_data.depth(buoy)

# print out titles
print('<table>')
# this is to buffer the left side
print("<TR><TD valign=top width=120 align=left rowspan=9>")
print("</td></tr>")
print('<tr>')
print('<td><b><big>Buoy %s </big></b>&nbsp;&nbsp;%s</td>' % (buoy, loc))
print('<TD colspan=3 style="text-align:right"><b>' + time + '</b> (' + time2 + ')</td>')
print('</TR>')
print('<tr></tr>')  # blank row

print('<tr>')
print('<td><b>Speed: %2.2f cm/s (%2.2f kts)&nbsp;&nbsp;&nbsp;</b></td>' % (speed, tools.convert(speed, 'cps2kts')))
print('<td><b>Direction: %3.0f&deg;T (%s)&nbsp;&nbsp;&nbsp;</b></td>' % (direct, tools.degrees_to_cardinal(direct)))
print('<td><b>Water temp: %2.1f&deg;C (%2.0f&deg;F)</b></td>' % (temp, tools.convert(temp, 'c2f')))
print('</tr>')

print('<tr>')
print('<td><small>System voltage: ' + str(volt) + ' V</small></td>')
print('<td><small>Signal strength: ' + str(sigstr) + ' dB</small></td>')
print('<td><small>Ping count: ' + str(ping) + '</small></td>')
print('</tr>')

if domet:
    print('<tr>')
    print('<td><small>Wind: %2.2f m/s (%2.2f kts) from %3.0f&deg;T (%s)</small></td>' % (wind, tools.convert(wind, 'mps2kts'), wdirect, tools.degrees_to_cardinal(wdirect)))
    print('<td><small>Air temp: %2.1f&deg;C (%2.0f&deg;F)</td>' % (airtemp, tools.convert(airtemp, 'c2f')))
    print('<td><small>Pressure: %4.1fmb (%2.2f inHg)</td>' % (press, tools.convert(press, 'mb2hg')))
    print('</tr>')

print('<tr>')
if domet:
    print('<td><small>Relative humidity: %2.0f&#37;</small></td>' % (humid))
if dowave:
    print('<td><small>Waves: %2.1fm (%2.1f ft) @ %2.1f sec</small></td>' % (wheight, tools.convert(wheight, 'm2ft'), wperiod))
print('</tr>')

print('<tr></tr>')  # blank row

print('<tr>')
print('<td><small>%s - sensor depth: %1im</small></td>' % (kind, sensor))
a = buoy_data.anemometer(buoy)  # 0 if doesn't exist
if a:
    print('<td><small>Anemometer height %1im</small></td>' % (a))
else:
    print('<td><small>No anemometer</small></td>')

print('<td><small>Water depth: %3.0f (%3.0f ft)</small></td>' % (d, tools.convert(d, 'm2ft')))
print('</tr>')

print('</table>')