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
from io_utils.read.geo_ts_readers.mixins import CellReaderMixin

class ERATs(GriddedNcOrthoMultiTs, CellReaderMixin):
    # The basic ERA TS reader, with some features
    def __init__(self, ts_path, grid_path=None, **kwargs):
        if grid_path is None:
            grid_path = os.path.join(ts_path, "grid.nc")

        grid = nc.load_grid(grid_path)
        super(ERATs, self).__init__(ts_path, grid, **kwargs)

    def read(self, *args, **kwargs):
        df = super(ERATs, self).read(*args, **kwargs)

        return df