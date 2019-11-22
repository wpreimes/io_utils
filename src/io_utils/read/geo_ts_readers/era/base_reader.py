# -*- coding: utf-8 -*-

"""
The basic, unchanged time series reader for the c3s time series, as in the
esa_cci_sm package.
"""
# TODO:
#   (+) 
#---------
# NOTES:
#   -

from pynetcf.time_series import GriddedNcOrthoMultiTs
import os
import pygeogrids.netcdf as nc

class ERATs(GriddedNcOrthoMultiTs):
    # The basic ERA TS reader, with some features
    def __init__(self, ts_path, grid_path=None, resample=None, **kwargs):
        if grid_path is None:
            grid_path = os.path.join(ts_path, "grid.nc")

        self.resample = resample
        grid = nc.load_grid(grid_path)
        super(ERATs, self).__init__(ts_path, grid, **kwargs)

    def read(self, *args, **kwargs):
        df = super(ERATs, self).read(*args, **kwargs)
        if self.resample:
            df = df.resample(self.resample).mean()

        return df