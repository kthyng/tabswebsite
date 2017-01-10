'''
Tests for run_daily.py
'''


import run_daily
import tools


def test_query_setup_recent():
    '''Test query setup when easy.'''

    index = run_daily.query_setup_recent(tools.engine(), 'V')
    assert index  # check for existence
    assert isinstance(index, run_daily.pd.tslib.Timestamp)


def test_query_setup():
    '''Test that correct query comes out of query_setup().'''

    dend = run_daily.pd.datetime(2017, 1, 6, 0, 0, 0)
    query = run_daily.query_setup(tools.engine(), 'V', 'ven', dend)
    assert query == 'SELECT * FROM tabs_V_ven WHERE (date BETWEEN "2017-01-01" AND "2017-01-06 00:00") order by obs_time'


def test_make_text():
    pass


def test_overall():
    pass
