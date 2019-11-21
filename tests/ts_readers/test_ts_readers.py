# -*- coding: utf-8 -*-

"""
Module description
"""
# TODO:
#   (+) 
#---------
# NOTES:
#   -

from src.io_utils.read.time_series import *
from pytesmo.validation_framework.adapters import SelfMaskingAdapter


def test_cci_v4_reader():
    for vers in ['v045', 'v044']:
        for prod in ['COMBINED', 'ACTIVE', 'PASSIVE']:
            reader = GeoCCISMv4Ts(dataset=('ESA_CCI_SM', vers, prod),
                                  exact_index=True,
                                  ioclass_kws={'read_bulk': True},
                                  parameters=['sm', 'sm_uncertainty', 'flag'],
                                  scale_factors={'sm': 100.})
            reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
            ts = reader.read(15,48)
            assert not ts.dropna(how='all').empty
            print(ts)

def test_era5_reader():
    reader = GeoEra5Ts(dataset=('ERA5', 'core'),
                       ioclass_kws={'read_bulk': True},
                       parameters=['swvl1'], scale_factors={'swvl1': 1.})
    ts = reader.read(15,48)
    assert not ts.dropna(how='all').empty
    print(ts)

def test_era5land_reader():
    reader = GeoEra5LandTs(group_vars={'sm_precip_lai': ['swvl1'], 'temperature': ['stl1']},
                           ioclass_kws={'read_bulk': True}, scale_factors={'swvl1': 1.})
    ts = reader.read(15,48)
    assert not ts.dropna(how='all').empty
    print(ts)

    reader = GeoEra5LandTs(group_vars={'snow':['snowc']}, ioclass_kws={'read_bulk': True},
                           scale_factors={'snowc': 1.})
    ts = reader.read(15,48)
    assert not ts.dropna(how='all').empty
    print(ts)

def test_eraint_reader():
    reader = GeoEraIntGBG4Ts(dataset=('ERAINT-Land', 'GBG4', 'core'),
                           ioclass_kws={'read_bulk': True},
                           parameters=['39'], scale_factors={'39': 100.})
    ts = reader.read(15,48)
    assert not ts.dropna(how='all').empty

    print(ts)

def test_C3S201706_single_readers():
    for record in ['TCDR', 'ICDR']:
        for dataset in ['COMBINED', 'ACTIVE', 'PASSIVE']:
            reader = GeoC3Sv201706Ts(dataset=('C3S', 'v201706', dataset, record),
                grid_path=None, ioclass_kws={'read_bulk': True},
                parameters=['sm', 'sm_uncertainty', 'flag'], scale_factors={'sm': 100.})
            ts = reader.read(15,48)
            assert not ts.dropna(how='all').empty
            print(ts)

def test_C3S201706_combined_readers():
    reader = GeoC3Sv201706FullCDRTs(dataset=('C3S', 'v201706', 'COMBINED'),
        grid_path=None, ioclass_kws={'read_bulk': True},
        parameters=['sm', 'flag', 'sm_uncertainty'], scale_factors={'sm': 100.})
    reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    ts = reader.read(15,48)
    assert not ts.dropna(how='all').empty
    print(ts)

def test_C3S201812_single_readers():
    for dataset in ['COMBINED', 'ACTIVE', 'PASSIVE']:
        reader = GeoC3Sv201706Ts(dataset=('C3S', 'v201706', dataset, 'TCDR'),
            grid_path=None, ioclass_kws={'read_bulk': True},
            parameters=['sm', 'sm_uncertainty', 'flag'], scale_factors={'sm': 1.})
        reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
        ts = reader.read(15,48)
        assert not ts.dropna(how='all').empty
        print(ts)

def test_gldas20_ts_reader():
    reader = GeoGLDAS20Ts(dataset=('GLDAS20', 'core'),
                           ioclass_kws={'read_bulk': True},
                           parameters=['SoilMoi0_10cm_inst'], scale_factors=None)
    ts = reader.read(15,48)
    assert not ts.dropna(how='all').empty
    print(ts)

def test_gldas21_ts_reader():
    reader = GeoGLDAS21Ts(dataset=('GLDAS21', 'core'),
                           ioclass_kws={'read_bulk': True},
                           parameters=['SoilMoi0_10cm_inst'], scale_factors=None)
    ts = reader.read(15,48)
    assert not ts.dropna(how='all').empty
    print(ts)

def test_merra2_ts_reader():
    reader = GeoMerra2Ts(dataset=('MERRA2', 'core'),
                         ioclass_kws={'read_bulk': True},
                         parameters=['SFMC'], scale_factors={'SFMC': 100.})
    ts = reader.read(15,48)
    assert not ts.dropna(how='all').empty
    print(ts)


if __name__ == '__main__':
    test_era5land_reader()
    test_era5_reader()
    test_C3S201706_single_readers()
    test_C3S201812_single_readers()
    test_C3S201706_combined_readers()
    test_cci_v4_reader()
    test_merra2_ts_reader()
    test_gldas21_ts_reader()
    test_gldas20_ts_reader()
    test_eraint_reader()

