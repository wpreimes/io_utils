# -*- coding: utf-8 -*-

"""
Reader for the ESA CCI SWI time series data of different versions
"""
# TODO:
#   (+)
#---------
# NOTES:
#   -

from pynetcf.time_series import GriddedNcOrthoMultiTs
import os
import pygeogrids.netcdf as nc
import pandas as pd
from collections import OrderedDict
import numpy as np
from datetime import timedelta

class CCISWITs(GriddedNcOrthoMultiTs):
    # The basic CCI TS netcdf reader, with some features
    def __init__(self, ts_path, grid_path=None, **kwargs):
        if grid_path is None:
            grid_path = os.path.join(ts_path, "grid.nc")

        grid = nc.load_grid(grid_path)
        super(CCISWITs, self).__init__(ts_path, grid, **kwargs)

    def read_ts(self, *args, **kwargs):
        df = super(CCISWITs, self).read(*args, **kwargs)
        return df


class GeoCCISWITs(CCISWITs):
    # Reader implementation that uses the PATH configuration from above

    # fill values in the data columns
    _col_fillvalues = {}

    def __init__(self, ts_path, grid_path=None, **kwargs):

        super(GeoCCISWITs, self).__init__(ts_path, grid_path=grid_path, **kwargs)

    def read(self, *args, **kwargs):
        return super(GeoCCISWITs, self).read(*args, **kwargs)

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
    ds = GeoCCISWITs(r'R:\Projects\G3P\07_data\SWI\SWI_CCI_v04.7_contUSA_TS')
    for offsetx in [0.,0.25,-0.25]:
        for offsety in [0.,0.25,-0.25]:
            loc = (-119.875+offsetx, 43.625+offsety)
            ts = ds.read(*loc)
            print(loc)
            print(ts.loc['2011-06-13', 'SSM'])
