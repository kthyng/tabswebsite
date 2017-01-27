'''
Script to make buoy table
'''

# import argparse
import tools
import buoy_data as bd
import pandas as pd


# parse the input arguments
# parser = argparse.ArgumentParser()
# parser.add_argument('which', type=str, help='which plot function to use ("ven", "met", "eng", "salt")')
# parser.add_argument('dataname', type=str, help='datafile name, found in /tmp')
# args = parser.parse_args()
# buoy = args.dataname.split('/')[-1][0]

def hover(hover_color="#ffff99"):
    return dict(selector="tr:hover",
                props=[("background-color", "%s" % hover_color)])


def color(val):
    """
    Takes a scalar and returns a string with
    the css property for text color
    """

    if val == 1:
        color = 'limegreen'
    elif val == 2:
        color = 'yellow'
    elif val == 3:
        color = 'orange'
    elif val == 4:
        color = 'firebrick'
    elif val == -1:
        color = 'lightgray'
    # elif val == 'None':
    #     color = 'None'
    else:
        color = 'black'
    return 'color: %s' % color


def backgroundcolor(val):
    """
    Takes a scalar and returns a string with
    the css property for background color
    """

    if val == 1:
        color = 'limegreen'
    elif val == 2:
        color = 'yellow'
    elif val == 3:
        color = 'orange'
    elif val == 4:
        color = 'firebrick'
    elif val == -1:
        color = 'lightgray'
    elif val == 'None':
        color = 'None'
    else:
        color = 'None'
    return 'background-color: %s' % color


def make_df():
    '''Make dataframe of buoy data.'''


    levels = ['active', 'inactive']
    dfs = []
    for level in levels:
        df = pd.DataFrame(index=bd.buoys(level))
        df.index.name = 'Buoy'

        kinds = ['C', 'M','T','E','W','P']
        for kind in kinds:
            df[kind] = ''
        df['Latitude [N]'] = ''; df['Longitude [W]'] = ''; df['Lease block'] = ''
        df['Water depth'] = ''; df['Notes'] = ''
        for ind in df.index:
            for kind in kinds:
                if bd.health(ind)[kind] == -999:
                    df[kind][ind] = ''
                else:
                    df[kind][ind] = bd.health(ind)[kind]
            df['Latitude [N]'][ind] = bd.locs(ind)['lat'][0] + '&deg; ' + \
                                      bd.locs(ind)['lat'][1] + '\''
            df['Longitude [W]'][ind] = bd.locs(ind)['lon'][0] + '&deg; ' + \
                                      bd.locs(ind)['lon'][1] + '\''
            df['Lease block'][ind] = bd.lease(ind)
            df['Water depth'][ind] = '%.0f ft  (%.0f m)' % \
                                             (tools.convert(bd.depth(ind), 'm2ft'),
                                              bd.depth(ind))
            df['Notes'][ind] = bd.notes(ind)

        dfs.append(df)
    # http://pandas.pydata.org/pandas-docs/stable/style.html#Table-Styles
    # styles = [
    #     hover(),
    #     dict(selector="th", props=[("font-size", "100%"),
    #                                ("text-align", "center")]),
    #     dict(selector="table", props=[("cell-spacing", 5)])
    # ]
    return (pd.concat(dfs).style.applymap(color)
                          .applymap(backgroundcolor))
                        #   .set_table_styles(styles))
#
# def make_legend():
#     '''Make legend for buoy status table.'''
#
#     df = pd.DataFrame(index=range(12))
#     inds = ['C', 'M','T','E','W','P', 1, 2, 3, 4, -1, '']
#     df['kind'] = ''
#     for i, ind in enumerate(inds):
#         df['kind'][i] = ind
#     df['Notes'] = ''
#     df['Notes'][0] = 'Current meter systems (current speed, direction, water temperature)'
#     df['Notes'][1] = 'Meteorological systems (wind speed,direction, air temperature, air pressure, humidity)'
#     df['Notes'][2] = 'Telemetry system (primary: satellite or cellular, backup: Argos)'
#     df['Notes'][3] = 'Engineering system'
#     df['Notes'][4] = 'Wave data system'
#     df['Notes'][5] = 'Water property system'
#     df['Notes'][6] = 'Data systems and telemetry system are functioning normally.'
#     df['Notes'][7] = 'Data systems are functioning normally with degraded data quality. Telemetry system is functioning normally but with degraded performance.'
#     df['Notes'][8] = 'Data systems are partially functional with some loss of data. Primary telemetry system is not functioning; data is returned via backup telemetry.'
#     df['Notes'][9] = 'Data systems are not functioning; no good data returned. Primary and backup telemetry systems both not functioning; no data is returned in real time.'
#     df['Notes'][10] = 'Data system used to run but is now discontinued.'
#     df['Notes'][11] = 'Data system never existed.'
#     return df.style.applymap(color).applymap(backgroundcolor)


if __name__ == "__main__":

    # print out buoy table to file
    print(make_df().render())
    # print(make_legend().render())
