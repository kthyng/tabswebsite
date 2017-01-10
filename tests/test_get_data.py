'''
Test get_data.py
'''

import subprocess
from os import path, remove


def test_get_data_from_file_to_data():
    '''Test reading in from existing file then printing to table.'''

    fname = 'tests/tabs_V_ven'
    datatype = 'data'
    command = 'python get_data.py %s %s' % (fname, datatype)
    out = subprocess.check_output(command, shell=True)

    assert out  # make sure not empty
    assert isinstance(out, bytes)


def test_get_data_from_file_to_data_units():
    '''Test reading in from existing file then printing to table with
    units changed to English.'''

    fname = 'tests/tabs_V_ven'
    datatype = 'data'
    command = 'python get_data.py %s %s --units "E"' % (fname, datatype)
    out = subprocess.check_output(command, shell=True)

    assert out  # make sure not empty
    assert isinstance(out, bytes)


def test_get_data_from_file_to_pic():
    '''Test reading in from existing file then printing to image.'''

    fname = 'tests/tabs_V_ven'
    datatype = 'pic'
    command = 'python get_data.py %s %s' % (fname, datatype)
    out = subprocess.check_output(command, shell=True)

    assert path.exists(fname + '.png')
    assert path.exists(fname + '.pdf')

    # remove plots after checking for future testing
    remove(fname + '.png')
    remove(fname + '.pdf')


def test_get_data_from_file_to_pic_units():
    pass


def test_get_data_from_mysql_to_data():
    '''Test reading in from mysql then printing to table.'''

    fname = 'tests/tabs_V_ven_tmp'
    datatype = 'data'
    dstart = '2017-01-01 00:00'
    dend = '2017-01-01 02:00'
    command = 'python get_data.py %s --dstart "%s" --dend "%s" %s' % \
              (fname, dstart, dend, datatype)
    out = subprocess.check_output(command, shell=True)

    assert out  # make sure not empty
    assert isinstance(out, bytes)

    # remove file after checking
    remove(fname)


def test_get_data_from_mysql_to_data_units():
    '''Test reading in from mysql then printing to table with
    units changed to English.'''

    fname = 'tests/tabs_V_ven_tmp'
    datatype = 'data'
    dstart = '2017-01-01 00:00'
    dend = '2017-01-01 02:00'
    command = 'python get_data.py %s --dstart "%s" --dend "%s" %s --units "E"' % \
              (fname, dstart, dend, datatype)
    out = subprocess.check_output(command, shell=True)

    assert out  # make sure not empty
    assert isinstance(out, bytes)

    # remove file after checking
    remove(fname)


def test_get_data_from_mysql_to_pic():
    '''Test reading in from mysql then printing to image.'''

    fname = 'tests/tabs_V_ven_tmp'
    datatype = 'pic'
    dstart = '2017-01-01 00:00'
    dend = '2017-01-01 02:00'
    command = 'python get_data.py %s --dstart "%s" --dend "%s" %s' % \
              (fname, dstart, dend, datatype)
    out = subprocess.check_output(command, shell=True)

    assert path.exists(fname + '.png')
    assert path.exists(fname + '.pdf')

    # remove plots after checking for future testing
    remove(fname + '.png')
    remove(fname + '.pdf')


def test_get_data_from_mysql_to_pic_units():
    pass
