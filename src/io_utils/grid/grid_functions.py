# -*- coding: utf-8 -*-

import functools

import numpy as np
import os
import ast

import pygeogrids as pgg
from pygeogrids.netcdf import load_grid
from smecv_grid.grid import SMECV_Grid_v052
from io_utils.grid.grid_shp_adapter import GridShpAdapter

'''
Contains functions to process subsets of grid points. Works only for QDEG grid atm.
Should be extended to work with any grid (subsets from latitude/longitudes) instead of GPIs.
'''

def fract_grid(grid):
    """
    Fractionise grid into parts to reconstuct a similar grid.
    E.g. to subsequently turn a land grid into a global grid.

    Parameters
    ----------
    grid : pygeogrids.BasicGrid

    Returns
    -------
    dx : float
        minimum resolution in lon direction
    dy : float
        minimum resolution in lat direction
    lons : np.array
        Unique longitudes in the grid
    lats : np.array
        Unique latitudes in the grid
    """

    gpis, lons, lats, _ = grid.get_grid_points()
    lons, lats = sorted(np.unique(lons)), sorted(np.unique(lats))

    dx = np.around(np.min(np.diff(lons)), 10)
    dy = np.around(np.min(np.diff(lats)), 10)

    return dx, dy, lons, lats

smecv52_5deg_cells = os.path.join(os.path.dirname(__file__), 'continents_grid_cells',
                                  'SMECV_v052_land_cells')

def read_cells_for_continent(continent, infile=smecv52_5deg_cells):
    """
    Read cells for passed continent(s) from a created text file.

    Parameters
    ----------
    continent : str or list
        One or multiple continents to read cells for.
    infile: str, optional (default: CCI v5.2 5 deg cells)
        Path to file to read

    Returns
    -------
    ret_cells : list
        Cells for the selected continent(s)
    """
    if isinstance(continent, str):
        continent = [continent]

    with open(infile, 'r') as f:
        s = f.read()
        cont_cells = ast.literal_eval(s)

    if len(continent) > 0:
        ret_cells = []
        for k in continent:
            if k not in cont_cells.keys():
                raise ValueError('{} not found in list, choose one of: {}'.format(
                    k, ', '.join(cont_cells.keys())))
            else:
                ret_cells += cont_cells[k]
    else:
        ret_cells = None

    return ret_cells

def grid_points_for_cells(areas_or_cells):
    '''
    Load the grid points on the grid for the passed area or cells

    Parameters
    ----------
    areas_or_cells : list
        List of names of continents or countries as in continents_cells.txt
        or list of cell numbers.

    Returns
    -------
    grid_points : np.array
        List of grid points in the passed cells or in the cells for the passed
        area(s)
    '''
    grid = SMECV_Grid_v052()

    grid_points = []

    if isinstance(areas_or_cells, str):
        areas_or_cells = [areas_or_cells]

    for area in areas_or_cells:
        if isinstance(area, str):
            cells = read_cells_for_continent(area)
        else:
            cells = area

        grid_points += np.ndarray.tolist(grid.grid_points_for_cell(cells)[0])
    return np.array(grid_points)

def cells_for_identifier(names, grid=SMECV_Grid_v052()):
    '''
    Return cell numbers for the passed areas (or cells)

    Parameters
    ----------
    areas_or_cells : str or list
        List of cells (trivial case), list of area names or 'global'
        Implemented areas:

    Returns
    -------
    cells: np.array
        List of cells on the selected grid
    '''
    if isinstance(names, str):
        if names.lower() == 'global':
            return grid.get_cells().tolist()
        else:
            names = [names]
    adp = GridShpAdapter(grid)
    return adp.create_subgrid(names)

def intersect_grids(grids, out_path=None):
    """
    Get a grid from common GPIs of a list of grids.

    Parameters
    ----------
    grids_paths : list
        Either a list of grid object or of paths to grids files to load.
    out_path : str, optional (default: None)
        Path where the intersected grid is stored. If None is passed, the grid
        is not stored.

    Returns
    -------
    common_grid : pgg.CellGrid
        A grid only with GPIs that were in all passed grids.
    """
    if all([isinstance(g, str) for g in grids]):
        grids = [load_grid(path) for path in grids]
    grid_points = tuple([grid.get_grid_points()[0] for grid in grids])

    common_gpis = functools.reduce(np.intersect1d, grid_points)
    common_grid = grids[0].subgrid_from_gpis(common_gpis)  #type: pgg.BasicGrid

    if out_path is not None:
        pgg.netcdf.save_grid(os.path.join(out_path, 'common_grid.nc'), common_grid,
                             subset_name='common_adjusted',
                             subset_meaning='LMP HOM QCM common adjusted points')
    return common_grid


def filter_grid(input_grid, filter_grid):
    """
    Filter a grid with points from other grid, so that points from filter_grid
    are excluded.
    Grids must have the same resolution.

    Parameters
    -------
    input_grid : pygeogrids.grids.CellGrid
        Grid that will be filtered
    filter_grid : pygeogrids.grids.CellGrid
        Grid that is used to filter points from input_grid

    Returns
    -------
    filtered_grid : pygeogrids.grids.CellGrid
        Input_grid that was filtered to exclude filter_grid
    """
    input_gpis = input_grid.get_grid_points()[0]
    filter_gpis = filter_grid.get_grid_points()[0]

    gpi_not_forest_mask = ~np.isin(input_gpis, filter_gpis)

    filtered_input_gpis = input_gpis[np.where(gpi_not_forest_mask)]
    filtered_input_grid = input_grid.subgrid_from_gpis(filtered_input_gpis)

    # keep the shape information
    filtered_input_grid.shape = input_grid.shape

    return filtered_input_grid