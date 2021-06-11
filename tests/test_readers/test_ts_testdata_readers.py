# -*- coding: utf-8 -*-

"""
Test the readers for which there is test data in this package
"""
from io_utils.read.geo_ts_readers import *
import pytest

test_loc = (-155.875, 19.625)

def test_read_applied():
    force_path_group = '__test'
    reader = GeoCCISMv6Ts(dataset_or_path=('ESA_CCI_SM', 'v061', 'COMBINED'),
                    exact_index=True,
                    ioclass_kws={'read_bulk': True},
                    parameters=['sm', 'sm_uncertainty', 't0'],
                    scale_factors={'sm': 1.},
                    force_path_group=force_path_group)
    ts = reader.read(*test_loc)
    assert not ts.empty

def test_smosic_reader():
    force_path_group = '__test'
    smos_reader = GeoSMOSICTs(dataset_or_path=('SMOS', 'IC', 'ASC'),
                              ioclass_kws={'read_bulk': True},
                              parameters=['Soil_Moisture', 'Quality_Flag'],
                              scale_factors={'sm': 1.},
                              force_path_group=force_path_group)
    celldata = smos_reader.read_cells([165,166])
    assert any([not data.empty for gpi, data in celldata.items()])
    smos_reader = SelfMaskingAdapter(smos_reader, '==', 0, 'Quality_Flag')
    ts = smos_reader.read(*test_loc)
    assert not ts.empty

def test_smap_spl3_v5_reader():
    force_path_group = '__test'
    smap_reader = GeoSpl3smpTs(dataset_or_path=('SMAP', 'SP3SMPv5', 'ASC'),
                               ioclass_kws={'read_bulk': True},
                               parameters=['soil_moisture_pm', 'retrieval_qual_flag_pm'],
                               scale_factors={'soil_moisture_pm': 1.},
                               force_path_group=force_path_group)
    celldata = smap_reader.read_cells([165,166])
    assert any([not data.empty for gpi, data in celldata.items()])
    smap_reader = SelfMaskingAdapter(smap_reader, '!=', 999, 'retrieval_qual_flag_pm')
    ts = smap_reader.read(*test_loc)
    assert not ts.empty

def test_cci_v033_reader():
    vers = 'v033'
    force_path_group = '__test'

    ## == active
    reader = GeoCCISMv3Ts(dataset_or_path=('ESA_CCI_SM', vers, 'ACTIVE'),
                          exact_index=False, # works only after 47
                          ioclass_kws={'read_bulk': True},
                          parameters=['sm', 'sm_uncertainty', 't0'],
                          scale_factors={'sm': 1.},
                          force_path_group=force_path_group)
    #reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    cell_data = reader.read_cells([165,166]) # all empty
    ts = reader.read(633697)
    # TODO: times are wrong
    assert not ts.empty

    ## == combined
    reader = GeoCCISMv3Ts(dataset_or_path=('ESA_CCI_SM', vers, 'COMBINED'),
                          exact_index=False,
                          ioclass_kws={'read_bulk': True},
                          parameters=['sm', 'sm_uncertainty', 't0'],
                          scale_factors={'sm': 1.},
                          force_path_group=force_path_group)
    #reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    cell_data = reader.read_cells([165,166]) # all empty
    ts = reader.read(633697)
    # TODO: times are wrong
    assert not ts.empty

    ## == passive
    reader = GeoCCISMv3Ts(dataset_or_path=('ESA_CCI_SM', vers, 'PASSIVE'),
                          exact_index=False,
                          ioclass_kws={'read_bulk': True},
                          parameters=['sm', 'sm_uncertainty', 't0'],
                          scale_factors={'sm': 1.},
                          force_path_group=force_path_group)
    #reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    cell_data = reader.read_cells([165,166]) # all empty
    ts = reader.read(633697)
    # TODO: times are wrong
    assert not ts.empty


@pytest.mark.parametrize("version,Reader",[
                         ("v045", GeoCCISMv4Ts),
                         ("v047", GeoCCISMv4Ts),
                         ("v052", GeoCCISMv5Ts),
                         ("v061", GeoCCISMv6Ts),
                         ])
def test_cci_reader(version, Reader):
    force_path_group = '__test'

    ## == active
    reader = Reader(dataset_or_path=('ESA_CCI_SM', version, 'ACTIVE'),
                          exact_index=True,
                          ioclass_kws={'read_bulk': True},
                          parameters=['sm', 'sm_uncertainty', 't0'],
                          scale_factors={'sm': 1.},
                          force_path_group=force_path_group)
    #reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    cell_data = reader.read_cells([165,166]) # all empty
    for col in cell_data.columns: # all empty
        assert cell_data[col].dropna().empty
    ts = reader.read(*test_loc)
    assert ts.dropna().empty
    reader.close()

    ## == combined
    reader = Reader(dataset_or_path=('ESA_CCI_SM', version, 'COMBINED'),
                          exact_index=True,
                          ioclass_kws={'read_bulk': True},
                          parameters=['sm', 'sm_uncertainty', 't0'],
                          scale_factors={'sm': 1.},
                          force_path_group=force_path_group)
    #reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    cell_data = reader.read_cells([165,166]) # not all empty
    assert not cell_data[(632257, 'sm')].dropna().empty
    ts = reader.read(632257).replace(-9999., np.nan)
    assert not ts.empty
    reader.close()

    ## == passive
    reader = Reader(dataset_or_path=('ESA_CCI_SM', version, 'PASSIVE'),
                          exact_index=True,
                          ioclass_kws={'read_bulk': True},
                          parameters=['sm', 'sm_uncertainty', 't0'],
                          scale_factors={'sm': 1.},
                          force_path_group=force_path_group)
    cell_data = reader.read_cells([165,166])
    assert isinstance(cell_data, pd.DataFrame)
    ts = reader.read(*test_loc)
    assert ts.dropna().empty


def test_era5_reader():
    force_path_group = '__test'
    reader = GeoEra5Ts(dataset_or_path=('ERA5', 'core'),
                       ioclass_kws={'read_bulk': True},
                       parameters=['swvl1'], scale_factors={'swvl1': 1.},
                       force_path_group=force_path_group)
    ts = reader.read(*test_loc)
    assert not ts.dropna(how='all').empty
    #print(ts)

def test_era5land_reader():
    force_path_group = '__test'
    reader = GeoEra5LandTs(group_vars={'sm_precip_lai': ['swvl1']},
                           ioclass_kws={'read_bulk': True},
                           scale_factors={'swvl1': 1.},
                           force_path_group=force_path_group)
    ts = reader.read(*test_loc)
    assert not ts.dropna(how='all').empty
    #print(ts)

def test_C3S201706_single_readers():
    force_path_group = '__test'
    for record in ['TCDR', 'ICDR']:
        dataset = 'ACTIVE'
        reader = GeoC3Sv201706Ts(
            dataset_or_path=('C3S', 'v201706', dataset, 'DAILY', record),
            grid=None, ioclass_kws={'read_bulk': True},
            parameters=['sm', 'sm_uncertainty', 'flag'], scale_factors={'sm': 1.},
            force_path_group=force_path_group)
        ts = reader.read(*test_loc)
        assert not ts.dropna(how='all').empty

        dataset = 'COMBINED'
        reader = GeoC3Sv201706Ts(
            dataset_or_path=('C3S', 'v201706', dataset, 'DAILY', record),
            grid=None, ioclass_kws={'read_bulk': True},
            parameters=['sm', 'sm_uncertainty', 'flag'], scale_factors={'sm': 1.},
            force_path_group=force_path_group)
        ts = reader.read(*test_loc)
        assert not ts.dropna(how='all').empty

        dataset = 'PASSIVE'
        reader = GeoC3Sv201706Ts(
            dataset_or_path=('C3S', 'v201706', dataset, 'DAILY', record),
            grid=None, ioclass_kws={'read_bulk': True},
            parameters=['sm', 'sm_uncertainty', 'flag'], scale_factors={'sm': 1.},
            force_path_group=force_path_group)
        ts = reader.read(*test_loc)
        assert not ts.dropna(how='all').empty
        #print(ts)

def test_C3S201812_single_readers():
    force_path_group = '__test'
    reader = GeoC3Sv201812Ts(
        dataset_or_path=('C3S', 'v201812', 'ACTIVE', 'DAILY', 'TCDR'),
        grid=None, ioclass_kws={'read_bulk': True},
        parameters=['sm', 'sm_uncertainty', 'flag'], scale_factors={'sm': 1.},
        force_path_group=force_path_group)
    reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    ts = reader.read(*test_loc)
    assert not ts.dropna(how='all').empty
    #print(ts)

    reader = GeoC3Sv201812Ts(
        dataset_or_path=('C3S', 'v201812', 'COMBINED', 'DAILY', 'TCDR'),
        grid=None, ioclass_kws={'read_bulk': True},
        parameters=['sm', 'sm_uncertainty', 'flag'], scale_factors={'sm': 1.},
        force_path_group=force_path_group)
    reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    ts = reader.read(*test_loc)
    assert not ts.dropna(how='all').empty
    #print(ts)

    # no data for the passive c3s there
    reader = GeoC3Sv201812Ts(
        dataset_or_path=('C3S', 'v201812', 'PASSIVE', 'DAILY', 'TCDR'),
        grid=None, ioclass_kws={'read_bulk': True},
        parameters=['sm', 'sm_uncertainty', 'flag'], scale_factors={'sm': 1.},
        force_path_group=force_path_group)
    reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    ts = reader.read(*test_loc)
    assert ts.empty # ATTENTION: passive data is empty here
    #print(ts)

@pytest.mark.parametrize("version,Reader",[
    ("v201706", GeoC3Sv201706Ts),
    ("v201812", GeoC3Sv201812Ts),
    ("v201912", GeoC3Sv201912Ts),
    ("v202012", GeoC3Sv202012Ts),
])
def test_C3S_single_readers(version, Reader):
    force_path_group = '__test'

    reader = Reader(
        dataset_or_path=('C3S', version, 'COMBINED', 'DAILY', 'TCDR'),
        grid=None, ioclass_kws={'read_bulk': True},
        parameters=['sm', 'sm_uncertainty', 'flag'],
                    scale_factors={'sm': 1.},
        force_path_group=force_path_group)
    reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    ts = reader.read(*test_loc)
    if version == 'v201706': # this version is empty
        assert ts.dropna(how='all').empty
    else:
        assert not ts.dropna(how='all').empty
    print(ts)

def test_merra2_ts_reader():
    force_path_group = '__test'
    reader = GeoMerra2Ts(dataset_or_path=('MERRA2', 'core'),
                         ioclass_kws={'read_bulk': True},
                         parameters=['SFMC'], scale_factors={'SFMC': 100.},
                         force_path_group=force_path_group)
    ts = reader.read(*test_loc)
    assert not ts.dropna(how='all').empty
    #print(ts)

def test_era5_land_ts_reader():
    force_path_group = '__test'
    reader = GeoEra5LandTs(group_vars={'testdata': ['swvl1', 'stl1']},
                           ioclass_kws={'read_bulk': True}, scale_factors={'swvl1': 1.},
                           force_path_group=force_path_group)
    reader = SelfMaskingAdapter(reader, '>=', 273.15, 'stl1')
    ts = reader.read(*test_loc)
    assert not ts.dropna(how='all').empty
    #print(ts)


def test_era5_ts_reader():
    force_path_group = '__test'
    reader = GeoEra5Ts(dataset_or_path=('ERA5', 'core'),
                       ioclass_kws={'read_bulk': True},
                       parameters=['swvl1', 'stl1'], scale_factors={'swvl1': 100.},
                       force_path_group=force_path_group)
    reader = SelfMaskingAdapter(reader, '>=', 273.15, 'stl1')
    ts = reader.read(*test_loc)
    assert not ts.dropna(how='all').empty
    # print(ts)

def test_gldas21_ts_reader():
    force_path_group = '__test'
    reader = GeoGLDAS21Ts(dataset_or_path=('GLDAS21', 'core'),
                          ioclass_kws={'read_bulk': True},
                          parameters=['SoilMoi0_10cm_inst', 'SoilTMP0_10cm_inst'],
                          scale_factors={'SoilMoi0_10cm_inst': 0.01},
                          force_path_group=force_path_group)
    reader = SelfMaskingAdapter(reader, '>=', 273.15, 'SoilTMP0_10cm_inst')
    ts = reader.read(*test_loc)
    assert not ts.dropna(how='all').empty
    #print(ts)

def test_ismn_good_sm_ts_reader_masking():
    reader = GeoISMNTs(('ISMN', 'v20191211'), network=['COSMOS'],
                       force_path_group='__test', scale_factors=None)
    reader.rebuild_metadata()
    mreader = SelfMaskingAdapter(reader, '==', 'G', 'soil_moisture_flag')

    nearest_station = reader.find_nearest_station(-155.5, 19.9)
    assert nearest_station.name == 'SilverSword'
    ids = reader.get_dataset_ids('soil_moisture', min_depth=0, max_depth=0.17)
    ts = mreader.read(ids[0]) # read and mask
    assert np.all(ts['soil_moisture_flag'] == 'G')
    df_drop = ts['soil_moisture'].dropna()
    assert not df_drop.empty

def test_ismn_good_sm_ts_reader_no_masking():

    reader = GeoISMNTs(('ISMN', 'v20191211'), network=['COSMOS'],
                       force_path_group='__test', scale_factors=None)
    nearest = reader.find_nearest_station(-155.5, 19.9)

    # todO: here the mask adapter cannot be applied because if expect fct read_ts..
    dat, station, dist = reader.read_nearest_station(
        lon=nearest.metadata['longitude'].val,
        lat=nearest.metadata['latitude'].val,
        variable='soil_moisture',
        only_good=True,
        return_flags=True,
        depth=(0, 0.2))

    sm_g = dat['soil_moisture 0.0 to 0.17 [m]']
    flag_g = dat['soil_moisture_flag 0.0 to 0.17 [m]']
    assert np.all(flag_g.values == 'G')

    also_sm = reader.read_ts(0)
    also_g_sm = also_sm.loc[also_sm['soil_moisture_flag'] == 'G']['soil_moisture']
    also_g_flag = also_sm.loc[also_sm['soil_moisture_flag'] == 'G']['soil_moisture_flag']
    assert np.all(also_g_flag.values == 'G')
    assert np.all(sm_g.values == also_g_sm.values)

    assert not dat.dropna().empty

if __name__ == '__main__':
    test_read_applied()

    test_C3S_single_readers('v201706', GeoC3Sv201706Ts)
    test_C3S_single_readers('v202012', GeoC3Sv202012Ts)
    test_C3S_single_readers('v201912', GeoC3Sv201912Ts)
    test_C3S_single_readers('v201812', GeoC3Sv201812Ts)

    test_cci_reader('v061', GeoCCISMv6Ts)
    test_cci_reader('v052', GeoCCISMv5Ts)
    test_cci_reader('v045', GeoCCISMv4Ts)
    test_cci_v033_reader()

    test_era5_reader()
    test_era5land_reader()
    test_C3S201706_single_readers()
    test_C3S201812_single_readers()
    test_merra2_ts_reader()
    test_era5_land_ts_reader()
    test_era5_ts_reader()
    test_gldas21_ts_reader()
    test_ismn_good_sm_ts_reader_masking()
    test_ismn_good_sm_ts_reader_no_masking()

    test_smosic_reader()
    test_smap_spl3_v5_reader()







