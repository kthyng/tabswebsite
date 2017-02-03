'''
Tests for tools.py
'''

import tools
import numpy as np
import io
from contextlib import redirect_stdout


def test_convert():
    '''Make sure function properly converts a sample of each type'''

    assert np.allclose(tools.convert(10, 'c2f'), 50)
    assert np.allclose(tools.convert(10, 'mps2kts'), 19.4384)
    assert np.allclose(tools.convert(10, 'cps2kts'), 0.194384)
    assert np.allclose(tools.convert(10, 'mb2hg'), 0.2953)
    assert np.allclose(tools.convert(10, 'm2ft'), 32.8084)


def test_degrees_to_cardinal():
    '''Test basic directions'''

    assert tools.degrees_to_cardinal(0) == 'N'
    assert tools.degrees_to_cardinal(30) == 'NNE'
    assert tools.degrees_to_cardinal(60) == 'ENE'
    assert tools.degrees_to_cardinal(90) == 'E'
    assert tools.degrees_to_cardinal(120) == 'ESE'
    assert tools.degrees_to_cardinal(150) == 'SSE'
    assert tools.degrees_to_cardinal(180) == 'S'


def test_read_string_ven():
    '''Test reading data from an existing ven file.'''

    df = tools.read('tests/tabs_V_ven')
    # test column names
    dfcolumns = 'East [cm/s]\tNorth [cm/s]\tDir [deg T]\tWaterT [deg C]\tTx\tTy\tSpeed [cm/s]\tAcross [cm/s]\tAlong [cm/s]'
    assert '\t'.join(df.columns.values) == dfcolumns
    # test values in final line
    dftail1 = np.array([[2.06, 23.59, 170., 24.02, 0., -2., 23.68, -23.16, 4.92]])
    assert np.allclose(dftail1, df.tail(1).values)


def test_read_string_ven_changeunits():
    '''Test reading data from an existing ven file and changing to English units.'''

    df = tools.read('tests/tabs_V_ven', units='E')
    # test column names
    dfcolumns = 'East [kts]\tNorth [kts]\tDir [deg T]\tWaterT [deg F]\tTx\tTy\tSpeed [kts]\tAcross [kts]\tAlong [kts]'
    assert '\t'.join(df.columns.values) == dfcolumns
    # test values in final line
    dftail1 = np.array([[0.04, 0.46, 170, 75.2, 0.0, -2.0, 0.46, -0.45, 0.1]])
    assert np.allclose(dftail1, df.tail(1).values)


def test_read_string_met():
    '''Test reading data from an existing met file.'''

    df = tools.read('tests/tabs_V_met')
    # test column names
    dfcolumns = 'East [m/s]\tNorth [m/s]\tAirT [deg C]\tAtmPr [MB]\tGust [m/s]\tComp [deg M]\tTx\tTy\tPAR \tRelH [%]\tSpeed [m/s]\tDir from [deg T]'
    assert '\t'.join(df.columns.values) == dfcolumns
    # test values in final line
    dftail1 = np.array([[-4.29, -0.45, 15.70, 1015.74, 6.34, 169.50, 0, 0, 0.00, 108.20, 4.31, 84.00]])
    assert np.allclose(dftail1, df.tail(1).values)


def test_read_string_met_changeunits():
    '''Test reading data from an existing met file and changing to English units.'''

    df = tools.read('tests/tabs_V_met', units='E')
    # test column names
    dfcolumns = 'East [kts]\tNorth [kts]\tAirT [deg F]\tAtmPr [inHg]\tGust [kts]\tComp [deg M]\tTx\tTy\tPAR \tRelH [%]\tSpeed [kts]\tDir from [deg T]'
    assert '\t'.join(df.columns.values) == dfcolumns
    # test values in final line
    dftail1 = np.array([[-8.34, -0.87, 60.3, 29.99, 12.32, 169.5, 0., 0., 0., 108.2, 8.38, 84.]])
    assert np.allclose(dftail1, df.tail(1).values)
    pass


def test_read_string_wave():
    '''Test reading data from an existing wave file.'''

    df = tools.read('tests/tabs_V_wave')
    # test column names
    dfcolumns = 'WaveHeight [m]\tMeanPeriod [s]\tPeakPeriod [s]'
    assert '\t'.join(df.columns.values) == dfcolumns
    # test values in final line
    dftail1 = np.array([[0.86, 4.26, 5.13]])
    assert np.allclose(dftail1, df.tail(1).values)


def test_read_string_wave_changeunits():
    '''Test reading data from an existing wave file and changing to English units.'''

    df = tools.read('tests/tabs_V_wave', units='E')
    # test column names
    dfcolumns = 'WaveHeight [ft]\tMeanPeriod [s]\tPeakPeriod [s]'
    assert '\t'.join(df.columns.values) == dfcolumns
    # test values in final line
    dftail1 = np.array([[2.8, 4.26, 5.13]])
    assert np.allclose(dftail1, df.tail(1).values)


def test_read_mysql_ven():
    '''Test reading 1st line of ven data buoy V from mysql database.'''

    engine = tools.engine()
    query = 'select * from tabs_V_ven limit 0,1'
    df = tools.read([query, engine])
    # test column names
    dfcolumns = 'East [cm/s]\tNorth [cm/s]\tDir [deg T]\tWaterT [deg C]\tTx\tTy\tSpeed [cm/s]\tAcross [cm/s]\tAlong [cm/s]'
    assert '\t'.join(df.columns.values) == dfcolumns
    # test values in final line
    dftail1 = np.array([[15.11, -3.58, 256., 23.54, 0., -1., 15.53, 5.39, 14.56]])
    assert np.allclose(dftail1, df.tail(1).values)


def test_read_mysql_ven_changeunits():
    '''Test reading 1st line of ven data buoy V from mysql database and change
    to English units.'''

    engine = tools.engine()
    query = 'select * from tabs_V_ven limit 0,1'
    df = tools.read([query, engine], units='E')
    # test column names
    dfcolumns = 'East [kts]\tNorth [kts]\tDir [deg T]\tWaterT [deg F]\tTx\tTy\tSpeed [kts]\tAcross [kts]\tAlong [kts]'
    assert '\t'.join(df.columns.values) == dfcolumns
    # test values in final line
    dftail1 = np.array([[0.29, -0.07, 256, 74.4, 0.0, -1.0, 0.3, 0.1, 0.28]])
    assert np.allclose(dftail1, df.tail(1).values)


def test_read_mysql_met():
    '''Test reading 1st line of met data buoy V from mysql database.'''

    engine = tools.engine()
    query = 'select * from tabs_V_met limit 0,1'
    df = tools.read([query, engine])
    # test column names
    dfcolumns = 'East [m/s]\tNorth [m/s]\tAirT [deg C]\tAtmPr [MB]\tGust [m/s]\tComp [deg M]\tTx\tTy\tPAR \tRelH [%]\tSpeed [m/s]\tDir from [deg T]'
    assert '\t'.join(df.columns.values) == dfcolumns
    # test values in final line
    dftail1 = np.array([[-1.45, 1.07, 24.4, 1020.14, 8.33, 21.3, 0., -3., 0., 91.8, 1.8, 126.]])
    assert np.allclose(dftail1, df.tail(1).values)


def test_read_mysql_met_changeunits():
    '''Test reading 1st line of met data buoy V from mysql database.'''

    engine = tools.engine()
    query = 'select * from tabs_V_met limit 0,1'
    df = tools.read([query, engine], units='E')
    # test column names
    dfcolumns = 'East [kts]\tNorth [kts]\tAirT [deg F]\tAtmPr [inHg]\tGust [kts]\tComp [deg M]\tTx\tTy\tPAR \tRelH [%]\tSpeed [kts]\tDir from [deg T]'
    assert '\t'.join(df.columns.values) == dfcolumns
    # test values in final line
    dftail1 = np.array([[-2.82, 2.08, 75.9, 30.12, 16.19, 21.3, 0., -3., 0., 91.8, 3.5, 126.]])
    assert np.allclose(dftail1, df.tail(1).values)


def test_read_mysql_eng():
    '''Test reading 1st line of eng data buoy V from mysql database.'''

    engine = tools.engine()
    query = 'select * from tabs_V_eng limit 0,1'
    df = tools.read([query, engine])
    # test column names
    dfcolumns = 'VBatt [Oper]\tSigStr [dB]\tComp [deg M]\tNping\tTx\tTy\tADCP Volt\tADCP Curr\tVBatt [sleep]'
    assert '\t'.join(df.columns.values) == dfcolumns
    # test values in final line
    dftail1 = np.array([[13.9, -3.69, 256., 121., 0., -1., 29.94, 6.45, 13.9]])
    assert np.allclose(dftail1, df.tail(1).values)


def test_read_mysql_salt():
    '''Test reading 1st line of salt data buoy V from mysql database.'''

    engine = tools.engine()
    query = 'select * from tabs_V_salt limit 0,1'
    df = tools.read([query, engine])
    # test column names
    dfcolumns = 'Temp [deg C]\tCond [ms/cm]\tSalinity\tDensity [kg/m^3]\tSoundVel [m/s]'
    assert '\t'.join(df.columns.values) == dfcolumns
    # test values in final line
    dftail1 = np.array([[32.52, -0.01, 0.01, 99.9999, 99.9999]])
    assert np.allclose(dftail1, df.tail(1).values)


def test_read_mysql_wave():
    '''Test reading 1st line of met data buoy V from mysql database.'''

    engine = tools.engine()
    query = 'select * from tabs_V_wave limit 0,1'
    df = tools.read([query, engine])
    # test column names
    dfcolumns = 'WaveHeight [m]\tMeanPeriod [s]\tPeakPeriod [s]'
    assert '\t'.join(df.columns.values) == dfcolumns
    # test values in final line
    dftail1 = np.array([[1.1574, 5.0539, 6.6667]])
    assert np.allclose(dftail1, df.tail(1).values)


def test_read_mysql_wave_changeunits():
    '''Test reading 1st line of wave data buoy V from mysql database.'''

    engine = tools.engine()
    query = 'select * from tabs_V_wave limit 0,1'
    df = tools.read([query, engine], units='E')
    # test column names
    dfcolumns = 'WaveHeight [ft]\tMeanPeriod [s]\tPeakPeriod [s]'
    assert '\t'.join(df.columns.values) == dfcolumns
    # test values in final line
    dftail1 = np.array([[3.8,  5.0539,  6.6667]])
    assert np.allclose(dftail1, df.tail(1).values)


def test_present():
    '''Test functionality of present.

    http://stackoverflow.com/questions/16571150/how-to-capture-stdout-output-from-a-python-function-call
    '''

    df = tools.read('tests/tabs_V_ven')
    f = io.StringIO()
    with redirect_stdout(f):
        tools.present(df)
    out = f.getvalue()

    assert out  # make sure not empty
    assert isinstance(out, str)


def test_engine():
    '''Test functionality'''

    engine = tools.engine()
    assert engine  # make sure not empty
