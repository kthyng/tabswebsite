'''
Test tabsquery.php
'''

import requests
from bs4 import BeautifulSoup
import buoy_data as bd
from os import path
import re


base = 'http://localhost/tabswebsite/tabsquery.php?'

# test dates
dates = {'B': '2015-01-01', 'D': '2017-01-08', 'F': '2017-01-08',
         'J': '2017-01-08', 'K': '2017-01-08', 'N': '2015-01-01',
         'R': '2017-01-08', 'V': '2017-01-08', 'W': '2015-01-01',
         'X': '2014-08-26'}

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
    '''Test that can query some date for all buoys for image of ven.'''

    table = 'ven'
    for buoy in bd.buoys():

        query = "Buoyname=" + buoy + "&table=" + table + "&Datatype=pic&datepicker=" + dates[buoy]
        # read in website
        out = requests.get(base + query)
        # parse website
        soup = BeautifulSoup(out.text, 'lxml')
        # test for download link
        assert soup.findAll('a', string='download')
        # test for image
        assert soup.findAll('a', href=re.compile("tmp/tabs_" + buoy + "_" + table + "_.*pdf"))


def test_active_table():
    '''Test that can query a particular date for all buoys for all available tables.'''

    table = 'ven'
    for buoy in bd.buoys():

        query = "Buoyname=" + buoy + "&table=" + table + "&Datatype=data&datepicker=" + dates[buoy]
        # read in website
        out = requests.get(base + query)
        # parse website
        soup = BeautifulSoup(out.text, 'lxml')
        # test for download link
        assert soup.findAll('a', string='download')
        # test for data table
        assert soup.findAll('table', id=re.compile("T_*"))
