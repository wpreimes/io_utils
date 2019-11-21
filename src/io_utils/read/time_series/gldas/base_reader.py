# -*- coding: utf-8 -*-

"""
The base reader class without any modifications for reading GLDAS Time series.
As in the gldas package (but we don't want to install the whole package)
"""
# TODO:
#   (+) 
#---------
# NOTES:
#   -

from pygeogrids.netcdf import load_grid
from pynetcf.time_series import GriddedNcOrthoMultiTs
import os

class GLDASTs(GriddedNcOrthoMultiTs):
    def __init__(self, ts_path, grid_path=None, **kwargs):
        if grid_path is None:
            grid_path = os.path.join(ts_path, "grid.nc")

        grid = load_grid(grid_path)
        super(GLDASTs, self).__init__(ts_path, grid, **kwargs)

    def read(self, *args, **kwargs):
        df = super(GLDASTs, self).read(*args, **kwargs)
        return df