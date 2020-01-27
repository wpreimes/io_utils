# -*- coding: utf-8 -*-

"""
Time Series Reader for the SMOS Time Series
"""
# TODO:
#   (+) 
#---------
# NOTES:
#   -

from pygeogrids.netcdf import load_grid
from pynetcf.time_series import GriddedNcOrthoMultiTs
import os

class SMOSTs(GriddedNcOrthoMultiTs):
    def __init__(self, ts_path=None, grid_path=None, **kwargs):
        if grid_path is None:
            grid_path = os.path.join(ts_path, "grid.nc")

        grid = load_grid(grid_path)
        super(SMOSTs, self).__init__(ts_path, grid, **kwargs)

    def read(self, *args, **kwargs):
        df = super(SMOSTs, self).read(*args, **kwargs)
        return df