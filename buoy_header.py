import buoy_data
import argparse
import pandas as pd
import plot_buoy

# parse the input arguments
parser = argparse.ArgumentParser()
parser.add_argument('buoy', type=str, help='which buoy')
args = parser.parse_args()
buoy = args.buoy

# read in vel file
which = 'ven'
fname = 'daily/tabs_' + buoy + '_' + which + '.txt'
df = plot_buoy.read(buoy, fname, which)
# df = pd.read_table('daily/tabs_' + buoy + '_ven.txt')
speed = df[-1,4]

# print out titles
print('<br><br><br><table>')
print('<tr>')
print('<td><h2>Buoy ' + buoy + '</h2></td>')
print('<TD>')# colspan=3 valign=top>')
print('<b>Conditions at 01/04/2017 11:19 UTC (01/04/2017 05:19 CST)')
print('</TD></TR>')

# # print out rows of buoy specs in 1st column
# print('<tr>')
# loc = buoy_data.locs(buoy)['lat'][0] + '&deg; ' +\
#     buoy_data.locs(buoy)['lat'][1] + '\'' +\
#     buoy_data.locs(buoy)['lat'][2] + ' ' +\
#     buoy_data.locs(buoy)['lon'][0] + '&deg; ' +\
#     buoy_data.locs(buoy)['lon'][1] + '\'' +\
#     buoy_data.locs(buoy)['lon'][2]
# sensor = buoy_data.kind(buoy) + ' - sensor depth: ' + str(buoy_data.sensor(buoy)) + 'm'
# a = buoy_data.anemometer(buoy)  # 0 if doesn't exist
# if a:
#     an = 'Anemometer height: ' +  + 'm'
# else:
#     an = 'No anemometer'
# d = buoy_data.depth(buoy)
# depth = 'Water depth: ' + str(d) + 'm (' + str(d*3.28084) + ' ft)'
# print('<td rowspan=4>' + loc + '<br>' + sensor + '<br>' + an + '<br>' + depth + '</td>')

# # print out rest of this row as single rows
# speed =
# direction
# temp
# print('<td>' + speed + '</td>')
# print('</tr>')
#
# # next row
# System Voltage: 13.8 V	Signal Strength: -1.5 dB	Ping Count: 132
#
# # next row
# Wind: 3.1 m/s (6.0 kts)
#           From 58°T (ENE)	Air Temp: 32 °C (89 °F)
# Relative Humidity:  75 %	Pressure: 1012.3 mb (29.89 inHg)
# Waves: 0.6 m (1.9 ft) @ 6 sec

print('</table>')
