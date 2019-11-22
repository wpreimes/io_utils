# -*- coding: utf-8 -*-

"""
Test the readers for which there is no test data in this package,
readers will use the shared datapool.

"""
# TODO:
#   (+) 
#---------
# NOTES:
#   -

import pytest
import matplotlib.pyplot as plt
from io_utils.read.geo_ts_readers import *

#stest_loc = (-155.875, 19.625)
test_loc = (15, 45)


@pytest.mark.geo_test_data
def test_cci_v045_reader():
    vers = 'v045'
    for prod in ['COMBINED', 'ACTIVE', 'PASSIVE']:
        reader = GeoCCISMv4Ts(dataset=('ESA_CCI_SM', vers, prod),
                              exact_index=True,
                              ioclass_kws={'read_bulk': True},
                              parameters=['sm', 'sm_uncertainty', 'flag', 't0'],
                              scale_factors={'sm': 1.})
        #reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
        ts = reader.read(*test_loc)
        assert not ts.empty
        print(ts)

@pytest.mark.geo_test_data
def test_cci_v044_reader():
    vers = 'v044'
    for prod in ['COMBINED', 'ACTIVE', 'PASSIVE']:
        reader = GeoCCISMv4Ts(dataset=('ESA_CCI_SM', vers, prod),
                              exact_index=True,
                              ioclass_kws={'read_bulk': True},
                              parameters=['sm', 'sm_uncertainty', 'flag', 't0'],
                              scale_factors={'sm': 1.})
        #reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
        ts = reader.read(*test_loc)
        assert not ts.empty
        print(ts)

@pytest.mark.geo_test_data
def test_era5land_merged_reader():
    reader = GeoEra5LandTs(group_vars={'sm_precip_lai': ['swvl1'], 'temperature': ['stl1']},
                           ioclass_kws={'read_bulk': True}, scale_factors={'swvl1': 1.})
    ts = reader.read(*test_loc)
    assert not ts.dropna(how='all').empty
    #print(ts)

@pytest.mark.geo_test_data
# no test data for this test in the repo
def test_era5land_snow_reader():
    reader = GeoEra5LandTs(group_vars={'snow':['snowc']}, ioclass_kws={'read_bulk': True},
                           scale_factors={'snowc': 1.})
    ts = reader.read(*test_loc)
    assert not ts.dropna(how='all').empty
    #print(ts)

@pytest.mark.geo_test_data
def test_eraint_reader():
    reader = GeoEraIntGBG4Ts(dataset=('ERAINT-Land', 'GBG4', 'core'),
                           ioclass_kws={'read_bulk': True},
                           parameters=['39'], scale_factors={'39': 100.})
    ts = reader.read(*test_loc)
    assert not ts.dropna(how='all').empty

    #print(ts)

@pytest.mark.geo_test_data
def test_C3S201706_combined_readers():
    force_path_group = '_test'
    reader = GeoC3Sv201706FullCDRTs(dataset=('C3S', 'v201706', 'COMBINED'),
        grid_path=None, ioclass_kws={'read_bulk': True},
        parameters=['sm', 'flag', 'sm_uncertainty'], scale_factors={'sm': 100.},
        force_path_group=force_path_group)
    reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    ts = reader.read(*test_loc)
    assert not ts.dropna(how='all').empty
    #print(ts)

if __name__ == '__main__':
    test_cci_v045_reader()
    #test_cci_v044_reader()
    #test_era5land_snow_reader()
    #test_eraint_reader()
    #test_C3S201706_combined_readers()


