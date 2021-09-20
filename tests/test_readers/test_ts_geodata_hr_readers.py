# -*- coding: utf-8 -*-

"""
Module description
"""
# TODO:
#   (+) 
#---------
# NOTES:
#   -

import pytest
import io_utils.root_path as root_path
from io_utils.read.geo_ts_readers import *
test_loc = (15, 45)

def print_test_config(dataset, path_group=None):
    ds = dataset
    pg = path_group if path_group is not None else 'storage'
    print('Test reading {} data from {}.'.format(ds, pg))

@pytest.mark.geo_test_data
def test_ascat_direx_reader_reader(verbose=False):
    if verbose: print('Test reading ASCAT Direx from storage.')
    reader = GeoDirexTs(
        dataset_or_path=('ASCAT', 'DIREX', 'v2', 'Senegal'),
        ioclass_kws={'read_bulk': True},
        parameters=['swi_005'],
        scale_factors={'swi_005': 1.})
    ts = reader.read(-17.455902100, 14.731057934)
    assert not ts.empty
    if verbose: print(ts)

@pytest.mark.skipif(not hr_available,
                    reason="Hires Image readers not available")
@pytest.mark.geo_test_data
def test_cgls_ssm_ts_reader(verbose=False):
    reader = GeoCSarSsmTiffReader(dataset_or_path=('CSAR', 'CGLS', 'SSM', '1km', 'V1.1', 'tiff'))
    ts = reader.read(*test_loc)
    if verbose: print(ts)
    assert not ts.dropna(how='all').empty

@pytest.mark.skipif(not hr_available,
                    reason="Hires Image readers not available")
@pytest.mark.geo_test_data
def test_cgls_swi_ts_reader(verbose=False):
    reader = GeoCSarSwiTiffReader(dataset_or_path=('CSAR', 'CGLS', 'SWI', '1km', 'V1.0', 'geotiff'))
    ts = reader.read(*test_loc)
    if verbose: print(ts)
    assert not ts.dropna(how='all').empty

@pytest.mark.skipif(not hr_available,
                    reason="Hires Image readers not available")
@pytest.mark.geo_test_data
def test_scatsar_swi_ts_reader(verbose=False):
    reader = GeoScatSarCglsSwiReader(dataset_or_path=('SCATSAR', 'CGLS', 'C0418', 'E7'))
    ts = reader.read(*test_loc)
    if verbose: print(ts)
    assert not ts.dropna(how='all').empty

if __name__ == '__main__':
    v = True
    test_scatsar_swi_ts_reader(v)
    test_cgls_ssm_ts_reader(v)
    test_cgls_swi_ts_reader(v)
