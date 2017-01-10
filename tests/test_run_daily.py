'''
Tests for run_daily.py
'''


import run_daily
import tools
from os import path, remove
import warnings
import buoy_data as bd


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
    '''Test file writing.'''

    df = tools.read('tests/tabs_V_ven')
    fname = 'tests/write_tabs_V_ven'
    run_daily.make_text(df, fname)

    assert open(fname).readlines() == ['Dates [UTC]\tEast [cm/s]\tNorth [cm/s]\tDir [deg T]\tWaterT [deg C]\tTx\tTy\tSpeed [cm/s]\tAcross [cm/s]\tAlong [cm/s]\n',
                                        '2017-01-05 00:00:00\t-2.50\t28.27\t139.00\t24.03\t0\t-1\t28.38\t-28.36\t0.96\n',
                                        '2017-01-05 00:30:00\t0.69\t25.37\t144.00\t24.03\t0\t-1\t25.38\t-25.10\t3.78\n',
                                        '2017-01-05 01:00:00\t1.06\t24.70\t161.00\t24.02\t0\t-1\t24.72\t-24.39\t4.06\n',
                                        '2017-01-05 01:30:00\t2.06\t23.59\t170.00\t24.02\t0\t-2\t23.68\t-23.16\t4.92\n']

    # remove file after checking
    remove(fname)


def test_made_ven():
    '''Check that ven files have been produced for every buoy since that should
    always be possible.'''

    for buoy in bd.buoys():
        assert path.exists('daily/tabs_' + buoy + '_ven')
        assert path.exists('daily/tabs_' + buoy + '_ven_low.png')
        assert path.exists('daily/tabs_' + buoy + '_ven.png')
        assert path.exists('daily/tabs_' + buoy + '_ven.pdf')


def test_overall():
    '''Check that script has produced requested files.

    This checks for files that should be made based on instruments on the buoys.
    Print out if data is not available for existing
    instruments on the buoys at the same time as the ven data.'''

    for buoy in bd.buoys():
        for table in bd.tables():
            # this checks that it should be available based on instrumentation
            if buoy in bd.avail(table):
                fname = 'tabs_' + buoy + '_' + table
                if not path.exists('daily/' + fname):
                    message = Warning(fname + ' not available at same time as ven data')
                    warnings.warn(message)
