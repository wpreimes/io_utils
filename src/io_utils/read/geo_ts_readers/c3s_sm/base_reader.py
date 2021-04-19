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
from datetime import datetime, timedelta
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
        super(C3STs, self).__init__(ts_path, grid, automask=True, **kwargs)

    def read(self, *args, **kwargs):
        df = super(C3STs, self).read(*args, **kwargs)

        return df

class GeoC3STs(C3STs):
    # Reader implementation that uses the PATH configuration from above
    # Flagging should be done with the masking adapter from pytesmo
    _t0_ref = ('t0', datetime(1970,1,1,0,0,0)) # todo: use t0 from metadata

    _col_fillvalues = {'sm': [-9999.0],
                       'sm_uncertainty': [-9999.0],
                       _t0_ref[0]: [-3440586.5, -9999.]}

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
        self.exact_index = exact_index

        super(GeoC3STs, self).__init__(ts_path, grid_path=grid_path, **kwargs)

        if (self.parameters is not None) and self.exact_index and \
                (self._t0_ref[0] not in self.parameters):
            self.parameters.append(self._t0_ref[0])

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
            df['_datetime'] = pd.Series(index=df.index, data=self._t0_ref[1]) + dt
            if self.exact_index:
                df['_date'] = df.index
                df = df.set_index('_datetime')
                df = df[df.index.notnull()]

        return df

    def read(self, *args, **kwargs):
        return self._add_time(self._replace_with_nan(
            super(GeoC3STs, self).read(*args, **kwargs)))

    def read_cell_file(self, cell, var):
        """
        Read a whole cell file

        Parameters
        ----------
        cell : int
            Cell / filename to read.
        var : str
            Name of the variable to extract from the cellfile.

        Returns
        -------
        data : np.array
            Data for var in cell
        """

        file_path = os.path.join(self.path, '{}.nc'.format("%04d" % (cell,)))
        with nc.Dataset(file_path) as ncfile:
            loc_id = ncfile.variables['location_id'][:]
            time = ncfile.variables['time'][:]
            unit_time = ncfile.variables['time'].units
            delta = lambda t: timedelta(t)
            vfunc = np.vectorize(delta)
            since = pd.Timestamp(unit_time.split('since ')[1])
            time = since + vfunc(time)
            variable = ncfile.variables[var][:]
            variable = np.transpose(variable)
            data = pd.DataFrame(variable, columns=loc_id, index=time)
            if var in self._col_fillvalues.keys():
                data = data.replace(self._col_fillvalues[var], np.nan)
            return data

    def read_cells(self, cells):
        cell_data = OrderedDict()
        gpis, lons, lats = self.grid.grid_points_for_cell(list(cells))
        for gpi, lon, lat in zip(gpis, lons, lats):
            df = self.read(lon, lat)
            cell_data[gpi] = df
        return cell_data

if __name__ == '__main__':
    # ds = C3STs(r"R:\Datapool_processed\C3S\v201706\TCDR\063_images_to_ts\combined-daily")
    # ds.read(15,45)
    ds_new = GeoC3STs(r"R:\Datapool\C3S\02_processed\v201912\TCDR\063_images_to_ts\combined-daily",
                      exact_index=True)
    ts_new = ds_new.read(659123)

