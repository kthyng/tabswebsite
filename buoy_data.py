'''
Info about buoys to read in.
'''


def angle(buoy):
    '''degree True for across-shelf rotation angle (rotated x axis is offshore)'''
    angle = {'B': 145, 'K': 90, 'D': 140, 'F': 155, 'J': 90, 'N': 155, 'R': 145,
             'V': 173, 'W': 173, 'X': 90}
    return angle[buoy]


def locs(buoy):
    '''locations for buoys'''
    locs = {'B': {'lon': ['94', '53.943', 'W'], 'lat': ['28', '58.938', 'N']}, 'K': {'lon': ['96', '29.988', 'W'], 'lat': ['26', '13.008', 'N']},
            'D': {'lon': ['96', '50.574', 'W'], 'lat': ['27', '56.376', 'N']}, 'F': {'lon': ['94', '14.496', 'W'], 'lat': ['28', '50.550', 'N']},
            'J': {'lon': ['97', '03.042', 'W'], 'lat': ['26', '11.484', 'N']}, 'N': {'lon': ['94', '02.202', 'W'], 'lat': ['27', '53.418', 'N']},
            'R': {'lon': ['93', '38.502', 'W'], 'lat': ['29', '38.100', 'N']}, 'V': {'lon': ['93', '35.838', 'W'], 'lat': ['27', '53.796', 'N']},
            'W': {'lon': ['96', '00.348', 'W'], 'lat': ['28', '21.042', 'N']}, 'X': {'lon': ['96', '20.298', 'W'], 'lat': ['27', '03.960', 'N']}}
    return locs[buoy]


def kind(buoy):
    '''kind of buoy'''
    kind = {'B': 'AA3900 DCS', 'F': 'AA3900 DCS', 'D': 'AA3900 DCS',
            'K': 'AA3900 DCS', 'J': 'AA3900 DCS', 'N': 'AA3900 DCS',
            'R': 'AA3900 DCS', 'V': 'AA3900 DCS', 'W': 'AA3900 DCS',
            'X': 'AA3900 DCS'}
    return kind[buoy]


def sensor(buoy):
    '''sensor depth in meters'''
    sensor = {'B': 2, 'F': 2, 'D': 2, 'K': 2, 'J': 2, 'N': 2, 'R': 2, 'V': 2,
              'W': 2, 'X': 2}
    return sensor[buoy]


def depth(buoy):
    '''water depth in meters'''
    depth = {'B': 19, 'F': 24, 'D': 18, 'K': 62, 'J': 20, 'N': 105, 'R': 9,
             'V': 89, 'W': 21, 'X': 289}
    return depth[buoy]


def anemometer(buoy):
    '''anemometer height above water in meters'''
    an = {'B': 4, 'K': 4, 'J': 4, 'N': 4, 'V': 4, 'X': 4, 'F': 0, 'D': 0,
          'R': 0, 'W': 0}
    return an[buoy]