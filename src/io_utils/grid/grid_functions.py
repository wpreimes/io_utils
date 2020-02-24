# -*- coding: utf-8 -*-

import functools

import numpy as np
import os

import pygeogrids as pgg
from pygeogrids.netcdf import load_grid
from smecv_grid.grid import SMECV_Grid_v052
from io_utils.grid.continents_cells import read_cells_for_continent

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

    dx, dy = np.min(np.diff(lons)), np.min(np.diff(lats))

    return dx, dy, lons, lats

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

def cells_for_identifier(areas_or_cells, grid=SMECV_Grid_v052()):
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
    if isinstance(areas_or_cells, str):
        if areas_or_cells.lower() == 'global':
            cells = grid.get_cells().tolist()
        else:
            cells = read_cells_for_continent(areas_or_cells)
    elif isinstance(areas_or_cells, list):
        if all((isinstance(i, str) for i in areas_or_cells)):
            cells = read_cells_for_continent(*areas_or_cells)
        else:
            cells = areas_or_cells
    else:
        raise ValueError(areas_or_cells, 'Unexpected input format')

    return np.array(cells)


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


if __name__ == '__main__':
    cells = cells_for_identifier('United_States')
    gpis = grid_points_for_cells(['United_States', 'Australia'])
    print(cells)


def filter_grid(input_grid, filter_grid):
    '''
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
    '''
    input_gpis = input_grid.get_grid_points()[0]
    filter_gpis = filter_grid.get_grid_points()[0]

    gpi_not_forest_mask = ~np.isin(input_gpis, filter_gpis)

    filtered_input_gpis = input_gpis[np.where(gpi_not_forest_mask)]
    filtered_input_grid = input_grid.subgrid_from_gpis(filtered_input_gpis)

    return filtered_input_grid