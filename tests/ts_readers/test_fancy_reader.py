# -*- coding: utf-8 -*-

import pytest
from io_utils.read.geo_ts_readers.ts_reader import GeoTsReader
import pandas as pd
from io_utils.read.geo_ts_readers import GeoCCISMv4Ts, GeoGLDAS21Ts, GeoISMNTs
import numpy as np
from datetime import datetime

test_loc = (15, 45)

@pytest.mark.geo_test_data
def test_sat_data():
    """
    Read ESA CCI SM 45 data, mask based on goodl-flags soil and create
    sm anomalies based on 1991-2010 clim.
    """
    reader_kwargs = {'dataset': ('ESA_CCI_SM', 'v045', 'COMBINED'),
                     'force_path_group': 'radar',
                     'exact_index': True,
                     'parameters': ['sm', 'flag', 't0', 'sm_uncertainty'],
                     'ioclass_kws': {'read_bulk': True}}

    selfmaskingadapter_kwargs = {'op' : '==', 'threshold' : 0,
                                 'column_name' : 'flag'}
    climadapter_kwargs = {'columns' : ['sm'],
                          'timespan': [datetime(1991, 1, 1), datetime(2010, 12, 31)],
                          'wraparound' : True,
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
    """
    Read GLDAS 21 Sm and temp data, mask based on frozen soil and create
    sm anomalies based on 2000-2010 clim.
    """
    reader_kwargs = {'dataset': ('GLDAS21', 'core'),
                     'force_path_group' : 'radar',
                     'parameters': ['SoilMoi0_10cm_inst', 'SoilTMP0_10cm_inst'],
                     'ioclass_kws': {'read_bulk': True}}

    # keep only obs where temp >= 277.15°C
    selfmaskingadapter_kwargs = {'op' : '>=', 'threshold' : 277.15,
                                 'column_name' : 'SoilTMP0_10cm_inst'}
    climadapter_kwargs = {'columns' : ['SoilMoi0_10cm_inst'],
                          'wraparound' : True,
                          'timespan': [datetime(2000,1,1), datetime(2010,12,31)],
                          'moving_avg_clim' : 30}
    resample = ('1D', 'mean')
    params_rename = {'SoilMoi0_10cm_inst': 'sm', 'SoilTMP0_10cm_inst': 'tmp'}

    fancyreader = GeoTsReader(GeoGLDAS21Ts, reader_kwargs, selfmaskingadapter_kwargs,
                              climadapter_kwargs, resample, params_rename)

    ts = fancyreader.read(*test_loc)

    ts = ts.dropna(how='all')
    assert np.all(ts.columns.values == ['sm', 'tmp'])
    assert np.all(ts['tmp'].dropna().values >= 277.15)
    assert not ts.empty
    print(ts)

def test_insitu_data():
    """
    Read GLDAS 21 Sm and temp data, mask based on frozen soil and create
    sm anomalies based on 2000-2010 clim.
    """
    reader_kwargs = {'dataset': ('ISMN', 'v20191211'),
                     'network': 'COSMOS',
                     'force_path_group': '__test',
                     'parameters': ['soil moisture', 'flag']}

    # keep only obs where temp >= 277.15°C
    selfmaskingadapter_kwargs = {'op' : '==', 'threshold' : 'G',
                                 'column_name' : 'soil moisture_flag'}
    climadapter_kwargs = {'columns' : ['soil moisture'],
                          'wraparound' : True,
                          'timespan': [datetime(2010,1,1), datetime(2019,12,31)],
                          'moving_avg_clim' : 30}
    resample = None
    params_rename = {'soil moisture': 'initu_sm'}


    fancyreader = GeoTsReader(GeoISMNTs, reader_kwargs, selfmaskingadapter_kwargs,
                              climadapter_kwargs, resample, params_rename)
    fancyreader.reader.reset_python_metadata()

    nearest, dist = fancyreader.reader.find_nearest_station(-155.5, 19.9,
                                                            return_distance=True)
    ids = fancyreader.reader.get_dataset_ids('soil moisture',
                                             min_depth=0, max_depth=0.17)
    ts = fancyreader.read(ids[0]) # read and mask
    assert all(ts['soil moisture_flag'].values == 'G')
    df_drop = ts['initu_sm'].dropna()
    assert not df_drop.empty


if __name__ == '__main__':
    #test_model_data()
    #test_sat_data()
    test_insitu_data()

