import buoy_data
import argparse
import pandas as pd
import plot_buoy

# parse the input arguments
parser = argparse.ArgumentParser()
parser.add_argument('buoy', type=str, help='which buoy')
args = parser.parse_args()
buoy = args.buoy

# MAKE CURRENTS AND TEMP LARGE AND EVERYTHING ELSE SMALL
# read in vel file
which = 'ven'
fname = 'daily/tabs_' + buoy + '_' + which
df = plot_buoy.read(buoy, fname, which)
tail = df.tail(1)
time = tail.index.strftime("%Y-%m-%d %H:%M")[0]
speed = tail['Speed  [cm/s]'].values[0]
direct = tail['Dir  [deg  T]'].values[0]
temp = tail['WaterT  [deg  C]'].values[0]

# DO I NEED TO MAKE SURE THE PROPERTIES ARE AT THE SAME TIME?

# read in eng file
which = 'eng'
fname = 'daily/tabs_' + buoy + '_' + which
df = plot_buoy.read(buoy, fname, which)
tail = df.tail(1)
# time = tail.index.strftime("%Y-%m-%d %H:%M")[0]
volt = tail['VBatt  [Oper]'].values[0]
sigstr = tail['SigStr  [dB]'].values[0]
ping = tail['Nping'].values[0]

# read in met file
which = 'met'
fname = 'daily/tabs_' + buoy + '_' + which
df = plot_buoy.read(buoy, fname, which)
tail = df.tail(1)
# time = tail.index.strftime("%Y-%m-%d %H:%M")[0]
wind = tail['Speed  [m/s]'].values[0]
temp = tail['AirT  [deg  C]'].values[0]
press = tail['AtmPr  [MB]'].values[0]
wdirect = tail['Dir  from  [deg  T]'].values[0]
humid = tail['RelH  [%]'].values[0]

# read in wave file
which = 'wave'
fname = 'daily/tabs_' + buoy + '_' + which
df = plot_buoy.read(buoy, fname, which)
tail = df.tail(1)
# time = tail.index.strftime("%Y-%m-%d %H:%M")[0]
wheight = tail['WaveHeight  [m]'].values[0]
wperiod = tail['MeanPeriod  [s]'].values[0]

# print out titles
print('<br><br><br><table>')
print("<TR><TD valign=top width=120 align=left rowspan=6>")
print("</td></tr>")
print('<tr>')
print('<td><h2>Buoy ' + buoy + '</h2></td>')
print('<TD colspan=3 valign=top>')
print('<h2>Conditions at ' + time + 'CONV</h2>')
# print('<b>Conditions at 01/04/2017 11:19 UTC (01/04/2017 05:19 CST)')
print('</TD></TR>')

# print out rows of buoy specs in 1st column
print('<tr>')
loc = buoy_data.locs(buoy)['lat'][0] + '&deg; ' +\
    buoy_data.locs(buoy)['lat'][1] + '\'' +\
    buoy_data.locs(buoy)['lat'][2] + ' ' +\
    buoy_data.locs(buoy)['lon'][0] + '&deg; ' +\
    buoy_data.locs(buoy)['lon'][1] + '\'' +\
    buoy_data.locs(buoy)['lon'][2]
sensor = buoy_data.kind(buoy) + ' - sensor depth: ' + str(buoy_data.sensor(buoy)) + 'm'
a = buoy_data.anemometer(buoy)  # 0 if doesn't exist
if a:
    an = 'Anemometer height: ' + str(a) + 'm'
else:
    an = 'No anemometer'
d = buoy_data.depth(buoy)
depth = 'Water depth: ' + str(d) + 'm (' + str(d*3.28084) + ' ft)'
print('<td rowspan=4><small>' + loc + '<br>' + sensor + '<br>' + an + '<br>' + depth + '</small></td>')

# print out rest of this row as single rows
print('<td>Speed: ' + str(speed) + ' cm/s (CONV)</td>')
print('<td>Direction: ' + str(direct) + 'deg T (CONV)</td>')
print('<td>Water temp: ' + str(temp) + ' deg C (CONV)</td>')
print('</tr>')

# next row
print('<tr>')
print('<td><small>System voltage: ' + str(volt) + ' V</small></td>')
print('<td><small>Signal strength: ' + str(sigstr) + ' dB</small></td>')
print('<td><small>Ping count: ' + str(ping) + '</small></td>')
print('</tr>')

# next row
print('<tr>')
print('<td><small>Wind: ' + str(wind) + ' m/s (CONV)</small></td>')
print('<td><small>Air temp: ' + str(temp) + ' deg C (CONV)</small></td>')
print('<td><small>Pressure: ' + str(press) + ' MB (CONV)</small></td>')
print('</tr>')

# next row
print('<tr>')
print('<td><small>    from ' + str(wdirect) + ' deg T (DIRECTION?)</small></td>')
print('<td><small>Relative humidity: ' + str(humid) + '%</small></td>')
print('<td><small>Waves: ' + str(wheight) + ' m (CONV) @ ' + str(wperiod) + ' sec</small></td>')
print('</tr>')

print('</table>')
