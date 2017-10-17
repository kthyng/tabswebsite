'''
Info about buoys to read in.
'''


def buoys(kind='active'):
    '''Return list of buoys.'''

    if kind == 'active':
        return ['B','D','F','J','K','R','V','W','X',
                '42001','42002','42019','42020','42035','42036','42039','42040',
                'SRST2','PTAT2', 'BURL1', 'GISL1', 'AMRL1', 'PSTL1',
                '8770475', '8770520', '8770733', '8770777', '8770808', '8770822',
                '8770971', '8771486', '8771972', '8772985', '8773037', '8773146',
                '8773259', '8773701', '8774230', '8774513', '8775237', '8775241',
                '8775244', '8775283', '8775296', '8775792', '8776139', '8776604',
                '8777812', '8778490', '8779280', '8779748', '8779749',
                'g06010']
    elif kind == 'inactive':
        return ['A','C','E','G','H','L','M','N','P','S','42007']


def tables():
    '''Return list of tables.'''

    return ['ven', 'met', 'eng', 'salt', 'wave', 'ndbc', 'ndbc-nowave',
            'ndbc-nowave-nowtemp', 'ndbc-nowave-nowtemp-nopress',
            'tcoon-nomet', 'tcoon', 'ports']


def avail(key):
    '''Return dictionary of what buoys (value) have data for each table (key).'''

    avail = {}
    avail['ven'] = ['A','B','C','D','E','F','G','H','J','K','L','M','N','P','R','S','V','W','X']
    avail['eng'] = ['A','B','C','D','E','F','G','H','J','K','L','M','N','P','R','S','V','W','X']
    avail['met'] = ['B', 'H', 'J', 'K', 'N', 'V', 'X']
    avail['salt'] = ['B', 'D', 'F', 'J', 'K', 'N', 'R', 'V', 'W', 'X']
    avail['wave'] = ['K', 'N', 'V', 'X']
    avail['ndbc'] = ['42001','42002','42019','42020','42035','42036','42039','42040']
    avail['ndbc-nowave'] = ['PTAT2', 'GISL1', 'AMRL1']
    avail['ndbc-nowave-nowtemp'] = ['SRST2','BURL1']
    avail['ndbc-nowave-nowtemp-nopress'] = ['PSTL1']
    avail['tcoon-nomet'] = ['8770520']
    avail['tcoon'] = ['8770475', '8770733', '8770777', '8770808', '8770822',
                    '8770971', '8771486', '8771972', '8772985', '8773037', '8773146',
                    '8773259', '8773701', '8774230', '8774513', '8775237', '8775241',
                    '8775244', '8775283', '8775296', '8775792', '8776139', '8776604',
                    '8777812', '8778490', '8779280', '8779748', '8779749']
    avail['nos'] = ['']
    avail['ports'] = ['g06010']

    return avail[key]


def inmysql(buoy):
    '''Check if NDBC buoy is stored in mysql database or not. Returns True
    if so, and False otherwise.'''

    mysql = ['42001','42002','42019','42020','42035','42036','42039','42040',
             'SRST2','PTAT2','B','D','F','J','K','R','V','W','X','A','C','E',
             'G','H','L','M','N','P','S']
    return buoy in mysql


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
    notes['B'] = '<a href="tabsquery.php?Buoyname=B&table=ven&Datatype=pic&datepicker=recent&tz=UTC&units=M">In Service.</a> <a href="daily/tabs_D_ven_all">All data.</a> <a href="daily/tabs_D_ven_all">All data compressed.</a>\nRedeployed 2016/8/3. Batteries failed 2016/12/18.'
    notes['D'] = '<a href="tabsquery.php?Buoyname=D&table=ven&Datatype=pic&datepicker=recent&tz=UTC&units=M">In Service.</a> Redeployed 2017/01/05. Some telemetry problems.'
    notes['F'] = '<a href="tabsquery.php?Buoyname=F&table=ven&Datatype=pic&datepicker=recent&tz=UTC&units=M">In Service.</a> Redeployed 2016/1/30.'
    notes['J'] = '<a href="tabsquery.php?Buoyname=J&table=ven&Datatype=pic&datepicker=recent&tz=UTC&units=M">In Service.</a> Redeployed 2017/1/5.'
    notes['K'] = '<a href="tabsquery.php?Buoyname=K&table=ven&Datatype=pic&datepicker=recent&tz=UTC&units=M">In Service.</a> Redeployed 2016/8/4.'
    notes['R'] = '<a href="tabsquery.php?Buoyname=R&table=ven&Datatype=pic&datepicker=recent&tz=UTC&units=M">In Service.</a> Redeployed 2014/8/24.'
    notes['V'] = '<a href="tabsquery.php?Buoyname=V&table=ven&Datatype=pic&datepicker=recent&tz=UTC&units=M">In Service.</a> Redeployed 2016/8/4.'
    notes['W'] = '<a href="tabsquery.php?Buoyname=W&table=ven&Datatype=pic&datepicker=recent&tz=UTC&units=M">In Service.</a> Redeployed 2016/8/5. Stopped reporting 2016/9/23.'
    notes['X'] = '<a href="tabsquery.php?Buoyname=X&table=ven&Datatype=pic&datepicker=recent&tz=UTC&units=M">In Service.</a> Redeployed 2016/8/4.'

    notes['A'] = '<a href="daily/tabs_A_ven_all">All data.</a> <a href="daily/tabs_A_ven_all">All data compressed.</a> Retired 1997/3/25. Data available 1995/8/12 - 1995/10/8.'
    notes['C'] = '<a href="tabsqueryform.php?Buoyname=C&datepicker=1995-04-02+-+1996-11-29&tz=UTC&units=M">Database.</a> Retired 1997/3/17. Data available 1995/4/2 - 1996/11/29.'
    notes['E'] = '<a href="tabsqueryform.php?Buoyname=E&datepicker=1995-06-01+-+1996-1-16&tz=UTC&units=M">Database.</a> Retired 1996/6/5 (no cell service). Data available 1995/6/1-1995/7/20 and 1995/11/2-1996/1/16.'
    notes['G'] = '<a href="tabsqueryform.php?Buoyname=G&datepicker=1997-03-11+-+1998-6-8&tz=UTC&units=M">Database.</a> Retired 1998/6/15. Data available 1997/3/11 - 1998/6/8.'
    notes['H'] = '<a href="tabsqueryform.php?Buoyname=H&datepicker=1997-06-05+-+2007-08-05&tz=UTC&units=M">Database.</a> Retired. Data available 1997/06/05 - 1998/6/22, 2005/08/27 - 2005/10/14, 2006/8/24 - 2007/8/5.'
    notes['L'] = '<a href="tabsqueryform.php?Buoyname=L&datepicker=1998-04-20+-+1998-10-28&tz=UTC&units=M">Database.</a> Retired 1998/10/28. Data available 1998/4/20 - 1998/10/28.'
    notes['M'] = '<a href="tabsqueryform.php?Buoyname=M&datepicker=1999-03-02+-+1999-12-1&tz=UTC&units=M">Database.</a> Retired 1999/12/1. Data available 1999/3/2 - 1999/12/1.'
    notes['N'] = '<a href="tabsqueryform.php?Buoyname=N&datepicker=2002-01-23+-+2016-11-10&tz=UTC&units=M">Database.</a> Retired 2017/1/4. Data available 2002/01/23 - 2016/11/10.'
    notes['P'] = '<a href="tabsqueryform.php?Buoyname=P&datepicker=1998-07-22+-+2000-02-19&tz=UTC&units=M">Database.</a> Retired 2000/2/19. Data available 1998/7/22 - 2000/2/19.'
    notes['S'] = '<a href="tabsqueryform.php?Buoyname=S&datepicker=1999-02-19+-+2001-07-23&tz=UTC&units=M">Database.</a> Retired 2001/7/26. Data available 1999/2/19 - 2001/7/23.'

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
            'L': {'lon': ['94', '07.000', 'W'], 'lat': ['28', '02.500', 'N']}, '42019': {'lon': ['95', '21.600', 'W'], 'lat': ['27', '54.7830', 'N']},
            '42020': {'lon': ['96', '42.000', 'W'], 'lat': ['26', '57.000', 'N']},
            '42035': {'lon': ['94', '24.500', 'W'], 'lat': ['29', '14.7830', 'N']},
            'SRST2': {'lon': ['94', '3.000', 'W'], 'lat': ['29', '40.200', 'N']},
            'PTAT2': {'lon': ['97', '3.000', 'W'], 'lat': ['27', '49.700', 'N']},
            'BURL1': {'lon': ['89', '25.7', 'W'], 'lat': ['28', '54.3', 'N']},
            'GISL1': {'lon': ['89', '57.45', 'W'], 'lat': ['29', '15.88', 'N']},
            'AMRL1': {'lon': ['91', '20.28', 'W'], 'lat': ['29', '26.97', 'N']},
            'PSTL1': {'lon': ['89', '24.42', 'W'], 'lat': ['28', '55.93', 'N']},
            '42001': {'lon': ['89', '40.800', 'W'], 'lat': ['25', '55.200', 'N']},
            '42002': {'lon': ['94', '25.000', 'W'], 'lat': ['25', '10.167', 'N']},
            '42007': {'lon': ['88', '46.14', 'W'], 'lat': ['30', '5.4', 'N']},
            '42036': {'lon': ['84', '30.6', 'W'], 'lat': ['28', '30.6', 'N']},
            '42039': {'lon': ['86', '3.6', 'W'], 'lat': ['28', '48.00', 'N']},
            '42040': {'lon': ['88', '12.00', 'W'], 'lat': ['29', '12.60', 'N']},
            '8770475': {'lon': ['93', '55.8', 'W'], 'lat': ['29', '52', 'N']},
            '8770520': {'lon': ['93', '53.1', 'W'], 'lat': ['29', '58.9', 'N']},
            '8770733': {'lon': ['95', '4.7', 'W'], 'lat': ['29', '45.9', 'N']},
            '8770777': {'lon': ['95', '15.9', 'W'], 'lat': ['29', '43.6', 'N']},
            '8770808': {'lon': ['94', '23.4', 'W'], 'lat': ['29', '35.7', 'N']},
            '8770822': {'lon': ['93', '50.5', 'W'], 'lat': ['29', '41.3', 'N']},
            '8770971': {'lon': ['94', '30.6', 'W'], 'lat': ['29', '30.9', 'N']},
            '8771486': {'lon': ['94', '53.8', 'W'], 'lat': ['29', '18.1', 'N']},
            '8771972': {'lon': ['95', '7.9', 'W'], 'lat': ['29', '4.8', 'N']},
            '8772985': {'lon': ['95', '37', 'W'], 'lat': ['28', '46.3', 'N']},
            '8773037': {'lon': ['96', '42.7', 'W'], 'lat': ['28', '24.4', 'N']},
            '8773146': {'lon': ['95', '54.8', 'W'], 'lat': ['28', '42.6', 'N']},
            '8773259': {'lon': ['96', '36.6', 'W'], 'lat': ['28', '38.4', 'N']},
            '8773701': {'lon': ['96', '23.8', 'W'], 'lat': ['28', '26.8', 'N']},
            '8774230': {'lon': ['96', '47.8', 'W'], 'lat': ['28', '13.7', 'N']},
            '8774513': {'lon': ['97', '1.5', 'W'], 'lat': ['28', '6.8', 'N']},
            '8775237': {'lon': ['97', '4.3', 'W'], 'lat': ['27', '50.4', 'N']},
            '8775241': {'lon': ['97', '2.3', 'W'], 'lat': ['27', '50.2', 'N']},
            '8775244': {'lon': ['97', '29.1', 'W'], 'lat': ['27', '49.9', 'N']},
            '8775283': {'lon': ['97', '12.2', 'W'], 'lat': ['27', '49.3', 'N']},
            '8775296': {'lon': ['97', '23.4', 'W'], 'lat': ['27', '48.7', 'N']},
            '8775792': {'lon': ['97', '14.2', 'W'], 'lat': ['27', '37.8', 'N']},
            '8776139': {'lon': ['97', '19.1', 'W'], 'lat': ['27', '29.1', 'N']},
            '8776604': {'lon': ['97', '24.3', 'W'], 'lat': ['27', '17.8', 'N']},
            '8777812': {'lon': ['97', '29.5', 'W'], 'lat': ['26', '49.5', 'N']},
            '8778490': {'lon': ['97', '25.5', 'W'], 'lat': ['26', '33.5', 'N']},
            '8779280': {'lon': ['97', '17.1', 'W'], 'lat': ['26', '15.7', 'N']},
            '8779748': {'lon': ['97', '10.1', 'W'], 'lat': ['26', '4.4', 'N']},
            '8779749': {'lon': ['97', '9.3', 'W'], 'lat': ['26', '4', 'N']},
            'g06010': {'lon': ['94', '44.450', 'W'], 'lat': ['29', '20.533', 'N']}}
    return locs[buoy]


def locs_dd(buoy):
    '''Give buoy location in decimal degrees. Returns lon, lat.'''

    lat = int(locs(buoy)['lat'][0]) + float(locs(buoy)['lat'][1])/60.
    lon = -(int(locs(buoy)['lon'][0]) + float(locs(buoy)['lon'][1])/60.)
    return lon, lat


def kind(buoy):
    '''kind of buoy'''
    kind = {'B': 'AA3900 DCS', 'F': 'AA3900 DCS', 'D': 'AA3900 DCS',
            'K': 'AA3900 DCS', 'J': 'AA3900 DCS', 'N': 'AA3900 DCS',
            'R': 'AA3900 DCS', 'V': 'AA3900 DCS', 'W': 'AA3900 DCS',
            'X': 'AA3900 DCS', '42019': '', '42020': '', '42035': '',
            'SRST2': '', 'PTAT2': ''}
    return kind[buoy]


def lease(buoy):
    '''lease block of buoy'''
    lease = {'B': 'GA-252', 'F': 'HI-A69', 'D': 'MA-691',
            'K': 'PI-745', 'J': 'PS-1126', 'N': 'HI-A595',
            'R': 'WC-055', 'V': 'HI-A389', 'W': 'BR-492',
            'X': '', 'A': 'SP-018', 'C': 'GA-320', 'E': 'MU-858', 'S': 'BR-492',
            'G': 'WC-095', 'L': 'HI-A543', 'M': 'HI-A515', 'P': 'VR-102','H':'',
            '42019': '', '42020': '', '42035': '', 'SRST2': '', 'PTAT2': ''}
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
             'G': 12.5, 'L': 82.3, 'M': 56.7, 'P': 20.1, 'S': 22, 'H': 0,
             '42019': 82, '42020': 77, '42035': 16}
    return depth[buoy]


def anemometer(buoy):
    '''anemometer height above water in meters'''
    an = {'B': 4, 'K': 4, 'J': 4, 'N': 4, 'V': 4, 'X': 4, 'F': 0, 'D': 0,
          'R': 0, 'W': 0, '42019': 5, '42020': 5, '42035': 5, 'SRST2': 14,'PTAT2': 15,
          '8770475': 6.9, '8770733': 7.6, '8770777': 4.1, '8770808': 8, '8770822': 14.3,
            '8770971': 6.1, '8771486': 3.7, '8771972': 0, '8772985': 8.6,
            '8773037': 7.7, '8773146': 7.8,
            '8773259': 6.1, '8773701': 6.0, '8774230': 9.6, '8774513': 3.1,
            '8775237': 8.1, '8775241': 4.0, '8770520': 0, '8778490': 0,
            '8775244': 0, '8775283': 0, '8775296': 8.2, '8775792': 6.4,
            '8776139': 4.5, '8776604': 7.0,
            '8777812': 5.3, '8779280': 7.4, '8779748': 0, '8779749': 4.2}
    return an[buoy]


def model(buoy, grid):
    '''Give model indices closest to buoy on relevant numerical grid.

    Both buoy and grid must be strings.
    grid: 'u', 'v',or 'rho'
    j/lat, i/lon.
    '''

    rho = {'B': [140, 263], 'D': [159, 176], 'F': [110, 287], 'J': [108, 113],
           'K': [67, 120], 'N': [34, 279], 'R': [164, 323], 'V': [28, 305],
           'W': [140, 209], 'X': [85, 157],
            '42019': [78, 217], '42040': [15, 644],
           '42020': [104, 146], '42035': [147, 287], 'SRST2': [171, 307],
           'PTAT2': [164, 168], 'BURL1': [40, 572], 'GISL1': [95, 554],
            'AMRL1': [153, 450], 'PSTL1': [41, 573],
            'A': [158, 315], 'C': [122, 265],
            'E': [147, 153], 'G': [156, 330], 'H': [139, 180], 'L': [46, 278],
            'M': [58, 277], 'N': [34, 279], 'P': [118, 364], 'S': [57, 356],
            '8770475': [182, 314], '8770520': [189, 317], '8770733': [189, 274],
            '8770808': [168, 293], '8770822': [170, 315], '8770971': [170, 288],
            '8771486': [164, 270], '8771972': [155, 256], '8772985': [151, 232],
            '8773037': [177, 191], '8773146': [159, 221], '8773259': [184, 200],
            '8773701': [165, 200], '8774230': [171, 185], '8774513': [176, 177],
            '8775237': [167, 168], '8775241': [164, 169], '8775244': [184, 161],
            '8775283': [172, 165], '8775296': [179, 162], '8775792': [166, 159],
            '8776139': [165, 154], '8776604': [164, 148], '8777812': [157, 132],
            '8778490': [146, 123], '8779280': [129, 114], '8779748': [116, 108],
            '8779749': [113, 108]}
    u = {'B': [140, 262], 'D': [159, 175], 'F': [110, 287], 'J': [108, 113],
           'K': [67, 119], 'N': [34, 279], 'R': [164, 323], 'V': [28, 305],
           'W': [140, 208], 'X': [85, 157],
            '42019': [78, 216], '42040': [15, 644],
           '42020': [104, 146], '42035': [147, 286], 'SRST2': [171, 306],
           'PTAT2': [164, 168], 'BURL1': [40, 571], 'GISL1': [95, 554],
            'AMRL1': [153, 450], 'PSTL1': [41, 572],
            'A': [158, 315], 'C': [122, 264],
            'E': [147, 152], 'G': [156, 330], 'H': [139, 180], 'L': [46, 278],
            'M': [58, 277], 'N': [34, 279], 'P': [118, 364], 'S': [57, 356],
            '8770475': [182, 314], '8770520': [189, 317], '8770733': [189, 274],
            '8770808': [168, 293], '8770822': [170, 315], '8770971': [170, 288],
            '8771486': [164, 270], '8771972': [155, 256], '8772985': [151, 232],
            '8773037': [177, 191], '8773146': [159, 221], '8773259': [184, 200],
            '8773701': [165, 200], '8774230': [171, 185], '8774513': [176, 177],
            '8775237': [167, 168], '8775241': [164, 169], '8775244': [184, 161],
            '8775283': [172, 165], '8775296': [179, 162], '8775792': [166, 159],
            '8776139': [165, 154], '8776604': [164, 148], '8777812': [157, 132],
            '8778490': [146, 123], '8779280': [129, 114], '8779748': [116, 108],
            '8779749': [113, 108]}
    v = {'B': [140, 263], 'D': [159, 176], 'F': [109, 287], 'J': [108, 114],
           'K': [67, 119], 'N': [34, 279], 'R': [163, 323], 'V': [28, 305],
           'W': [140, 209], 'X': [84, 157],
                    '42019': [78, 217], '42040': [15, 644],
           '42020': [104, 146], '42035': [146, 287], 'SRST2': [171, 307],
           'PTAT2': [163, 168], 'BURL1': [39, 572], 'GISL1': [95, 554],
            'AMRL1': [153, 450], 'PSTL1': [40, 573],
            'A': [158, 315], 'C': [121, 265],
            'E': [147, 153], 'G': [155, 330], 'H': [139, 180], 'L': [46, 278],
            'M': [58, 277], 'N': [34, 279], 'P': [117, 364], 'S': [57, 356],
            '8770475': [182, 314], '8770520': [189, 317], '8770733': [189, 274],
            '8770808': [168, 293], '8770822': [170, 315], '8770971': [170, 288],
            '8771486': [164, 270], '8771972': [155, 256], '8772985': [151, 232],
            '8773037': [177, 191], '8773146': [159, 221], '8773259': [184, 200],
            '8773701': [165, 200], '8774230': [171, 185], '8774513': [176, 177],
            '8775237': [167, 168], '8775241': [164, 169], '8775244': [184, 161],
            '8775283': [172, 165], '8775296': [179, 162], '8775792': [166, 159],
            '8776139': [165, 154], '8776604': [164, 148], '8777812': [157, 132],
            '8778490': [146, 123], '8779280': [129, 114], '8779748': [116, 108],
            '8779749': [113, 108]}
    model = {'rho': rho, 'u': u, 'v': v}

    if buoy in model[grid]:
        return model[grid][buoy]
    else:
        return False


def station(buoy):
    '''Give buoy station index if available. -999 otherwise.

    Certain stations are saved separately in ROMS. Buoy B, GISL1, PSTL1 will give nan's so
    is not included in the list, though a placeholder is in its space.'''

    stations = ['wasB', 'D', 'F', 'J', 'N', 'R', 'V', 'W', '42019', '42020', '42035',
                'BURL1', 'PTAT2', 'SRST2', 'wasGISL1', 'AMRL1', 'wasPSTL1']
    try:
        return stations.index(buoy)
    except:
        return -999
