# -*- coding: utf-8 -*-

"""
Module description
"""
# TODO:
#   (+) 
#---------
# NOTES:
#   -

from pygeogrids.netcdf import load_grid
from pynetcf.time_series import GriddedNcOrthoMultiTs
import os
from io_utils.read.geo_ts_readers.mixins import OrthoMultiTsCellReaderMixin

class MERRATs(GriddedNcOrthoMultiTs, OrthoMultiTsCellReaderMixin):
    def __init__(self, ts_path=None, grid_path=None, **kwargs):
        if grid_path is None:
            grid_path = os.path.join(ts_path, "grid.nc")

        grid = load_grid(grid_path)
        super(MERRATs, self).__init__(ts_path, grid, **kwargs)

    def read(self, *args, **kwargs):
        df = super(MERRATs, self).read(*args, **kwargs)
        return df