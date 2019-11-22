# -*- coding: utf-8 -*-

"""
The basic, unchanged time series reader for the c3s time series, as in the
c3s_sm package.
"""
# TODO:
#   (+) Use the reader from the c3s package directly?
#---------
# NOTES:
#   -


from pynetcf.time_series import GriddedNcOrthoMultiTs
import os
import pygeogrids.netcdf as nc

class C3STs(GriddedNcOrthoMultiTs):
    # The basic ERA TS reader, with some features
    def __init__(self, ts_path, grid_path=None, **kwargs):
        if grid_path is None:
            grid_path = os.path.join(ts_path, "grid.nc")

        grid = nc.load_grid(grid_path)
        super(C3STs, self).__init__(ts_path, grid, **kwargs)

    def read(self, *args, **kwargs):
        df = super(C3STs, self).read(*args, **kwargs)

        return df

if __name__ == '__main__':
    ds = C3STs(r"R:\Datapool_processed\C3S\v201706\TCDR\063_images_to_ts\combined-daily")
    ds.read(15,45)