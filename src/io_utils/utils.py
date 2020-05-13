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
    """
    Split list of elements in n approx. equal parts for multiprocessing

    Parameters
    ----------
    el : list
        List of elements to split
    n : int
        Number of lists to split input up into

    Returns
    -------
    parts : Iterable
        List of n lists of parts of the input
    """
    k, m = divmod(len(list(el)), n)
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

    return p

def filter_months(df, months, dropna=False):
    """
    Select only entries of a time series that are within certain month(s)

    Parameters
    ----------
    df : pd.DataFrame
        Time series (index.month must exist) that is filtered
    months : list
        Months for which data is kept, e.g. [12,1,2] to keep data for winter
    dropna : bool, optional (default: False)
        Drop lines for months that are not to be kept, if this is false, the
        original index is not changed, but filtered values are replaced with nan.

    Returns
    -------
    df_filtered : pd.DataFrame
        The filtered series
    """

    dat = df.copy(True)
    dat['__index_month'] = dat.index.month
    cond = ['__index_month == {}'.format(m) for m in months]
    selection = dat.query(' | '.join(cond)).index
    dat.drop('__index_month', axis=1, inplace=True)

    if dropna:
        return dat.loc[selection]
    else:
        dat.loc[dat.index.difference(selection)] = np.nan
        return dat

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    ds = pd.DataFrame(index=pd.date_range(start='2000-01-01', end='2010-12-31', freq='D'),
                   data={'data': range(4018), 'flag': np.full(4018, 1)})
    fil = filter_months(ds, months=[12,1,2])