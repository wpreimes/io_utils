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
from datetime import datetime
import pygeogrids.netcdf as nc
import pandas as pd
from collections import OrderedDict
import numpy as np

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

class GeoC3STs(C3STs):
    # Reader implementation that uses the PATH configuration from above
    # Flagging should be done with the masking adapter from pytesmo
    _t0_ref = ('t0', datetime(1970,1,1,0,0,0))

    _col_fillvalues = {'sm': [-9999.0],
                       'sm_uncertainty': [-9999.0],
                       _t0_ref[0]: [-3440586.5]}

    def __init__(self, ts_path, grid_path=None, exact_index=False, **kwargs):
        """
        Parameters
        ----------
        dataset : tuple
            e.g. ('C3S', 'v201812', 'COMBINED', 'TCDR')
        force_path_group : str, optional (default: None)
            Select a specific path group from the path config to read.
        kwargs :
            kwargs that are passed to load_path and to initialise the reader.
        """
        super(GeoC3STs, self).__init__(ts_path, grid_path=grid_path, **kwargs)
        self.exact_index = exact_index

    def _replace_with_nan(self, df):
        """
        Replace the fill values in columns defined in __new__ with NaN
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
        return self._replace_with_nan(
            super(GeoC3STs, self).read(*args, **kwargs))

    def read_cells(self, cells):
        cell_data = OrderedDict()
        gpis, lons, lats = self.grid.grid_points_for_cell(list(cells))
        for gpi, lon, lat in zip(gpis, lons, lats):
            df = self.read(lon, lat)
            cell_data[gpi] = df
        return cell_data

if __name__ == '__main__':
    ds = C3STs(r"R:\Datapool_processed\C3S\v201706\TCDR\063_images_to_ts\combined-daily")
    ds.read(15,45)