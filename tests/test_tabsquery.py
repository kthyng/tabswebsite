'''
Test tabsquery.php
'''

import requests
from bs4 import BeautifulSoup
import buoy_data as bd
from os import path


base = 'http://localhost/tabswebsite/tabsquery.php?'

def test_recent():
    '''Test for all parts of call (ven) to "recent" showing up on tabsquery page.'''

    table = 'ven'
    for buoy in bd.buoys():
        if not buoy in bd.avail(table):
            continue

        query = "Buoyname=" + buoy + "&table=" + table + "&Datatype=pic&datepicker=recent"

        # read in website
        out = requests.get(base + query)
        # parse website
        soup = BeautifulSoup(out.text, 'lxml')
        # test for header
        assert soup.findAll('table', id="header")
        # test for download link
        assert soup.findAll('a', string='download')
        # test for download file
        assert path.exists('daily/tabs_' + buoy + '_' + table)
        # test for image
        assert soup.findAll('a', href='daily/tabs_' + buoy + '_' + table + '.pdf')
