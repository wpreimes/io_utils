# -*- coding: utf-8 -*-

"""
Test the readers for which there is no test data in this package,
readers will use the shared datapool.
"""

import pytest
import io_utils.root_path as root_path
from io_utils.read.geo_ts_readers import *
test_loc = (15, 45)

def print_test_config(dataset, path_group=None):
    ds = dataset
    pg = path_group if path_group is not None else 'storage'
    print('Test reading {} data from {}.'.format(ds, pg))

@pytest.mark.geo_test_data
def test_cciswi_v047_reader(verbose=False):
    if verbose: print('Test reading CCI47 SWI from storage.')
    reader = GeoSmecSwiRzsmnv0Ts(
        dataset_or_path=os.path.join(root_path.r, 'Projects', 'G3P', '07_data',
                                     'SWI', 'SWI_CCI_04.7', 'SWI_CCI_v04.7_TS'),
                          ioclass_kws={'read_bulk': True},
                          parameters=['SWI_001', 'SWI_010', 'QFLAG_001', 'QFLAG_010'],
                          scale_factors={'SWI_001': 1.})
    #reader = SelfMaskingAdapter(reader, '>', 1, 'QFLAG_001')
    ts = reader.read(*test_loc)
    assert not ts.empty
    if verbose: print(ts)

@pytest.mark.geo_test_data
def test_smecvrzsm_v0_reader(verbose=False):
    if verbose: print('Test reading C3S RZSMv0 from storage.')
    reader = GeoSmecSwiRzsmnv0Ts(
        dataset_or_path=os.path.join(root_path.r, 'Projects', 'G3P', '07_data',
                                     'C3S_v202012_RZSM', 'time_series'),
        ioclass_kws={'read_bulk': True},
        parameters=['QFLAG_0-10cm', 'SSM', 'RZSM_0-10cm'],
        scale_factors={'SSM': 1.})
    #reader = SelfMaskingAdapter(reader, '>', 1, 'QFLAG_001')
    ts = reader.read(*test_loc)
    assert not ts.empty
    if verbose: print(ts)

@pytest.mark.geo_test_data
def test_cci_v061_reader(verbose=False):
    vers = 'v061'
    for prod in ['COMBINED', 'ACTIVE', 'PASSIVE']:
        dataset = ('ESA_CCI_SM', vers, prod)
        if verbose: print_test_config(dataset)
        reader = GeoCCISMv6Ts(dataset_or_path=dataset,
                              exact_index=False,
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
    reader = GeoEra5LandTs(group_vars={'sm_precip_lai': ['swvl1'],
                                       'temperature': ['stl1']},
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
    force_path_group = 'radar'
    if verbose: print_test_config(dataset, force_path_group)

    reader = GeoC3Sv201706FullCDRTs(
        dataset=dataset,
        grid=None, ioclass_kws={'read_bulk': True},
        exact_index=True, parameters=['sm', 'flag', 'sm_uncertainty'],
        scale_factors={'sm': 1.}, force_path_group=force_path_group)
    #reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    ts = reader.read(*test_loc)
    if verbose: print(ts)
    assert not ts.dropna(how='all').empty

@pytest.mark.geo_test_data
@pytest.mark.parametrize("version", ['v201912', 'v202012'])
@pytest.mark.parametrize("product", ['ACTIVE', 'PASSIVE', 'COMBINED'])
def test_C3S_single_monthly_readers(version, product, verbose=False):
    dataset = ('C3S', version, product, 'MONTHLY', 'TCDR')
    if verbose: print_test_config(dataset)
    reader = eval(f"GeoC3S{version}Ts")(
        dataset_or_path=dataset,
        grid=None, ioclass_kws={'read_bulk': True},
        parameters=['sm', 'freqbandID', 'nobs'], scale_factors={'sm': 1.})
    ts = reader.read(*test_loc)
    if verbose: print(ts)
    assert not ts.dropna(how='all').empty


@pytest.mark.geo_test_data
def test_C3S201912_single_daily_readers(verbose=False):

    dataset = ('C3S', 'v201912', 'COMBINED', 'DAILY', 'TCDR')
    if verbose: print_test_config(dataset)
    reader = GeoC3Sv201912Ts(
        dataset_or_path=dataset,
        grid=None, ioclass_kws={'read_bulk': True}, exact_index=True,
        parameters=['sm', 'sm_uncertainty', 'flag'], scale_factors={'sm': 1.})
    reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    ts = reader.read(*test_loc)
    if verbose: print(ts)
    assert not ts.dropna(how='all').empty

    dataset = ('C3S', 'v201912', 'ACTIVE', 'DAILY', 'TCDR')
    if verbose: print_test_config(dataset)
    reader = GeoC3Sv201912Ts(
        dataset_or_path=dataset,
        grid=None, ioclass_kws={'read_bulk': True}, exact_index=True,
        parameters=['sm', 'sm_uncertainty', 'flag'], scale_factors={'sm': 1.})
    reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    ts = reader.read(*test_loc)
    if verbose: print(ts)
    assert not ts.dropna(how='all').empty

    dataset = ('C3S', 'v201912', 'PASSIVE', 'DAILY', 'TCDR')
    if verbose: print_test_config(dataset)
    reader = GeoC3Sv201912Ts(
        dataset_or_path=dataset,
        grid=None, ioclass_kws={'read_bulk': True}, exact_index=True,
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
                         ioclass_kws={'read_bulk': True}, exact_index=True,
                         parameters=['soil_moisture', 'retrieval_qual_flag'],
                         scale_factors={'soil_moisture': 1.})
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
    reader = GeoAmsr2LPRMv6Ts(dataset_or_path=dataset, exact_index=True,
                              ioclass_kws={'read_bulk': True},
                              parameters=['SM_069', 'MASK'], scale_factors=None)
    ts = reader.read(*test_loc)
    if verbose: print(ts)
    assert not ts.dropna(how='all').empty

@pytest.mark.skipif(not pygenio_available,
                    reason="Pygenio is not installed.")
@pytest.mark.geo_test_data
def test_amsr2ccids_ts_reader(verbose=False):
    dataset = ('CCIDs', 'v052', 'AMSR2', 'DES')
    reader = GeoCCIDsAmsr2Ts(dataset,
                         parameters=['sm', 'flag', 'freqband'],
                         exact_index=True,
                         ioclass_kws={'read_bulk': True})
    ts = reader.read(*test_loc)
    if verbose: print(ts)
    assert not ts.dropna(how='all').empty

@pytest.mark.geo_test_data
def test_ascatssm_ts_reader(verbose=False):
    dataset = ('HSAF_ASCAT', 'SSM', 'H115+H116')
    grid_path = os.path.join(root_path.r, 'Projects',
                        'H_SAF_CDOP3', '05_deliverables_products',
                        'auxiliary','warp5_grid', 'TUW_WARP5_grid_info_2_3.nc')
    reader = GeoHsafAscatSsmTs(dataset,
                               grid_path=grid_path,
                               parameters=['sm', 'proc_flag', 'conf_flag'],
                               exact_index=True,
                               ioclass_kws={'read_bulk': True})
    ts = reader.read(*test_loc)
    if verbose: print(ts)
    assert not ts.dropna(how='all').empty

@pytest.mark.skipif(not pygenio_available,
                    reason="Pygenio is not installed.")
@pytest.mark.geo_test_data
def test_ccigenio_ts_reader(verbose=False):
    path = os.path.join(root_path.r, 'Projects', "CCIplus_Soil_Moisture",
                        "07_data", "ESA_CCI_SM_v06.1", "042_combined_MergedProd")
    reader = GeoCCISMv6GenioTs(path,
                               parameters=['sm', 'flag', 'freqband'],
                               exact_index=False)
    ts = reader.read(*test_loc)
    if verbose: print(ts)
    assert not ts.dropna(how='all').empty

# if __name__ == '__main__':
#     v = True
#     test_SMAP_spl3_v6_reader(v)
#
    # test_C3S201706_combined_readers(v)
#
#     test_ascatssm_ts_reader(v)
#
#     test_cciswi_v047_reader(v)
#
#     test_cci_v061_reader(v)
#
#     test_ccigenio_ts_reader()
#
#
#     test_amsr2ccids_ts_reader(v)
#     test_amsr2lprm_ts_reader(mode='ASC', verbose=v)
#     test_gldas20_ts_reader(v)
#     test_era5land_merged_reader(v)
#     test_era5land_snow_reader(v)
#     test_eraint_reader(v)





