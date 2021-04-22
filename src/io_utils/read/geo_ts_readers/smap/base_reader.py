# -*- coding: utf-8 -*-

"""
Time Series Reader for the SMAP Time Series
"""

from pygeogrids.netcdf import load_grid
from pynetcf.time_series import GriddedNcOrthoMultiTs
import os
from netCDF4 import num2date
import pandas as pd

class SMAPTs(GriddedNcOrthoMultiTs):

    _t0_var = 'tb_time_seconds'
    _t0_unit = 'seconds since 2000-01-01T12:00' # from tb_time_seconds long_name

    def __init__(self, ts_path=None, grid_path=None, exact_index=False, **kwargs):
        if grid_path is None:
            grid_path = os.path.join(ts_path, "grid.nc")

        grid = load_grid(grid_path)
        super(SMAPTs, self).__init__(ts_path, grid, **kwargs)

        self.exact_index = exact_index

        if self.exact_index and \
                (self.parameters is not None and self._t0_var not in self.parameters):
            self.parameters.append(self._t0_var)

    def _to_datetime(self, df):
        df['_date'] = df.index.values
        num = df[self._t0_var].dropna()
        if len(num) == 0:
            df.loc[num.index, '_datetime'] = []
        else:
            df.loc[num.index, '_datetime'] = \
                pd.DatetimeIndex(num2date(num.values, units=self._t0_unit,
                                calendar='standard', only_use_cftime_datetimes=False))
        df = df.set_index('_datetime')
        df = df[df.index.notnull()]
        return  df

    def read(self, *args, **kwargs):
        df = super(SMAPTs, self).read(*args, **kwargs)
        if self.exact_index:
            df = self._to_datetime(df)
        return df