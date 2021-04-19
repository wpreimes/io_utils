# -*- coding: utf-8 -*-

import pytest
from io_utils.read.geo_ts_readers.ts_reader import GeoTsReader
import pandas as pd
from io_utils.read.geo_ts_readers import GeoCCISMv4Ts, GeoGLDAS21Ts, GeoISMNTs, GeoHsafAscatSsmTs, GeoEra5LandTs
import numpy as np
from datetime import datetime
import os
import io_utils.root_path as root_path
test_loc = (15, 45)

@pytest.mark.geo_test_data
def test_ascat_sat_data():
    """
    Read ESA CCI SM 45 data, mask based on goodl-flags soil and create
    sm anomalies based on 1991-2010 clim.
    """
    grid_path = os.path.join(root_path.r, 'Projects',
                        'H_SAF_CDOP3', '05_deliverables_products',
                        'auxiliary','warp5_grid', 'TUW_WARP5_grid_info_2_3.nc')

    reader_kwargs = {'dataset_or_path': ('HSAF_ASCAT', 'SSM', 'H115+H116'),
                     'force_path_group': 'radar',
                     'grid_path': grid_path,
                     'parameters': ['sm', 'proc_flag', 'conf_flag'],
                     'ioclass_kws': {'read_bulk': True}}

    selfmaskingadapter_kwargs = [{'op' : '==', 'threshold' : 0,
                                 'column_name' : 'proc_flag'},
                                 {'op': '==', 'threshold': 0,
                                  'column_name': 'conf_flag'},
                                 {'op': '<=', 'threshold': 50,
                                  'column_name': 'sm'}]

    climadapter_kwargs = None

    resample = ('1D', 'mean')
    params_rename = {'sm': 'ascat_sm'}

    fancyreader = GeoTsReader(GeoHsafAscatSsmTs, reader_kwargs, selfmaskingadapter_kwargs,
                              climadapter_kwargs, resample, filter_months=None,
                              params_rename=params_rename)

    ts = fancyreader.read(*test_loc)

    ts = ts.dropna(how='all')
    assert np.all(ts.columns.values == ['ascat_sm', 'proc_flag', 'conf_flag'])
    assert np.all(ts['proc_flag'].dropna().values == 0.)
    assert np.all(ts['conf_flag'].dropna().values == 0.)
    assert np.all(ts['ascat_sm'].dropna().values <= 50.)
    assert not ts.empty
    print(ts)


@pytest.mark.geo_test_data
def test_cci_sat_data():
    """
    Read ESA CCI SM 45 data, mask based on goodl-flags soil and create
    sm anomalies based on 1991-2010 clim.
    """
    reader_kwargs = {'dataset_or_path': ('ESA_CCI_SM', 'v047', 'COMBINED'),
                     'force_path_group': 'radar',
                     'exact_index': True,
                     'parameters': ['sm', 'flag', 't0', 'sm_uncertainty'],
                     'ioclass_kws': {'read_bulk': True}}

    selfmaskingadapter_kwargs = [{'op' : '==', 'threshold' : 0,
                                 'column_name' : 'flag'}]

    climadapter_kwargs = {'columns' : ['sm'],
                          'timespan': [datetime(1991, 1, 1), datetime(2010, 12, 31)],
                          'wraparound' : True,
                          'moving_avg_clim' : 30}
    resample = ('10D', 'mean')
    params_rename = {'sm': 'esa_cci_sm'}

    fancyreader = GeoTsReader(GeoCCISMv4Ts, reader_kwargs, selfmaskingadapter_kwargs,
                              climadapter_kwargs, resample, filter_months=None,
                              params_rename=params_rename)

    ts = fancyreader.read(*test_loc)

    ts = ts.dropna(how='all')
    assert np.all(ts.columns.values == ['esa_cci_sm', 'flag', 'sm_uncertainty'])
    assert np.all(ts['flag'].dropna().values == 0.)
    assert np.all(ts['esa_cci_sm'].values <= 0.1)
    assert not ts.empty
    print(ts)

@pytest.mark.geo_test_data
def test_gldas_model_data():
    """
    Read GLDAS 21 Sm and temp data, mask based on frozen soil and create
    sm anomalies based on 2000-2010 clim.
    """
    reader_kwargs = {'dataset_or_path': ('GLDAS21', 'core'),
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
                              climadapter_kwargs, resample, filter_months=None,
                              params_rename=params_rename)

    ts = fancyreader.read(*test_loc)

    ts = ts.dropna(how='all')
    assert np.all(ts.columns.values == ['sm', 'tmp'])
    assert np.all(ts['tmp'].dropna().values >= 277.15)
    assert not ts.empty
    print(ts)

@pytest.mark.geo_test_data
def test_era5land_rean_data():
    reader_kwargs = {'group_vars':{'sm_precip_lai': ['swvl1'],
                                      'temperature': ['stl1']},
                          'ioclass_kws': {'read_bulk': True}}

    # keep only obs where temp >= 277.15°C
    selfmaskingadapter_kwargs = {'op' : '>=',
                                 'threshold' : 277.15,
                                 'column_name' : 'stl1'}

    climadapter_kwargs = {'columns' : ['swvl1'],
                          'wraparound' : True,
                          'timespan': [datetime(2000,1,1), datetime(2010,12,31)],
                          'moving_avg_clim' : 30}
    resample = None
    params_rename = {'swvl1': 'swvl1', 'stl1': 'stl1'}

    fancyreader = GeoTsReader(GeoEra5LandTs, reader_kwargs, selfmaskingadapter_kwargs,
                              climadapter_kwargs, resample, filter_months=None,
                              params_rename=params_rename)

    ts = fancyreader.read(*test_loc)

    ts = ts.dropna(how='all')
    assert np.all(ts.columns.values == ['swvl1', 'stl1'])
    assert np.all(ts['stl1'].dropna().values >= 277.15)
    assert not ts.empty
    print(ts)

def test_insitu_data():
    """
    Read GLDAS 21 Sm and temp data, mask based on frozen soil and create
    sm anomalies based on 2000-2010 clim.
    """
    reader_kwargs = {'dataset_or_path': ('ISMN', 'v20191211'),
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
                              climadapter_kwargs, resample, filter_months=None,
                              params_rename=params_rename)
    fancyreader.base_reader.reset_python_metadata()

    nearest, dist = fancyreader.base_reader.find_nearest_station(-155.5, 19.9,
                                                            return_distance=True)
    ids = fancyreader.base_reader.get_dataset_ids('soil moisture',
                                             min_depth=0, max_depth=0.17)
    ts = fancyreader.read(ids[0]) # read and mask
    assert all(ts['soil moisture_flag'].values == 'G')
    df_drop = ts['initu_sm'].dropna()
    assert not df_drop.empty


if __name__ == '__main__':
    test_era5land_rean_data()
    # test_gldas_model_data()
    # test_ascat_sat_data()
    # test_cci_sat_data()
    # test_insitu_data()

