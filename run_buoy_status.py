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
        df['Water depth'] = ''
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

        dfs.append(df)
    return pd.concat(dfs).style.applymap(color).applymap(backgroundcolor)


if __name__ == "__main__":

    # print out buoy table to file
    print(make_df().render())
    # tools.present(df)
