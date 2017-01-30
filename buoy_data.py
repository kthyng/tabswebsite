'''
Info about buoys to read in.
'''


def buoys(kind='active'):
    '''Return list of buoys.'''

    if kind == 'active':
        return ['B','D','F','J','K','R','V','W','X']
    elif kind == 'inactive':
        return ['A','C','E','G','H','L','M','N','P','S']


def tables():
    '''Return list of tables.'''

    return ['ven', 'met', 'eng', 'salt', 'wave']


def avail(key):
    '''Return dictionary of what buoys (value) have data for each table (key).'''

    avail = {}
    avail['ven'] = ['A','B','C','D','E','F','G','H','J','K','L','M','N','P','R','S','V','W','X']
    avail['eng'] = ['A','B','C','D','E','F','G','H','J','K','L','M','N','P','R','S','V','W','X']
    avail['met'] = ['B', 'H', 'J', 'K', 'N', 'V']
    avail['salt'] = ['B', 'D', 'F', 'J', 'K', 'N', 'R', 'V', 'W', 'X']
    avail['wave'] = ['K', 'N', 'V', 'X']

    return avail[key]


def health(buoy):
    '''Health of instruments.

    1: normal, 2: degraded data, 3: data loss, 4: not functioning,
    -1: discontinued, -999: not applicable
    'C': Currents
    'E': engineering
    'M': Met
    'P': water properties
    'W': wave
    'T': telemetry
    '''

    health = {}
    health['B'] = {'C': 4, 'E': 4, 'M': 4, 'P': 4, 'W': -999, 'T': 4}
    health['D'] = {'C': 4, 'E': 4, 'M': -999, 'P': 4, 'W': -999, 'T': 4}
    health['F'] = {'C': 1, 'E': 1, 'M': -999, 'P': 1, 'W': -999, 'T': 1}
    health['J'] = {'C': 1, 'E': 1, 'M': 1, 'P': 1, 'W': -999, 'T': 1}
    health['K'] = {'C': 1, 'E': 1, 'M': 1, 'P': 1, 'W': 1, 'T': 1}
    health['R'] = {'C': 1, 'E': 1, 'M': -999, 'P': 1, 'W': -999, 'T': 1}
    health['V'] = {'C': 1, 'E': 1, 'M': 1, 'P': 1, 'W': 1, 'T': 1}
    health['W'] = {'C': 4, 'E': 4, 'M': -999, 'P': 4, 'W': -999, 'T': 4}
    health['X'] = {'C': 4, 'E': 4, 'M': 4, 'P': 4, 'W': 4, 'T': 4}

    health['A'] = {'C': -1, 'E': -1, 'M': -999, 'P': -999, 'W': -999, 'T': -1}
    health['C'] = {'C': -1, 'E': -1, 'M': -999, 'P': -999, 'W': -999, 'T': -1}
    health['E'] = {'C': -1, 'E': -1, 'M': -999, 'P': -999, 'W': -999, 'T': -1}
    health['G'] = {'C': -1, 'E': -1, 'M': -999, 'P': -999, 'W': -999, 'T': -1}
    health['H'] = {'C': -1, 'E': -1, 'M': -1, 'P': -999, 'W': -999, 'T': -1}
    health['L'] = {'C': -1, 'E': -1, 'M': -999, 'P': -999, 'W': -999, 'T': -1}
    health['M'] = {'C': -1, 'E': -1, 'M': -999, 'P': -999, 'W': -999, 'T': -1}
    health['N'] = {'C': -1, 'E': -1, 'M': -1, 'P': -1, 'W': -1, 'T': -1}
    health['P'] = {'C': -1, 'E': -1, 'M': -999, 'P': -999, 'W': -999, 'T': -1}
    health['S'] = {'C': -1, 'E': -1, 'M': -999, 'P': -999, 'W': -999, 'T': -1}

    return health[buoy]


def notes(buoy):

    notes = {}
    notes['B'] = '<a href="http://localhost/tabswebsite/tabsquery.php?Buoyname=B&table=ven&Datatype=pic&datepicker=recent&tz=UTC&units=M">In Service.</a> Redeployed 2016/8/3. Batteries failed 2016/12/18.'
    notes['D'] = '<a href="http://localhost/tabswebsite/tabsquery.php?Buoyname=D&table=ven&Datatype=pic&datepicker=recent&tz=UTC&units=M">In Service.</a> Redeployed 2017/01/05. Some telemetry problems.'
    notes['F'] = '<a href="http://localhost/tabswebsite/tabsquery.php?Buoyname=F&table=ven&Datatype=pic&datepicker=recent&tz=UTC&units=M">In Service.</a> Redeployed 2016/1/30.'
    notes['J'] = '<a href="http://localhost/tabswebsite/tabsquery.php?Buoyname=J&table=ven&Datatype=pic&datepicker=recent&tz=UTC&units=M">In Service.</a> Redeployed 2017/1/5.'
    notes['K'] = '<a href="http://localhost/tabswebsite/tabsquery.php?Buoyname=K&table=ven&Datatype=pic&datepicker=recent&tz=UTC&units=M">In Service.</a> Redeployed 2016/8/4.'
    notes['R'] = '<a href="http://localhost/tabswebsite/tabsquery.php?Buoyname=R&table=ven&Datatype=pic&datepicker=recent&tz=UTC&units=M">In Service.</a> Redeployed 2014/8/24.'
    notes['V'] = '<a href="http://localhost/tabswebsite/tabsquery.php?Buoyname=V&table=ven&Datatype=pic&datepicker=recent&tz=UTC&units=M">In Service.</a> Redeployed 2016/8/4.'
    notes['W'] = '<a href="http://localhost/tabswebsite/tabsquery.php?Buoyname=W&table=ven&Datatype=pic&datepicker=recent&tz=UTC&units=M">In Service.</a> Redeployed 2016/8/5. Stopped reporting 2016/9/23.'
    notes['X'] = '<a href="http://localhost/tabswebsite/tabsquery.php?Buoyname=X&table=ven&Datatype=pic&datepicker=recent&tz=UTC&units=M">In Service.</a> Redeployed 2016/8/4.'

    notes['A'] = '<a href="http://localhost/tabswebsite/tabsqueryform.php?Buoyname=A&datepicker=1995-08-12 - 1995-10-08&tz=UTC&units=M">Database.</a> Retired 1997/3/25. Data available 1995/8/12 - 1995/10/8.'
    notes['C'] = '<a href="http://localhost/tabswebsite/tabsqueryform.php?Buoyname=C&datepicker=1995-04-02 - 1996-11-29&tz=UTC&units=M">Database.</a> Retired 1997/3/17. Data available 1995/4/2 - 1996/11/29.'
    notes['E'] = '<a href="http://localhost/tabswebsite/tabsqueryform.php?Buoyname=E&datepicker=1995-06-01 - 1996-1-16&tz=UTC&units=M">Database.</a> Retired 1996/6/5 (no cell service). Data available 1995/6/1-1995/7/20 and 1995/11/2-1996/1/16.'
    notes['G'] = '<a href="http://localhost/tabswebsite/tabsqueryform.php?Buoyname=G&datepicker=1997-03-11 - 1998-6-8&tz=UTC&units=M">Database.</a> Retired 1998/6/15. Data available 1997/3/11 - 1998/6/8.'
    notes['H'] = ''
    notes['L'] = 'Retired 1998/10/28. Data available 1997/4/20 - 1998/10/28.'
    notes['M'] = 'Retired 1999/12/1. Data available 1999/3/2 - 1999/12/1.'
    notes['N'] = 'Out of Service. Buoy recovered 01/04/2017.'
    notes['P'] = 'Retired 2000/2/19. Data available 1998/7/22 - 2000/2/19.'
    notes['S'] = 'Retired 2001/7/26. Data available 1999/2/19 - 2001/7/23.'

    return notes[buoy]


def angle(buoy):
    '''degree True for across-shelf rotation angle (rotated x axis is offshore)'''
    angle = {'B': 145, 'K': 90, 'D': 140, 'F': 155, 'J': 90, 'N': 155, 'R': 145,
             'V': 173, 'W': 173, 'X': 90, 'A': 140, 'E': 140, 'G': 173, 'H': 140,
             'P': 200, 'S': 173, 'M': 155, 'L': 155, 'C': 145}
    return angle[buoy]


def locs(buoy):
    '''locations for buoys'''
    locs = {'B': {'lon': ['94', '53.943', 'W'], 'lat': ['28', '58.938', 'N']}, 'K': {'lon': ['96', '29.988', 'W'], 'lat': ['26', '13.008', 'N']},
            'D': {'lon': ['96', '50.574', 'W'], 'lat': ['27', '56.376', 'N']}, 'F': {'lon': ['94', '14.496', 'W'], 'lat': ['28', '50.550', 'N']},
            'J': {'lon': ['97', '03.042', 'W'], 'lat': ['26', '11.484', 'N']}, 'N': {'lon': ['94', '02.202', 'W'], 'lat': ['27', '53.418', 'N']},
            'R': {'lon': ['93', '38.502', 'W'], 'lat': ['29', '38.100', 'N']}, 'V': {'lon': ['93', '35.838', 'W'], 'lat': ['27', '53.796', 'N']},
            'W': {'lon': ['96', '00.348', 'W'], 'lat': ['28', '21.042', 'N']}, 'X': {'lon': ['96', '20.298', 'W'], 'lat': ['27', '03.960', 'N']},
            'A': {'lon': ['93', '48.700', 'W'], 'lat': ['29', '31.950', 'N']}, 'E': {'lon': ['97', '06.000', 'W'], 'lat': ['27', '20.300', 'N']},
            'G': {'lon': ['93', '28.000', 'W'], 'lat': ['29', '33.000', 'N']}, 'H': {'lon': ['96', '32.601', 'W'], 'lat': ['27', '52.045', 'N']},
            'P': {'lon': ['92', '44.190', 'W'], 'lat': ['29', '09.972', 'N']}, 'C': {'lon': ['94', '45.126', 'W'], 'lat': ['28', '48.549', 'N']},
            'S': {'lon': ['92', '48.669', 'W'], 'lat': ['28', '26.185', 'N']}, 'M': {'lon': ['94', '11.484', 'W'], 'lat': ['28', '11.526', 'N']},
            'L': {'lon': ['94', '07.000', 'W'], 'lat': ['28', '02.500', 'N']}}
    return locs[buoy]


def kind(buoy):
    '''kind of buoy'''
    kind = {'B': 'AA3900 DCS', 'F': 'AA3900 DCS', 'D': 'AA3900 DCS',
            'K': 'AA3900 DCS', 'J': 'AA3900 DCS', 'N': 'AA3900 DCS',
            'R': 'AA3900 DCS', 'V': 'AA3900 DCS', 'W': 'AA3900 DCS',
            'X': 'AA3900 DCS'}
    return kind[buoy]


def lease(buoy):
    '''lease block of buoy'''
    lease = {'B': 'GA-252', 'F': 'HI-A69', 'D': 'MA-691',
            'K': 'PI-745', 'J': 'PS-1126', 'N': 'HI-A595',
            'R': 'WC-055', 'V': 'HI-A389', 'W': 'BR-492',
            'X': '', 'A': 'SP-018', 'C': 'GA-320', 'E': 'MU-858', 'S': 'BR-492',
            'G': 'WC-095', 'L': 'HI-A543', 'M': 'HI-A515', 'P': 'VR-102','H':''}
    return lease[buoy]


def sensor(buoy):
    '''sensor depth in meters'''
    sensor = {'B': 2, 'F': 2, 'D': 2, 'K': 2, 'J': 2, 'N': 2, 'R': 2, 'V': 2,
              'W': 2, 'X': 2}
    return sensor[buoy]


def depth(buoy):
    '''water depth in meters'''
    depth = {'B': 19, 'F': 24, 'D': 18, 'K': 62, 'J': 20, 'N': 105, 'R': 9,
             'V': 89, 'W': 21, 'X': 289, 'A': 12, 'C': 22, 'E': 27.4,
             'G': 12.5, 'L': 82.3, 'M': 56.7, 'P': 20.1, 'S': 22, 'H': 0}
    return depth[buoy]


def anemometer(buoy):
    '''anemometer height above water in meters'''
    an = {'B': 4, 'K': 4, 'J': 4, 'N': 4, 'V': 4, 'X': 4, 'F': 0, 'D': 0,
          'R': 0, 'W': 0}
    return an[buoy]


def model(buoy, grid):
    '''Give model indices closest to buoy on relevant numerical grid.

    Both buoy and grid must be strings.
    grid: 'u', 'v',or 'rho'
    j/lat, i/lon.
    '''

    rho = {'B': [140, 263], 'D': [159, 176], 'F': [110, 287], 'J': [100, 114],
           'K': [108, 113], 'N': [34, 279], 'R': [164, 323], 'V': [28, 305],
           'W': [140, 209], 'X': [85, 157]}
    u = {'B': [140, 262], 'D': [159, 175], 'F': [110, 287], 'J': [100, 114],
           'K': [108, 113], 'N': [34, 279], 'R': [164, 323], 'V': [28, 305],
           'W': [140, 208], 'X': [85, 157]}
    v = {'B': [140, 263], 'D': [159, 176], 'F': [109, 287], 'J': [100, 114],
           'K': [108, 113], 'N': [34, 279], 'R': [163, 323], 'V': [28, 305],
           'W': [140, 209], 'X': [84, 157]}
    model = {'rho': rho, 'u': u, 'v': v}

    return model[grid][buoy]
