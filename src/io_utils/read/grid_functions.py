# -*- coding: utf-8 -*-

import ast
import functools

import numpy as np
import os

import pygeogrids as pgg
from pygeogrids.netcdf import load_grid
from smecv_grid.grid import SMECV_Grid_v042


'''
Contains functions to process subsets of grid points. Works only for QDEG grid atm.
Should be extended to work with any grid (subsets from latitude/longitudes) instead of GPIs.
'''


def cells_for_area(*areas):
    '''
    Load cells for the selected continent from the continents_cells.txt file

    Parameters
    ----------
    areas : str
        Names of the continents or countries the cells are loaded for
        eg. Australia, United_States

    Returns
    -------
    cells : list
        List of cells for the selected area(s)

    '''
    from src.io_utils.read.continents_cells import cells_lut
    cells = []

    for area in areas:
        cells += cells_lut[area]
    return cells

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
    grid = SMECV_Grid_v042()

    grid_points = []

    if isinstance(areas_or_cells, str):
        areas_or_cells = [areas_or_cells]

    for area in areas_or_cells:
        if isinstance(area, str):
            cells = cells_for_area(area)
        else:
            cells = area

        grid_points += np.ndarray.tolist(grid.grid_points_for_cell(cells)[0])
    return np.array(grid_points)

def cells_for_identifier(areas_or_cells, grid=None):
    '''
    Return cell numbers for the passed areas (or cells)

    Parameters
    ----------
    areas_or_cells : str or list
        List of cells (trivial), list of area names or 'global'

    Returns
    -------
    cells: np.array
        List of cells on the CCI Grid
    '''
    if grid is None:
        grid = SMECV_Grid_v042()

    if isinstance(areas_or_cells, str):
        if areas_or_cells == 'global':
            cells = grid.get_cells().tolist()
        else:
            cells = cells_for_area(areas_or_cells)
    elif isinstance(areas_or_cells, list):
        if all((isinstance(i, str) for i in areas_or_cells)):
            cells = cells_for_area(*areas_or_cells)
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