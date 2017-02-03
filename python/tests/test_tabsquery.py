'''
Test tabsquery.php
'''

import requests
from bs4 import BeautifulSoup
import buoy_data as bd
from os import path
import re


base = 'http://localhost/tabswebsite/subpages/tabsquery.php?'

# test dates
dates = {'B': '2015-01-01', 'D': '2017-01-08', 'F': '2017-01-08',
         'J': '2017-01-08', 'K': '2017-01-08', 'N': '2015-01-01',
         'R': '2017-01-08', 'V': '2017-01-08', 'W': '2015-01-01',
         'X': '2014-08-26', '42019': '2017-02-02', '42020': '2017-02-02',
        '42035': '2017-02-02', 'SRST2': '2017-02-02', 'PTAT2': '2017-02-02'}

def test_recent_image():
    '''Test for all parts of call (ven) to "recent" showing up on tabsquery page.

    This is just the image showing, but with the link to the data too.'''

    for buoy in bd.buoys():

        if len(buoy) == 1:
            table = 'ven'
            fname = '../daily/tabs_' + buoy + '_' + table
        elif len(buoy) > 1:
            table = 'ndbc'
            fname = '../daily/ndbc_' + buoy

        query = "Buoyname=" + buoy + "&table=" + table + "&Datatype=pic&datepicker=recent"

        # read in website
        out = requests.get(base + query)
        # parse website
        soup = BeautifulSoup(out.text, 'lxml')
        # test for header
        assert soup.findAll('table', id="header")
        # test for download file
        assert path.exists(fname)
        # test for download link
        assert soup.findAll('a', string='download')
        # test for image
        assert soup.findAll('a', href=fname + '.pdf')


def test_recent_table():
    '''Test for all parts of "recent" to show a table.

    This is just the table showing.'''

    for buoy in bd.buoys():

        if len(buoy) == 1:
            table = 'ven'
            fname = '../daily/tabs_' + buoy + '_' + table
        elif len(buoy) > 1:
            table = 'ndbc'
            fname = '../daily/ndbc_' + buoy

        query = "Buoyname=" + buoy + "&table=" + table + "&Datatype=data&datepicker=recent"

        # read in website
        out = requests.get(base + query)
        # parse website
        soup = BeautifulSoup(out.text, 'lxml')
        # test for header
        assert soup.findAll('table', id="header")
        # test for download file
        assert path.exists(fname)
        # test for download link
        assert soup.findAll('a', string='download')
        # test for table
        assert soup.findAll('table', id=re.compile("T_*"))


def test_active_image():
    '''Test that can query some date for all buoys for image of ven.'''

    for buoy in bd.buoys():

        if len(buoy) == 1:
            table = 'ven'
            fname = '../tmp/tabs_' + buoy + '_' + table
        elif len(buoy) > 1:
            table = 'ndbc'
            fname = '../tmp/ndbc_' + buoy

        query = "Buoyname=" + buoy + "&table=" + table + "&Datatype=pic&datepicker=" + dates[buoy]
        # read in website
        out = requests.get(base + query)
        # parse website
        soup = BeautifulSoup(out.text, 'lxml')
        # test for download link
        assert soup.findAll('a', string='download')
        # test for image
        assert soup.findAll('a', href=re.compile(fname + "_.*pdf"))


def test_active_table():
    '''Test that can query a particular date for all buoys for all available tables.'''

    for buoy in bd.buoys():

        if len(buoy) == 1:
            table = 'ven'
        elif len(buoy) > 1:
            table = 'ndbc'

        query = "Buoyname=" + buoy + "&table=" + table + "&Datatype=data&datepicker=" + dates[buoy]
        # read in website
        out = requests.get(base + query)
        # parse website
        soup = BeautifulSoup(out.text, 'lxml')
        # test for download link
        assert soup.findAll('a', string='download')
        # test for data table
        assert soup.findAll('table', id=re.compile("T_*"))
