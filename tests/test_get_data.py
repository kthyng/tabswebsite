'''
Test get_data.py
'''

import subprocess


def test_get_data_from_file_to_data():
    '''Test reading in from existing file then printing to table.'''

    fname = 'tests/tabs_V_ven'
    datatype = 'data'
    command = 'python get_data.py %s %s' % (fname, datatype)
    out = subprocess.check_output(command, shell=True)

    assert out  # make sure not empty
    assert isinstance(out, bytes)


def test_get_data_from_file_to_data_units():
    pass


def test_get_data_from_file_to_pic():
    pass


def test_get_data_from_file_to_pic_units():
    pass


def test_get_data_from_mysql_to_data():
    pass


def test_get_data_from_mysql_to_data_units():
    pass


def test_get_data_from_mysql_to_pic():
    pass


def test_get_data_from_mysql_to_pic_units():
    pass
