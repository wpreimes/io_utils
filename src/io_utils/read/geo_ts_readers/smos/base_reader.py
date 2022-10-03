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
from netCDF4 import num2date
import pandas as pd
from io_utils.read.geo_ts_readers.mixins import OrthoMultiTsCellReaderMixin

class SMOSTs(GriddedNcOrthoMultiTs, OrthoMultiTsCellReaderMixin):

    _t0_vars = {'sec': 'UTC_Seconds', 'days': 'Days'}
    _t0_unit = 'days since 2000-01-01'

    def __init__(self, ts_path=None, grid_path=None, exact_index=False,
                 **kwargs):

        if grid_path is None:
            grid_path = os.path.join(ts_path, "grid.nc")

        grid = load_grid(grid_path)
        super(SMOSTs, self).__init__(ts_path, grid, **kwargs)

        self.exact_index = exact_index
        if (self.parameters is not None) and self.exact_index:
            for v in self._t0_vars.values():
                self.parameters.append(v)

    def _to_datetime(self, df):
        units = self._t0_unit

        df['_date'] = df.index.values
        num = df[self._t0_vars['days']].dropna() + \
              (df[self._t0_vars['sec']].dropna() / 86400)
        if len(num) == 0:
            df.loc[num.index, 'exact_time'] = []
        else:
            df.loc[num.index, 'exact_time']= \
                pd.DatetimeIndex(num2date(num.values, units=units,
                                 calendar='standard', only_use_cftime_datetimes=False))

        df = df.set_index('exact_time')
        df = df[df.index.notnull()]
        return df

    def read(self, *args, **kwargs):
        df = super(SMOSTs, self).read(*args, **kwargs)
        if self.exact_index:
            df = self._to_datetime(df)

        return df

