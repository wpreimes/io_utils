# -*- coding: utf-8 -*-

import pytest
from io_utils.read.geo_ts_readers.ts_reader import GeoTsReader
import pandas as pd
from io_utils.read.geo_ts_readers import GeoCCISMv4Ts, GeoGLDAS21Ts
import numpy as np
from datetime import datetime

test_loc = (15, 45)

@pytest.mark.geo_test_data
def test_sat_data():
    reader_kwargs = {'dataset': ('ESA_CCI_SM', 'v045', 'COMBINED'),
                     'exact_index': True,
                     'parameters': ['sm', 'flag', 't0', 'sm_uncertainty'],
                     'ioclass_kws': {'read_bulk': True}}

    selfmaskingadapter_kwargs = {'op' : '==', 'threshold' : 0,
                                 'column_name' : 'flag'}
    climadapter_kwargs = {'columns' : ['sm'], 'wraparound' : True,
                          'moving_avg_clim' : 30}
    resample = ('10D', pd.DataFrame.mean)
    params_rename = {'sm': 'esa_cci_sm'}

    fancyreader = GeoTsReader(GeoCCISMv4Ts, reader_kwargs, selfmaskingadapter_kwargs,
                             climadapter_kwargs, resample, params_rename)

    ts = fancyreader.read(*test_loc)

    ts = ts.dropna(how='all')
    assert np.all(ts.columns.values == ['esa_cci_sm', 'flag', 'sm_uncertainty'])
    assert np.all(ts['flag'].dropna().values == 0.)
    assert not ts.empty
    print(ts)

@pytest.mark.geo_test_data
def test_model_data():
    reader_kwargs = {'dataset': ('GLDAS21', 'core'),
                     'parameters': ['SoilMoi0_10cm_inst', 'SoilTMP0_10cm_inst'],
                     'ioclass_kws': {'read_bulk': True}}

    # keep only obs where temp >= 277.15°C
    selfmaskingadapter_kwargs = {'op' : '>=', 'threshold' : 277.15,
                                 'column_name' : 'SoilTMP0_10cm_inst'}
    climadapter_kwargs = {'columns' : ['SoilMoi0_10cm_inst'],
                          'wraparound' : True,
                          'timespan': [datetime(2000,1,1), datetime(2010,1,1)],
                          'moving_avg_clim' : 30}
    resample = ('1D', pd.DataFrame.mean)
    params_rename = {'SoilMoi0_10cm_inst': 'sm', 'SoilTMP0_10cm_inst': 'tmp'}

    fancyreader = GeoTsReader(GeoGLDAS21Ts, reader_kwargs, selfmaskingadapter_kwargs,
                              climadapter_kwargs, resample, params_rename)

    ts = fancyreader.read(*test_loc)

    ts = ts.dropna(how='all')
    assert np.all(ts.columns.values == ['sm', 'tmp'])
    assert np.all(ts['tmp'].dropna().values >= 277.15)
    assert not ts.empty
    print(ts)

if __name__ == '__main__':
    test_model_data()
    test_sat_data()
