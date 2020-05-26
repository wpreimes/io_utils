# -*- coding: utf-8 -*-

"""
Test the readers for which there is no test data in this package,
readers will use the shared datapool.
"""

import pytest
from io_utils.read.geo_ts_readers import *
test_loc = (15, 45)

def print_test_config(dataset, path_group=None):
    ds = dataset
    pg = path_group if path_group is not None else 'storage'
    print('Test reading {} data from {}.'.format(ds, pg))

@pytest.mark.geo_test_data
def test_cciswi_v047_reader(verbose=False):
    if verbose: print('Test reading CCI47 SWI from storage.')
    vers = 'v047'
    reader = GeoCCISWIv4Ts(dataset_or_path=('ESA_CCI_SWI', vers),
                          ioclass_kws={'read_bulk': True},
                          parameters=['SWI_001', 'SWI_010', 'QFLAG_001', 'QFLAG_010'],
                          scale_factors={'SWI_001': 1.})
    #reader = SelfMaskingAdapter(reader, '>', 1, 'QFLAG_001')
    ts = reader.read(*test_loc)
    assert not ts.empty
    if verbose: print(ts)

@pytest.mark.geo_test_data
def test_cci_v045_reader(verbose=False):
    if verbose: print('Test reading CCI45, Combined, passive from storage.')
    vers = 'v045'
    for prod in ['COMBINED', 'ACTIVE', 'PASSIVE']:
        reader = GeoCCISMv4Ts(dataset_or_path=('ESA_CCI_SM', vers, prod),
                              exact_index=True,
                              ioclass_kws={'read_bulk': True},
                              parameters=['sm', 'sm_uncertainty', 'flag', 't0'],
                              scale_factors={'sm': 1.})
        #reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
        ts = reader.read(*test_loc)
        assert not ts.empty
        if verbose: print(ts)

@pytest.mark.geo_test_data
def test_cci_v044_reader(verbose=False):
    vers = 'v044'
    for prod in ['COMBINED', 'ACTIVE', 'PASSIVE']:
        dataset = ('ESA_CCI_SM', vers, prod)
        if verbose: print_test_config(dataset)
        reader = GeoCCISMv4Ts(dataset_or_path=dataset,
                              exact_index=True,
                              ioclass_kws={'read_bulk': True},
                              parameters=['sm', 'sm_uncertainty', 'flag', 't0'],
                              scale_factors={'sm': 1.})
        #reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
        ts = reader.read(*test_loc)
        assert not ts.empty
        if verbose: print(ts)

@pytest.mark.geo_test_data
def test_era5land_merged_reader(verbose=False):
    if verbose: print('Test reading ERA5Land MERGED sm/temp data from storage.')
    reader = GeoEra5LandTs(group_vars={'sm_precip_lai': ['swvl1'], 'temperature': ['stl1']},
                           ioclass_kws={'read_bulk': True}, scale_factors={'swvl1': 1.})
    ts = reader.read(*test_loc)
    assert not ts.dropna(how='all').empty
    if verbose: print(ts)

@pytest.mark.geo_test_data
# no test data for this test in the repo
def test_era5land_snow_reader(verbose=False):
    if verbose: print('Test reading ERA5Land, snow data from storage.')
    reader = GeoEra5LandTs(group_vars={'snow':['snowc']}, ioclass_kws={'read_bulk': True},
                           scale_factors={'snowc': 1.})
    ts = reader.read(*test_loc)
    assert not ts.dropna(how='all').empty
    if verbose: print(ts)

@pytest.mark.geo_test_data
def test_eraint_reader(verbose=False):
    dataset = ('ERAINT-Land', 'GBG4', 'core')
    if verbose: print_test_config(dataset)
    reader = GeoEraIntGBG4Ts(dataset_or_path=dataset,
                           ioclass_kws={'read_bulk': True},
                           parameters=['39'], scale_factors={'39': 1.})
    ts = reader.read(*test_loc)
    if verbose: print(ts)
    assert not ts.dropna(how='all').empty

@pytest.mark.geo_test_data
def test_C3S201706_combined_readers(verbose=False):
    dataset = ('C3S', 'v201706', 'COMBINED',  'DAILY')
    force_path_group = '__test'
    if verbose: print_test_config(dataset, force_path_group)

    reader = GeoC3Sv201706FullCDRTs(dataset=dataset,
        grid_path=None, ioclass_kws={'read_bulk': True},
        parameters=['sm', 'flag', 'sm_uncertainty'], scale_factors={'sm': 1.},
        force_path_group=force_path_group)
    #reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    ts = reader.read(*test_loc)
    if verbose: print(ts)
    assert not ts.dropna(how='all').empty

@pytest.mark.geo_test_data
def test_C3S201912_single_monthly_readers(verbose=False):

    dataset = ('C3S', 'v201912', 'COMBINED', 'MONTHLY', 'TCDR')
    if verbose: print_test_config(dataset)
    reader = GeoC3Sv201912Ts(dataset_or_path=dataset,
        grid_path=None, ioclass_kws={'read_bulk': True},
        parameters=['sm', 'freqbandID', 'nobs'], scale_factors={'sm': 1.})
    ts = reader.read(*test_loc)
    if verbose: print(ts)
    assert not ts.dropna(how='all').empty

    dataset = ('C3S', 'v201912', 'ACTIVE', 'MONTHLY', 'TCDR')
    if verbose: print_test_config(dataset)
    reader = GeoC3Sv201912Ts(dataset_or_path=dataset,
        grid_path=None, ioclass_kws={'read_bulk': True},
        parameters=['sm', 'freqbandID', 'nobs'], scale_factors={'sm': 1.})
    ts = reader.read(*test_loc)
    if verbose: print(ts)
    assert not ts.dropna(how='all').empty

    dataset = ('C3S', 'v201912', 'PASSIVE', 'MONTHLY', 'TCDR')
    if verbose: print_test_config(dataset)
    reader = GeoC3Sv201912Ts(dataset_or_path=dataset,
        grid_path=None, ioclass_kws={'read_bulk': True},
        parameters=['sm', 'freqbandID', 'nobs'], scale_factors={'sm': 1.})
    ts = reader.read(*test_loc)
    if verbose: print(ts)
    assert not ts.dropna(how='all').empty


@pytest.mark.geo_test_data
def test_C3S201912_single_daily_readers(verbose=False):

    dataset = ('C3S', 'v201912', 'COMBINED', 'DAILY', 'TCDR')
    if verbose: print_test_config(dataset)
    reader = GeoC3Sv201912Ts(dataset_or_path=dataset,
        grid_path=None, ioclass_kws={'read_bulk': True},
        parameters=['sm', 'sm_uncertainty', 'flag'], scale_factors={'sm': 1.})
    reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    ts = reader.read(*test_loc)
    if verbose: print(ts)
    assert not ts.dropna(how='all').empty

    dataset = ('C3S', 'v201912', 'ACTIVE', 'DAILY', 'TCDR')
    if verbose: print_test_config(dataset)
    reader = GeoC3Sv201912Ts(dataset_or_path=dataset,
        grid_path=None, ioclass_kws={'read_bulk': True},
        parameters=['sm', 'sm_uncertainty', 'flag'], scale_factors={'sm': 1.})
    reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    ts = reader.read(*test_loc)
    if verbose: print(ts)
    assert not ts.dropna(how='all').empty

    dataset = ('C3S', 'v201912', 'PASSIVE', 'DAILY', 'TCDR')
    if verbose: print_test_config(dataset)
    reader = GeoC3Sv201912Ts(dataset_or_path=dataset,
        grid_path=None, ioclass_kws={'read_bulk': True},
        parameters=['sm', 'sm_uncertainty', 'flag'], scale_factors={'sm': 1.})
    reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    ts = reader.read(*test_loc)
    if verbose: print(ts)
    assert not ts.dropna(how='all').empty

@pytest.mark.geo_test_data
def test_SMAP_spl3_v6_reader(verbose=False):
    dataset = ('SMAP', 'SP3SMPv6', 'ASC')
    if verbose: print_test_config(dataset)

    smap_reader = GeoSpl3smpTs(dataset_or_path=dataset,
                         ioclass_kws={'read_bulk': True},
                         parameters=['soil_moisture', 'retrieval_qual_flag'],
                         scale_factors={'soil_moisture_pm': 1.})
    celldata = smap_reader.read_cells([166])
    assert any([not data.empty for gpi, data in celldata.items()])
    smap_reader = SelfMaskingAdapter(smap_reader, '!=', 999, 'retrieval_qual_flag')
    ts = smap_reader.read(*test_loc)
    if verbose: print(ts)
    assert not ts.empty

@pytest.mark.geo_test_data
def test_gldas20_ts_reader(verbose=False):
    dataset = ('GLDAS20', 'core')
    reader = GeoGLDAS20Ts(dataset_or_path=dataset,
                          ioclass_kws={'read_bulk': True},
                          parameters=['SoilMoi0_10cm_inst'], scale_factors=None)
    ts = reader.read(*test_loc)
    if verbose: print(ts)
    assert not ts.dropna(how='all').empty
    # print(ts)

@pytest.mark.geo_test_data
@pytest.mark.parametrize('mode', ['ASC', 'DES'])
def test_amsr2lprm_ts_reader(mode, verbose=False):
    dataset = ('AMSR2', 'LPRM', 'v6', mode)
    reader = GeoAmsr2LPRMv6Ts(dataset_or_path=dataset,
                              ioclass_kws={'read_bulk': True},
                              parameters=['SM_069', 'MASK'], scale_factors=None)
    ts = reader.read(*test_loc)
    if verbose: print(ts)
    assert not ts.dropna(how='all').empty


if __name__ == '__main__':
    v = True
    test_amsr2lprm_ts_reader(verbose=v)
    test_cciswi_v047_reader(v)
    test_SMAP_spl3_v6_reader(v)
    test_gldas20_ts_reader(v)
    test_cci_v045_reader(v)
    test_cci_v044_reader(v)
    test_era5land_merged_reader(v)
    test_era5land_snow_reader(v)
    test_eraint_reader(v)
    test_C3S201706_combined_readers(v)
    test_C3S201912_single_monthly_readers(v)
    test_C3S201912_single_daily_readers(v)

