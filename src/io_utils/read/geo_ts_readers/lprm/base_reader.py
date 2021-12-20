# -*- coding: utf-8 -*-

"""
LPRM time series reader
"""
from pynetcf.time_series import GriddedNcOrthoMultiTs
import os
import pygeogrids.netcdf as nc
from cadati.jd_date import jd2dt
from io_utils.utils import mjd2jd
from io_utils.read.geo_ts_readers.mixins import OrthoMultiTsCellReaderMixin

class LPRMTs(GriddedNcOrthoMultiTs, OrthoMultiTsCellReaderMixin):

    _t0 = 'SCANTIME_MJD'

    def __init__(self, ts_path, exact_index=False, grid_path=None, **kwargs):
        if grid_path is None:
            grid_path = os.path.join(ts_path, "grid.nc")

        grid = nc.load_grid(grid_path)
        super(LPRMTs, self).__init__(ts_path, grid, automask=True, **kwargs)

        self.exact_index = exact_index
        if exact_index and (self.parameters is not None):
            self.parameters.append(self._t0)

    def read(self, *args, **kwargs):
        df = super(LPRMTs, self).read(*args, **kwargs)
        if self.exact_index:
            df[self._t0] = jd2dt(mjd2jd(df[self._t0].values))
            df = df.set_index(self._t0) # drop nan index
            df = df.loc[df.index.dropna()]

        return df