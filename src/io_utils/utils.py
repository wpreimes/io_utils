# -*- coding: utf-8 -*-

"""
Utility functions that are used in all modules
"""
# TODO:
#   (+) 
#---------
# NOTES:
#   -

import logging
from datetime import datetime, timedelta
import os
from pprint import pprint

import numpy as np
import pandas as pd
from matplotlib.dates import date2num


def safe_arange(start, stop, step):
    f_step = (1. / float(step))
    vals = np.arange(float(start) * f_step, float(stop) * f_step , float(step) * f_step)
    return vals / f_step

def log(msg=None, lvl=0, error=False, printit=False):
    if not msg:
        msg = '-'*100
    if error:
        logging.error('{}{}: {}'.format('.'*(lvl*3), str(datetime.now()), str(msg)))
    else:
        logging.info('{}{}: {}'.format('.'*(lvl*3), str(datetime.now()), str(msg)))

    if printit:
        pprint(msg)

def setup_log(logfile, workfolder):
    logpath = os.path.join(workfolder, 'log')
    if not os.path.exists(logpath):
        os.makedirs(logpath)
    logfile = os.path.join(logpath, logfile)

    logging.basicConfig(filename=logfile, level=logging.DEBUG)
    logging.captureWarnings(True)

    return logfile


def dt_to_dec(dt):
    # Datetime object to decimal year
    startyear = datetime(dt.year, 1, 1)
    endyear = startyear.replace(year=dt.year + 1)
    return dt.year + ((dt - startyear).total_seconds() / float((endyear - startyear).total_seconds()))


def dates_to_num(dates):
    calendar = 'standard'
    units = 'days since 1900-01-01 00:00:00'
    timestamps=[]
    for date in dates:
        timestamps.append(pd.Timestamp(date).to_datetime())

    return np.sort(date2num(timestamps, units, calendar))


def datetime2matlabdn(dt):
    ord = dt.toordinal()
    mdn = dt + timedelta(days=366)
    frac = (dt - datetime(dt.year, dt.month, dt.day, 0, 0, 0)).seconds / (24.0 * 60.0 * 60.0)
    return mdn.toordinal() + frac



def split(el, n):
    '''
    Split list of elements in n approx. equal parts for multiprocessing

    Parameters
    --------
    el : list
        List of elements to split
    n : int
        Number of lists to split input up into

    Returns
    ---------
    split : list
        Lists of n parts of the input
    '''

    k, m = divmod(len(el), n)
    parts = [el[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]
    return parts


def split_cells_gpi_equal(all_cells, n, grid):
    ''' Split a list of cells in equal parts. Consider the number of points
    per cell, so that in each part approx. the same number of gpis are

    Parameters
    --------
    all_cells : list
        List of cell number that should be split
    n : int
        Number of separate lists that the input is plit into
    grid : pygeogrids.CellGrid
        Grid on which the input and output cells are

    Returns
    --------
    rparts : tuple
        Tuple of lists of all parts (about equal number of gpis)
    '''

    parts = {i:[0, []] for i in range(n)}
    min_part = 0
    for cell in all_cells:
        g = grid.grid_points_for_cell(cell)[0].size
        parts[min_part][1] += [cell]
        parts[min_part][0] += g

        counter = {k: v[0] for k, v in parts.items()}
        min_part = min(counter, key=counter.get)

    rparts = tuple([np.array(parts[j][1]) for j in range(n)])
    return rparts


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

def create_workfolder(path, no_version_folder=False):
    i = 1
    while os.path.exists(os.path.join(path, 'v' + str(i))):
        i += 1
    else:
        if no_version_folder:
            p = os.path.join(path)
        else:
            p = os.path.join(path, 'v' + str(i))

        if not os.path.exists(p): os.makedirs(p)

    print('Create workfolder: %s' % str(p))

    return p