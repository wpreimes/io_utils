# -*- coding: utf-8 -*-
from io_utils.grid.continents_cells import CountryShpReader, subgrid_for_polys
from io_utils.grid.continents_cells import create_cells_for_continents, read_cells_for_continent
from smecv_grid.grid import SMECV_Grid_v042
import os
from io_utils.globals import src_root

def test_shp_reader():
    reader = CountryShpReader()

    counts = reader.continent_countries('Europe', 'Asia')
    assert 'China' in counts
    assert 'Austria' in counts

    ids_at_de = reader.country_ids('Austria', 'Germany')
    assert ids_at_de == [114, 121]

    poly_at = reader._geom(114)
    assert poly_at is not None

def test_subgrid_country_cont_names():
    full_grid = SMECV_Grid_v042('land')
    sgrid = subgrid_for_polys(full_grid, 'Austria', 'Seven seas (open ocean)', silent=True)

    gpis, lons, lats, cells = sgrid.get_grid_points()
    assert 795661 in gpis
    assert sgrid.gpi2lonlat(795661) == (15.375, 48.125)

    assert 232835 in gpis
    assert sgrid.gpi2lonlat(232835) == (68.875, -49.625)

def test_cells_for_continent():
    grid = SMECV_Grid_v042('land')
    cells = create_cells_for_continents(grid, 'Seven seas (open ocean)',
                                        out_file=None)
    assert 1808 in cells['Seven seas (open ocean)']

def test_read_cells_for_continents():
    infile = os.path.join(src_root, 'grid', 'continents_grid_cells', 'SMECV_v052_land_cells')

    cells = read_cells_for_continent(['Europe', 'Oceania'], infile)

    assert 1797 in cells # for europe
    assert 2444 in cells # for europe

    assert 2244 in cells # for oceania
    assert 2463 in cells # for oceania

if __name__ == '__main__':
    test_read_cells_for_continents()
    test_shp_reader()
    test_subgrid_country_cont_names()
    test_cells_for_continent()