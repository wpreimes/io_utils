# -*- coding: utf-8 -*-
from io_utils.grid.grid_functions import read_cells_for_continent
from io_utils.grid.grid_shp_adapter import CountryShpReader, GridShpAdapter
from smecv_grid.grid import SMECV_Grid_v052
import os
import io_utils.root_path as root_path

def test_shp_reader():
    reader = CountryShpReader()

    counts = reader.continent_countries('Europe', 'Asia')
    assert 'China' in counts
    assert 'Austria' in counts

    ids_at_de = reader.country_ids('Austria', 'Germany')
    assert ids_at_de == [113, 120]

    poly_at = reader._geom(113)
    assert poly_at is not None

def test_subgrid_country_cont_names():
    full_grid = SMECV_Grid_v052('land')
    adp = GridShpAdapter(full_grid)
    sgrid = adp.create_subgrid(names=['Austria', 'Seven seas (open ocean)'], verbose=False)

    gpis, lons, lats, cells = sgrid.get_grid_points()
    assert 795661 in gpis
    assert sgrid.gpi2lonlat(795661) == (15.375, 48.125)

    assert 232835 in gpis
    assert sgrid.gpi2lonlat(232835) == (68.875, -49.625)

def test_cells_for_continent():
    grid = SMECV_Grid_v052(None)
    adp = GridShpAdapter(grid)

    cells = adp.create_cells_for_continents(['Seven seas (open ocean)'], out_file=None)
    assert 1808 in cells['Seven seas (open ocean)']

def test_read_cells_for_continents():
    infile = os.path.join(root_path.src_root, 'grid', 'continents_grid_cells',
                          'SMECV_v052_land_cells')

    cells = read_cells_for_continent(['Europe', 'Oceania'], infile)

    assert 1468 in cells # for europe
    assert 1250 in cells # for europe

    assert 2244 in cells # for oceania
    assert 2463 in cells # for oceania

if __name__ == '__main__':
    test_cells_for_continent()
    test_read_cells_for_continents()
    test_shp_reader()
    test_subgrid_country_cont_names()
