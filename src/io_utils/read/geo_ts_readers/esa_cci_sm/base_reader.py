# -*- coding: utf-8 -*-

"""
Reader for the ESA CCI SM time series data of different versions
"""
# TODO:
#   (+) 
#---------
# NOTES:
#   -

from pynetcf.time_series import GriddedNcOrthoMultiTs
import os
import pygeogrids.netcdf as nc

class CCITs(GriddedNcOrthoMultiTs):
    # The basic CCI TS netcdf reader, with some features
    def __init__(self, ts_path, grid_path=None, **kwargs):
        if grid_path is None:
            grid_path = os.path.join(ts_path, "grid.nc")

        grid = nc.load_grid(grid_path)
        super(CCITs, self).__init__(ts_path, grid, **kwargs)

    def read_ts(self, *args, **kwargs):
        df = super(CCITs, self).read(*args, **kwargs)
        return df


if __name__ == '__main__':
    ds = CCITs(r'D:\data-read\CCI_45_D_TS\combined')
    ts = ds.read(15,45)