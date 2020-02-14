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
from datetime import datetime
import pandas as pd
from collections import OrderedDict
import numpy as np

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


class GeoCCITs(CCITs):
    # Reader implementation that uses the PATH configuration from above

    # exact time variable (days) from reference date
    _t0_ref = ('t0', datetime(1970,1,1,0,0,0))

    # fill values in the data columns
    _col_fillvalues = {'sm': [-9999.0],
                       'sm_uncertainty': [-9999.0],
                       }

    def __init__(self, ts_path, grid_path=None, exact_index=False, **kwargs):

        super(GeoCCITs, self).__init__(ts_path, grid_path=grid_path, **kwargs)
        self.exact_index = exact_index

    def _replace_with_nan(self, df):
        """
        Replace the fill values in columns defined in _col_fillvalues with NaN
        """
        for col in df.columns:
            if col in self._col_fillvalues.keys():
                for fv in self._col_fillvalues[col]:
                    if self.scale_factors is not None and \
                            col in self.scale_factors.keys():
                        fv = fv * self.scale_factors[col]
                    df.loc[df[col] == fv, col] = np.nan
        return df

    def _add_time(self, df):
        t0 = self._t0_ref[0]
        if t0 in df.columns:
            dt = pd.to_timedelta(df[t0], unit='d')
            df['t0'] = pd.Series(index=df.index, data=self._t0_ref[1]) + dt
            if self.exact_index:
                df = df.set_index('t0')
                df = df[df.index.notnull()]

        return df

    def read(self, *args, **kwargs):
        return self._add_time(self._replace_with_nan(
             super(GeoCCITs, self).read(*args, **kwargs)))

    def read_cells(self, cells):
        cell_data = OrderedDict()
        gpis, lons, lats = self.grid.grid_points_for_cell(list(cells))
        for gpi, lon, lat in zip(gpis, lons, lats):
            df = self.read(lon, lat)
            cell_data[gpi] = df
        return cell_data

if __name__ == '__main__':
    ds = CCITs(r'D:\data-read\CCI_45_D_TS\combined')
    ts = ds.read(15,45)