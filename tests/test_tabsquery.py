'''
Test tabsquery.php
'''

import requests
from bs4 import BeautifulSoup
import buoy_data as bd


base = 'http://localhost/tabswebsite/tabsquery.php?'

def test_recent():
    '''Test for all parts of call to "recent" showing up on tabsquery page.'''

    # buoy = 'V'

    for buoy in bd.buoys():
        table = 'ven'
        # for table in bd.tables():
        if not buoy in bd.avail(table):
            continue
        query = "Buoyname=" + buoy + "&table=" + table + "&Datatype=pic&datepicker=recent"

        # read in website
        out = requests.get(base + query)
        # parse website
        soup = BeautifulSoup(out.text, 'lxml')
        # TEST FOR HEADER
        # TEST THAT DOWNLOAD LINK WORKS (FILE EXISTS)
        # is image there?
        assert soup.findAll('a', href='daily/tabs_' + buoy + '_' + table + '.pdf')
        # assert result
