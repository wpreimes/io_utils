# -*- coding: utf-8 -*-

"""
Module description
"""
# TODO:
#   (+) 
#---------
# NOTES:
#   -


import xarray as xr
import numpy as np
import pandas as pd
import os
from pygeogrids.grids import BasicGrid, CellGrid


def join_files(tmp_dir, out_file, mfdataset=False, global_attrs=None):
    if mfdataset:
        cell_data = xr.open_mfdataset(os.path.join(tmp_dir, '*.nc'))
        cell_data.to_netcdf(out_file)
    else:
        if len(os.listdir(tmp_dir)) == 0:
            return
    dfs = []
    for filename in os.listdir(tmp_dir):
        ds = xr.open_dataset(os.path.join(tmp_dir, filename))
        dfs.append(ds.to_dataframe().dropna(how='all'))

    df = pd.concat(dfs, axis=0, sort=True)

    ds = df.to_xarray()
    if global_attrs is not None:
        ds = ds.assign_attrs(global_attrs)

    ds.to_netcdf(out_file, mode='w', engine='scipy')


def minmax(values):
    return np.nanmin(values), np.nanmax(values)


