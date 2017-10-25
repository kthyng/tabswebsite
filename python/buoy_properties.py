'''
Info about buoys to read in.
'''

def load():
    '''Read in data about buoys from csv file into dictionary.

    Health of instruments:

    1: normal, 2: degraded data, 3: data loss, 4: not functioning,
    -1: discontinued, -999: not applicable
    'C': Currents
    'E': engineering
    'M': Met
    'P': water properties
    'W': wave
    'T': telemetry

    angle: degree True for across-shelf rotation angle (rotated x axis is offshore)

    sensor depth in meters

    water depth in meters

    anemometer height above water in meters


    buoy properties can be accessed as follows:
        buoys = buoy_properties.read()
        buoys['B']
        buoys['B']['table1']
        buoys.keys()  # list of buoys

    '''

    import pandas as pd
    buoys = pd.read_csv('../includes/buoys.csv', index_col=0)
    return buoys.to_dict('index')


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
