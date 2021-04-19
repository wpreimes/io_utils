# -*- coding: utf-8 -*-

"""
AMSR2 time series reader
"""
from pynetcf.time_series import GriddedNcOrthoMultiTs
import os
import pygeogrids.netcdf as nc
from cadati.jd_date import jd2dt
from io_utils.utils import mjd2jd

class LPRMTs(GriddedNcOrthoMultiTs):

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

if __name__ == '__main__':
    path = r"\\project9\data-read\RADAR\Datapool_processed\LPRM\v6\SMAP_S3_VEGC\timeseries\d"
    ds = LPRMTs(path, exact_index=True)
    ts = ds.read(45,15)
