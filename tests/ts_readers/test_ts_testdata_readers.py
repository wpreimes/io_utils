# -*- coding: utf-8 -*-

"""
Test the readers for which there is test data in this package
"""
from io_utils.read.geo_ts_readers import *

test_loc = (-155.875, 19.625)

def test_smosic_reader():
    force_path_group = '_test'
    smos_reader = GeoSMOSICTs(dataset=('SMOS', 'IC', 'ASC'),
                              ioclass_kws={'read_bulk': True},
                              parameters=['Soil_Moisture', 'Quality_Flag'],
                              scale_factors={'sm': 1.},
                              force_path_group=force_path_group)
    celldata = smos_reader.read_cells([165,166])
    assert any([not data.empty for gpi, data in celldata.items()])
    smos_reader = SelfMaskingAdapter(smos_reader, '==', 0, 'Quality_Flag')
    ts = smos_reader.read(*test_loc)
    assert not ts.empty

def test_smap_spl3_reader():
    force_path_group = '_test'
    smap_reader = GeoSMAPTs(dataset=('SMAP', 'SP3SMPv5', 'ASC'),
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
    force_path_group = '_test'

    ## == active
    reader = GeoCCISMv3Ts(dataset=('ESA_CCI_SM', vers, 'ACTIVE'),
                          exact_index=True,
                          ioclass_kws={'read_bulk': True},
                          parameters=['sm', 'sm_uncertainty', 'flag', 't0'],
                          scale_factors={'sm': 1.},
                          force_path_group=force_path_group)
    #reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    cell_data = reader.read_cells([165,166]) # all empty
    ts = reader.read(633697)
    # TODO: times are wrong
    assert not ts.empty

    ## == combined
    reader = GeoCCISMv3Ts(dataset=('ESA_CCI_SM', vers, 'COMBINED'),
                          exact_index=True,
                          ioclass_kws={'read_bulk': True},
                          parameters=['sm', 'sm_uncertainty', 'flag', 't0'],
                          scale_factors={'sm': 1.},
                          force_path_group=force_path_group)
    #reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    cell_data = reader.read_cells([165,166]) # all empty
    ts = reader.read(633697)
    # TODO: times are wrong
    assert not ts.empty

    ## == passive
    reader = GeoCCISMv3Ts(dataset=('ESA_CCI_SM', vers, 'PASSIVE'),
                          exact_index=True,
                          ioclass_kws={'read_bulk': True},
                          parameters=['sm', 'sm_uncertainty', 'flag', 't0'],
                          scale_factors={'sm': 1.},
                          force_path_group=force_path_group)
    #reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    cell_data = reader.read_cells([165,166]) # all empty
    ts = reader.read(633697)
    # TODO: times are wrong
    assert not ts.empty



def test_cci_v045_reader():
    vers = 'v045'
    force_path_group = '_test'
    ## == active
    reader = GeoCCISMv4Ts(dataset=('ESA_CCI_SM', vers, 'ACTIVE'),
                          exact_index=True,
                          ioclass_kws={'read_bulk': True},
                          parameters=['sm', 'sm_uncertainty', 'flag', 't0'],
                          scale_factors={'sm': 1.},
                          force_path_group=force_path_group)
    #reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    cell_data = reader.read_cells([165,166]) # not all enoty
    for gpi, data in cell_data.items():
        assert data.empty # all empty
    ts = reader.read(*test_loc)
    assert ts.empty

    ## == combined
    reader = GeoCCISMv4Ts(dataset=('ESA_CCI_SM', vers, 'COMBINED'),
                          exact_index=True,
                          ioclass_kws={'read_bulk': True},
                          parameters=['sm', 'sm_uncertainty', 'flag', 't0'],
                          scale_factors={'sm': 1.},
                          force_path_group=force_path_group)
    #reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    cell_data = reader.read_cells([165,166]) # not all enoty
    ts = reader.read(633697)
    assert not ts.empty

    ## == passive
    reader = GeoCCISMv4Ts(dataset=('ESA_CCI_SM', vers, 'PASSIVE'),
                          exact_index=True,
                          ioclass_kws={'read_bulk': True},
                          parameters=['sm', 'sm_uncertainty', 'flag', 't0'],
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
    force_path_group = '_test'

    ## == active
    reader = GeoCCISMv4Ts(dataset=('ESA_CCI_SM', vers, 'ACTIVE'),
                          exact_index=True,
                          ioclass_kws={'read_bulk': True},
                          parameters=['sm', 'sm_uncertainty', 'flag', 't0'],
                          scale_factors={'sm': 1.},
                          force_path_group=force_path_group)
    #reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    cell_data = reader.read_cells([165,166]) # all empty
    for gpi, data in cell_data.items():
        assert data.empty # all empty
    ts = reader.read(*test_loc)
    assert ts.empty

    ## == combined
    reader = GeoCCISMv4Ts(dataset=('ESA_CCI_SM', vers, 'COMBINED'),
                          exact_index=True,
                          ioclass_kws={'read_bulk': True},
                          parameters=['sm', 'sm_uncertainty', 'flag', 't0'],
                          scale_factors={'sm': 1.},
                          force_path_group=force_path_group)
    #reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    cell_data = reader.read_cells([165,166]) # all empty
    ts = reader.read(633697)
    assert not ts.empty

    ## == passive
    reader = GeoCCISMv4Ts(dataset=('ESA_CCI_SM', vers, 'PASSIVE'),
                          exact_index=True,
                          ioclass_kws={'read_bulk': True},
                          parameters=['sm', 'sm_uncertainty', 'flag', 't0'],
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
    force_path_group = '_test'

    ## == active
    reader = GeoCCISMv4Ts(dataset=('ESA_CCI_SM', vers, 'ACTIVE'),
                          exact_index=True,
                          ioclass_kws={'read_bulk': True},
                          parameters=['sm', 'sm_uncertainty', 'flag', 't0'],
                          scale_factors={'sm': 1.},
                          force_path_group=force_path_group)
    #reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    cell_data = reader.read_cells([165,166]) # all empty
    for gpi, data in cell_data.items():
        assert data.empty # all empty
    ts = reader.read(*test_loc)
    assert ts.empty

    ## == combined
    reader = GeoCCISMv4Ts(dataset=('ESA_CCI_SM', vers, 'COMBINED'),
                          exact_index=True,
                          ioclass_kws={'read_bulk': True},
                          parameters=['sm', 'sm_uncertainty', 'flag', 't0'],
                          scale_factors={'sm': 1.},
                          force_path_group=force_path_group)
    #reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    cell_data = reader.read_cells([165,166]) # all empty
    ts = reader.read(633697)
    assert not ts.empty

    ## == passive
    reader = GeoCCISMv4Ts(dataset=('ESA_CCI_SM', vers, 'PASSIVE'),
                          exact_index=True,
                          ioclass_kws={'read_bulk': True},
                          parameters=['sm', 'sm_uncertainty', 'flag', 't0'],
                          scale_factors={'sm': 1.},
                          force_path_group=force_path_group)
    #reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    cell_data = reader.read_cells([165,166]) # all empty
    for gpi, data in cell_data.items():
        assert data.empty # all empty
    ts = reader.read(*test_loc)
    assert ts.empty

def test_era5_reader():
    force_path_group = '_test'
    reader = GeoEra5Ts(dataset=('ERA5', 'core'),
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
    force_path_group = '_test'
    for record in ['TCDR', 'ICDR']:
        dataset = 'ACTIVE'
        reader = GeoC3Sv201706Ts(dataset=('C3S', 'v201706', dataset, record),
            grid_path=None, ioclass_kws={'read_bulk': True},
            parameters=['sm', 'sm_uncertainty', 'flag'], scale_factors={'sm': 1.},
            force_path_group=force_path_group)
        ts = reader.read(*test_loc)
        assert not ts.dropna(how='all').empty

        dataset = 'COMBINED'
        reader = GeoC3Sv201706Ts(dataset=('C3S', 'v201706', dataset, record),
            grid_path=None, ioclass_kws={'read_bulk': True},
            parameters=['sm', 'sm_uncertainty', 'flag'], scale_factors={'sm': 1.},
            force_path_group=force_path_group)
        ts = reader.read(*test_loc)
        assert not ts.dropna(how='all').empty

        dataset = 'PASSIVE'
        reader = GeoC3Sv201706Ts(dataset=('C3S', 'v201706', dataset, record),
            grid_path=None, ioclass_kws={'read_bulk': True},
            parameters=['sm', 'sm_uncertainty', 'flag'], scale_factors={'sm': 1.},
            force_path_group=force_path_group)
        ts = reader.read(*test_loc)
        assert not ts.dropna(how='all').empty
        #print(ts)

def test_C3S201812_single_readers():
    force_path_group = '_test'
    reader = GeoC3Sv201812Ts(dataset=('C3S', 'v201812', 'ACTIVE', 'TCDR'),
        grid_path=None, ioclass_kws={'read_bulk': True},
        parameters=['sm', 'sm_uncertainty', 'flag'], scale_factors={'sm': 1.},
        force_path_group=force_path_group)
    reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    ts = reader.read(*test_loc)
    assert not ts.dropna(how='all').empty
    #print(ts)

    reader = GeoC3Sv201812Ts(dataset=('C3S', 'v201812', 'COMBINED', 'TCDR'),
        grid_path=None, ioclass_kws={'read_bulk': True},
        parameters=['sm', 'sm_uncertainty', 'flag'], scale_factors={'sm': 1.},
        force_path_group=force_path_group)
    reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    ts = reader.read(*test_loc)
    assert not ts.dropna(how='all').empty
    #print(ts)

    # no data for the passive c3s there
    reader = GeoC3Sv201812Ts(dataset=('C3S', 'v201812', 'PASSIVE', 'TCDR'),
        grid_path=None, ioclass_kws={'read_bulk': True},
        parameters=['sm', 'sm_uncertainty', 'flag'], scale_factors={'sm': 1.},
        force_path_group=force_path_group)
    reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
    ts = reader.read(*test_loc)
    assert ts.empty # ATTENTION: passive data is empty here
    #print(ts)

def test_gldas20_ts_reader():
    force_path_group = '_test'
    reader = GeoGLDAS20Ts(dataset=('GLDAS20', 'core'),
                          ioclass_kws={'read_bulk': True},
                          parameters=['SoilMoi0_10cm_inst'], scale_factors=None,
                          force_path_group=force_path_group)
    ts = reader.read(*test_loc)
    assert not ts.dropna(how='all').empty
    #print(ts)

def test_merra2_ts_reader():
    force_path_group = '_test'
    reader = GeoMerra2Ts(dataset=('MERRA2', 'core'),
                         ioclass_kws={'read_bulk': True},
                         parameters=['SFMC'], scale_factors={'SFMC': 100.},
                         force_path_group=force_path_group)
    ts = reader.read(*test_loc)
    assert not ts.dropna(how='all').empty
    #print(ts)

def test_era5_land_ts_reader():
    force_path_group = '_test'
    reader = GeoEra5LandTs(group_vars={'testdata': ['swvl1', 'stl1']},
                           ioclass_kws={'read_bulk': True}, scale_factors={'swvl1': 1.},
                           force_path_group=force_path_group)
    reader = SelfMaskingAdapter(reader, '>=', 273.15, 'stl1')
    ts = reader.read(*test_loc)
    assert not ts.dropna(how='all').empty
    #print(ts)


def test_era5_ts_reader():
    force_path_group = '_test'
    reader = GeoEra5Ts(dataset=('ERA5', 'testdata'),
                       ioclass_kws={'read_bulk': True},
                       parameters=['swvl1', 'stl1'], scale_factors={'swvl1': 100.},
                       force_path_group=force_path_group)
    reader = SelfMaskingAdapter(reader, '>=', 273.15, 'stl1')
    ts = reader.read(*test_loc)
    assert not ts.dropna(how='all').empty
    # print(ts)

def test_gldas21_ts_reader():
    force_path_group = '_test'
    reader = GeoGLDAS21Ts(dataset=('GLDAS21', 'testdata'),
                          ioclass_kws={'read_bulk': True},
                          parameters=['SoilMoi0_10cm_inst', 'SoilTMP0_10cm_inst'],
                          scale_factors={'SoilMoi0_10cm_inst': 0.01},
                          force_path_group=force_path_group)
    reader = SelfMaskingAdapter(reader, '>=', 273.15, 'SoilTMP0_10cm_inst')
    ts = reader.read(*test_loc)
    assert not ts.dropna(how='all').empty
    #print(ts)

if __name__ == '__main__':
    test_smap_spl3_reader()
    # test_smosic_reader()
    # test_gldas21_ts_reader()
    # test_era5_land_ts_reader()
    # test_era5_ts_reader()
    #
    # test_cci_v033_reader()
    # test_cci_v044_reader()
    # test_cci_v045_reader()
    #
    # test_merra2_ts_reader()
    #
    # test_C3S201706_single_readers()
    #
    # test_C3S201812_single_readers()
    #
    # test_gldas21_ts_reader()
    # test_gldas20_ts_reader()
    #
    # test_era5_reader()


