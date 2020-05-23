# -*- coding: utf-8 -*-

"""
AMSR2 time series reader
"""
from pynetcf.time_series import GriddedNcOrthoMultiTs
import os
import pygeogrids.netcdf as nc

class LPRMTs(GriddedNcOrthoMultiTs):
    def __init__(self, ts_path, grid_path=None, **kwargs):
        if grid_path is None:
            grid_path = os.path.join(ts_path, "grid.nc")

        grid = nc.load_grid(grid_path)
        super(LPRMTs, self).__init__(ts_path, grid, automask=True, **kwargs)

    def read(self, *args, **kwargs):
        df = super(LPRMTs, self).read(*args, **kwargs)

        return df

if __name__ == '__main__':
    path = r"R:\Datapool\AMSR2\02_processed\AMSR2_S3_VEGC_LPRMv6\timeseries\v202001\d"
    ds = LPRMTs(path)
    ts = ds.read(45,15)
