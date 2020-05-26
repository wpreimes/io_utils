# -*- coding: utf-8 -*-

"""
Test the readers for which there is test data in this package
"""
from io_utils.read.geo_ts_readers import *

test_loc = (-155.875, 19.625)

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
                          exact_index=True,
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
                          exact_index=True,
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
                          exact_index=True,
                          ioclass_kws={'read_bulk': True},
                          parameters=['sm', 'sm_uncertainty', 't0'],
                          scale_factors={'sm': 1.},
                          force_path_group=force_path_group)
    #reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    cell_data = reader.read_cells([165,166]) # all empty
    ts = reader.read(633697)
    # TODO: times are wrong
    assert not ts.empty



def test_cci_v045_reader():
    vers = 'v045'
    force_path_group = '__test'
    ## == active
    reader = GeoCCISMv4Ts(dataset_or_path=('ESA_CCI_SM', vers, 'ACTIVE'),
                          exact_index=True,
                          ioclass_kws={'read_bulk': True},
                          parameters=['sm', 'sm_uncertainty', 't0'],
                          scale_factors={'sm': 1.},
                          force_path_group=force_path_group)
    #reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    cell_data = reader.read_cells([165,166]) # not all enoty
    for gpi, data in cell_data.items():
        assert data.empty # all empty
    ts = reader.read(*test_loc)
    assert ts.empty

    ## == combined
    reader = GeoCCISMv4Ts(dataset_or_path=('ESA_CCI_SM', vers, 'COMBINED'),
                          exact_index=True,
                          ioclass_kws={'read_bulk': True},
                          parameters=['sm', 'sm_uncertainty', 't0'],
                          scale_factors={'sm': 1.},
                          force_path_group=force_path_group)
    #reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    cell_data = reader.read_cells([165,166]) # not all enoty
    ts = reader.read(633697)
    assert not ts.empty

    ## == passive
    reader = GeoCCISMv4Ts(dataset_or_path=('ESA_CCI_SM', vers, 'PASSIVE'),
                          exact_index=True,
                          ioclass_kws={'read_bulk': True},
                          parameters=['sm', 'sm_uncertainty', 't0'],
                          scale_factors={'sm': 1.},
                          force_path_group=force_path_group)
    #reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    cell_data = reader.read_cells([165,166]) # all empty
    for gpi, data in cell_data.items():
        assert data.empty # all empty
    ts = reader.read(*test_loc)
    assert ts.empty

def test_cci_v044_reader():
    vers = 'v044'
    force_path_group = '__test'

    ## == active
    reader = GeoCCISMv4Ts(dataset_or_path=('ESA_CCI_SM', vers, 'ACTIVE'),
                          exact_index=True,
                          ioclass_kws={'read_bulk': True},
                          parameters=['sm', 'sm_uncertainty', 't0'],
                          scale_factors={'sm': 1.},
                          force_path_group=force_path_group)
    #reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    cell_data = reader.read_cells([165,166]) # all empty
    for gpi, data in cell_data.items():
        assert data.empty # all empty
    ts = reader.read(*test_loc)
    assert ts.empty

    ## == combined
    reader = GeoCCISMv4Ts(dataset_or_path=('ESA_CCI_SM', vers, 'COMBINED'),
                          exact_index=True,
                          ioclass_kws={'read_bulk': True},
                          parameters=['sm', 'sm_uncertainty', 't0'],
                          scale_factors={'sm': 1.},
                          force_path_group=force_path_group)
    #reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    cell_data = reader.read_cells([165,166]) # all empty
    ts = reader.read(633697)
    assert not ts.empty

    ## == passive
    reader = GeoCCISMv4Ts(dataset_or_path=('ESA_CCI_SM', vers, 'PASSIVE'),
                          exact_index=True,
                          ioclass_kws={'read_bulk': True},
                          parameters=['sm', 'sm_uncertainty', 't0'],
                          scale_factors={'sm': 1.},
                          force_path_group=force_path_group)
    #reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    cell_data = reader.read_cells([165,166]) # all empty
    for gpi, data in cell_data.items():
        assert data.empty # all empty
    ts = reader.read(*test_loc)
    assert ts.empty

def test_cci_v047_reader():
    vers = 'v047'
    force_path_group = '__test'

    ## == active
    reader = GeoCCISMv4Ts(dataset_or_path=('ESA_CCI_SM', vers, 'ACTIVE'),
                          exact_index=True,
                          ioclass_kws={'read_bulk': True},
                          parameters=['sm', 'sm_uncertainty', 't0'],
                          scale_factors={'sm': 1.},
                          force_path_group=force_path_group)
    #reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    cell_data = reader.read_cells([165,166]) # all empty
    for gpi, data in cell_data.items():
        assert data.empty # all empty
    ts = reader.read(*test_loc)
    assert ts.empty

    ## == combined
    reader = GeoCCISMv4Ts(dataset_or_path=('ESA_CCI_SM', vers, 'COMBINED'),
                          exact_index=True,
                          ioclass_kws={'read_bulk': True},
                          parameters=['sm', 'sm_uncertainty', 't0'],
                          scale_factors={'sm': 1.},
                          force_path_group=force_path_group)
    #reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    cell_data = reader.read_cells([165,166]) # all empty
    ts = reader.read(633697)
    assert not ts.empty

    ## == passive
    reader = GeoCCISMv4Ts(dataset_or_path=('ESA_CCI_SM', vers, 'PASSIVE'),
                          exact_index=True,
                          ioclass_kws={'read_bulk': True},
                          parameters=['sm', 'sm_uncertainty', 't0'],
                          scale_factors={'sm': 1.},
                          force_path_group=force_path_group)
    #reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    cell_data = reader.read_cells([165,166]) # all empty
    for gpi, data in cell_data.items():
        assert data.empty # all empty
    ts = reader.read(*test_loc)
    assert ts.empty

def test_cci_v052_reader():
    vers = 'v052'
    force_path_group = '__test'

    ## == active
    reader = GeoCCISMv5Ts(dataset_or_path=('ESA_CCI_SM', vers, 'ACTIVE'),
                          exact_index=True,
                          ioclass_kws={'read_bulk': True},
                          parameters=['sm', 'sm_uncertainty', 't0'],
                          scale_factors={'sm': 1.},
                          force_path_group=force_path_group)
    #reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    cell_data = reader.read_cells([165,166]) # all empty
    for gpi, data in cell_data.items():
        assert data.empty # all empty
    ts = reader.read(*test_loc)
    assert ts.empty

    ## == combined
    reader = GeoCCISMv5Ts(dataset_or_path=('ESA_CCI_SM', vers, 'COMBINED'),
                          exact_index=True,
                          ioclass_kws={'read_bulk': True},
                          parameters=['sm', 'sm_uncertainty', 't0'],
                          scale_factors={'sm': 1.},
                          force_path_group=force_path_group)
    #reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    cell_data = reader.read_cells([165,166])
    ts = reader.read(633697)
    assert not ts.empty

    ## == passive
    reader = GeoCCISMv5Ts(dataset_or_path=('ESA_CCI_SM', vers, 'PASSIVE'),
                          exact_index=True,
                          ioclass_kws={'read_bulk': True},
                          parameters=['sm', 'sm_uncertainty', 't0'],
                          scale_factors={'sm': 1.},
                          force_path_group=force_path_group)
    #reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    cell_data = reader.read_cells([165,166]) # all empty
    for gpi, data in cell_data.items():
        assert data.empty # all empty
    ts = reader.read(*test_loc)
    assert ts.empty


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
    reader = GeoEra5LandTs(group_vars={'sm_precip_lai': ['swvl1']},
                           ioclass_kws={'read_bulk': True}, scale_factors={'swvl1': 1.})
    ts = reader.read(*test_loc)
    assert not ts.dropna(how='all').empty
    #print(ts)

def test_C3S201706_single_readers():
    force_path_group = '__test'
    for record in ['TCDR', 'ICDR']:
        dataset = 'ACTIVE'
        reader = GeoC3Sv201706Ts(dataset_or_path=('C3S', 'v201706', dataset, 'DAILY', record),
            grid_path=None, ioclass_kws={'read_bulk': True},
            parameters=['sm', 'sm_uncertainty', 'flag'], scale_factors={'sm': 1.},
            force_path_group=force_path_group)
        ts = reader.read(*test_loc)
        assert not ts.dropna(how='all').empty

        dataset = 'COMBINED'
        reader = GeoC3Sv201706Ts(dataset_or_path=('C3S', 'v201706', dataset, 'DAILY', record),
            grid_path=None, ioclass_kws={'read_bulk': True},
            parameters=['sm', 'sm_uncertainty', 'flag'], scale_factors={'sm': 1.},
            force_path_group=force_path_group)
        ts = reader.read(*test_loc)
        assert not ts.dropna(how='all').empty

        dataset = 'PASSIVE'
        reader = GeoC3Sv201706Ts(dataset_or_path=('C3S', 'v201706', dataset, 'DAILY', record),
            grid_path=None, ioclass_kws={'read_bulk': True},
            parameters=['sm', 'sm_uncertainty', 'flag'], scale_factors={'sm': 1.},
            force_path_group=force_path_group)
        ts = reader.read(*test_loc)
        assert not ts.dropna(how='all').empty
        #print(ts)

def test_C3S201812_single_readers():
    force_path_group = '__test'
    reader = GeoC3Sv201812Ts(dataset_or_path=('C3S', 'v201812', 'ACTIVE', 'DAILY', 'TCDR'),
        grid_path=None, ioclass_kws={'read_bulk': True},
        parameters=['sm', 'sm_uncertainty', 'flag'], scale_factors={'sm': 1.},
        force_path_group=force_path_group)
    reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    ts = reader.read(*test_loc)
    assert not ts.dropna(how='all').empty
    #print(ts)

    reader = GeoC3Sv201812Ts(dataset_or_path=('C3S', 'v201812', 'COMBINED', 'DAILY', 'TCDR'),
        grid_path=None, ioclass_kws={'read_bulk': True},
        parameters=['sm', 'sm_uncertainty', 'flag'], scale_factors={'sm': 1.},
        force_path_group=force_path_group)
    reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    ts = reader.read(*test_loc)
    assert not ts.dropna(how='all').empty
    #print(ts)

    # no data for the passive c3s there
    reader = GeoC3Sv201812Ts(dataset_or_path=('C3S', 'v201812', 'PASSIVE', 'DAILY', 'TCDR'),
        grid_path=None, ioclass_kws={'read_bulk': True},
        parameters=['sm', 'sm_uncertainty', 'flag'], scale_factors={'sm': 1.},
        force_path_group=force_path_group)
    reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    ts = reader.read(*test_loc)
    assert ts.empty # ATTENTION: passive data is empty here
    #print(ts)

def test_C3S201912_single_readers():
    force_path_group = '__test'

    reader = GeoC3Sv201912Ts(dataset_or_path=('C3S', 'v201912', 'COMBINED', 'DAILY', 'TCDR'),
        grid_path=None, ioclass_kws={'read_bulk': True},
        parameters=['sm', 'sm_uncertainty', 'flag'], scale_factors={'sm': 1.},
        force_path_group=force_path_group)
    reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    ts = reader.read(*test_loc)
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
                       parameters=('soil moisture', 'flag'),
                       force_path_group='__test', scale_factors=None)
    reader.reset_python_metadata()
    mreader = SelfMaskingAdapter(reader, '==', 'G', 'soil moisture_flag')

    nearest = reader.find_nearest_station(-155.5, 19.9)
    assert nearest.station == 'SilverSword'
    ids = reader.get_dataset_ids('soil moisture', min_depth=0, max_depth=0.17)
    ts = mreader.read(ids[0]) # read and mask
    assert np.all(ts['soil moisture_flag'] == 'G')
    df_drop = ts['soil moisture'].dropna()
    assert not df_drop.empty

def test_ismn_good_sm_ts_reader_no_masking():

    reader = GeoISMNTs(('ISMN', 'v20191211'), network=['COSMOS'],
                       parameters=('soil moisture'),
                       force_path_group='__test', scale_factors=None)
    nearest = reader.find_nearest_station(-155.5, 19.9)

    # todO: here the mask adapter cannot be applied because if expect fct read_ts..
    dat, station, dist = reader.read_sm_nearest_station(
        lon=nearest.longitude, lat=nearest.latitude, min_depth=0, max_depth=0.2)
    sm = dat['soil moisture', 'COSMOS', 'SilverSword', 0.0, 0.17,
            'Cosmic-ray-Probe'].loc[
             dat['soil moisture_flag', 'COSMOS', 'SilverSword', 0.0, 0.17,
                 'Cosmic-ray-Probe'].isin(['G'])]

    also_sm = station.read_variable('soil moisture').data
    also_sm = also_sm['soil moisture'].loc[also_sm['soil moisture_flag'].isin(['G'])]

    assert np.all(sm.values == also_sm.values)
    assert not dat.dropna().empty


if __name__ == '__main__':
    test_smap_spl3_v5_reader()


    test_ismn_good_sm_ts_reader_masking()
    test_ismn_good_sm_ts_reader_no_masking()

    test_smosic_reader()
    test_era5_land_ts_reader()
    test_era5_ts_reader()

    test_cci_v033_reader()
    test_cci_v044_reader()
    test_cci_v045_reader()
    test_cci_v052_reader()

    test_merra2_ts_reader()

    test_C3S201706_single_readers()
    test_C3S201812_single_readers()
    test_C3S201912_single_readers()

    test_gldas21_ts_reader()

    test_era5_reader()


