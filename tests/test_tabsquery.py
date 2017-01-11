'''
Test tabsquery.php
'''

import requests
from bs4 import BeautifulSoup
import buoy_data as bd
from os import path
import re


base = 'http://localhost/tabswebsite/tabsquery.php?'

def test_recent_image():
    '''Test for all parts of call (ven) to "recent" showing up on tabsquery page.

    This is just the image showing, but with the link to the data too.'''

    table = 'ven'
    for buoy in bd.buoys():

        query = "Buoyname=" + buoy + "&table=" + table + "&Datatype=pic&datepicker=recent"

        # read in website
        out = requests.get(base + query)
        # parse website
        soup = BeautifulSoup(out.text, 'lxml')
        # test for header
        assert soup.findAll('table', id="header")
        # test for download file
        assert path.exists('daily/tabs_' + buoy + '_' + table)
        # test for download link
        assert soup.findAll('a', string='download')
        # test for image
        assert soup.findAll('a', href='daily/tabs_' + buoy + '_' + table + '.pdf')


def test_recent_table():
    '''Test for all parts of "recent" to show a table.

    This is just the table showing.'''

    table = 'ven'
    for buoy in bd.buoys():

        query = "Buoyname=" + buoy + "&table=" + table + "&Datatype=data&datepicker=recent"

        # read in website
        out = requests.get(base + query)
        # parse website
        soup = BeautifulSoup(out.text, 'lxml')
        # test for header
        assert soup.findAll('table', id="header")
        # test for download file
        assert path.exists('daily/tabs_' + buoy + '_' + table)
        # test for download link
        assert soup.findAll('a', string='download')
        # test for table
        assert soup.findAll('table', id=re.compile("T_*"))


def test_active_image():
    '''Test that can query a particular date for all buoys for image.'''
    pass


def test_active_table():
    '''Test that can query a particular date for all buoys for all available tables.'''
    pass
