# -*- coding: utf-8 -*-

"""
Reader for the ESA CCI SWI time series data of different versions
"""
# TODO:
#   (+)
#---------
# NOTES:
#   -

from pynetcf.time_series import GriddedNcOrthoMultiTs
import os
import pygeogrids.netcdf as nc
from datetime import datetime
import pandas as pd
from collections import OrderedDict
import numpy as np

class CCISWITs(GriddedNcOrthoMultiTs):
    # The basic CCI TS netcdf reader, with some features
    def __init__(self, ts_path, grid_path=None, **kwargs):
        if grid_path is None:
            grid_path = os.path.join(ts_path, "grid.nc")

        grid = nc.load_grid(grid_path)
        super(CCISWITs, self).__init__(ts_path, grid, **kwargs)

    def read_cell(self, *args):
        for ts in self.iter_ts():
            print(ts)

    def read_ts(self, *args, **kwargs):
        df = super(CCISWITs, self).read(*args, **kwargs)
        return df


class GeoCCISWITs(CCISWITs):
    # Reader implementation that uses the PATH configuration from above

    # exact time variable (days) from reference date
    _t0_ref = ('t0', datetime(1970,1,1,0,0,0))

    # fill values in the data columns
    _col_fillvalues = {}

    def __init__(self, ts_path, grid_path=None, exact_index=False, **kwargs):

        super(GeoCCISWITs, self).__init__(ts_path, grid_path=grid_path, **kwargs)
        self.exact_index = exact_index

    def read(self, *args, **kwargs):
        return super(GeoCCISWITs, self).read(*args, **kwargs)

    def read_cells(self, cells):
        cell_data = OrderedDict()
        gpis, lons, lats = self.grid.grid_points_for_cell(list(cells))
        for gpi, lon, lat in zip(gpis, lons, lats):
            df = self.read(lon, lat)
            cell_data[gpi] = df
        return cell_data

if __name__ == '__main__':
    ds = GeoCCISWITs(r'R:\Projects\G3P\07_data\SWI_CCI_04.7\SWI_CCI_v04.7_TS')
    ts = ds.read(15,45)
    celldata = ds.read_cell(2244)