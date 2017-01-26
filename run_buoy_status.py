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



def make_df():
    '''Make dataframe of buoy data.'''


    levels = ['active', 'inactive']
    dfs = []
    for level in levels:
        df = pd.DataFrame(index=bd.buoys(level))

        df['Latitude [N]'] = ''; df['Longitude [W]'] = ''; df['Lease block'] = ''
        df['Water depth [ft/m]'] = ''; df['System health'] = ''
        for ind in df.index:
            for table in bd.tables():
                df['System health'][ind] += bd.health(ind, table)
            df['Latitude [N]'][ind] = bd.locs(ind)['lat'][0] + '&deg; ' + \
                                      bd.locs(ind)['lat'][1] + '\''
            df['Longitude [W]'][ind] = bd.locs(ind)['lon'][0] + '&deg; ' + \
                                      bd.locs(ind)['lon'][1] + '\''
            df['Lease block'][ind] = bd.lease(ind)
            df['Water depth [ft/m]'][ind] = '%.0f / %.0f' % \
                                             (tools.convert(bd.depth(ind), 'm2ft'),
                                              bd.depth(ind))

        dfs.append(df)
        df = pd.concat(dfs)
    return df

if __name__ == "__main__":

    # print out buoy table to file
    df = make_df()
    tools.present(df)
