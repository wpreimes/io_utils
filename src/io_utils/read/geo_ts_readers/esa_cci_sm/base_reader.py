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
from collections import OrderedDict
import netCDF4
import pandas as pd

class CCITs(GriddedNcOrthoMultiTs):
    # The basic CCI TS netcdf reader, with some features

    def __init__(self, ts_path, grid_path=None, exact_index=False,
                 ioclass_kws=None, **kwargs):

        if grid_path is None:
            grid_path = os.path.join(ts_path, "grid.nc")

        if ioclass_kws is None:
            ioclass_kws = {'read_bulk': True}
        else:
            if 'read_bulk' not in ioclass_kws.keys():
                ioclass_kws['read_bulk'] = True

        grid = nc.load_grid(grid_path)

        super(CCITs, self).__init__(ts_path, grid, ioclass_kws=ioclass_kws,
                                    **kwargs)

        self.exact_index = exact_index
        self.t0 = 't0' # observation time stamp variable
        if (self.parameters is not None) and self.exact_index:
            self.parameters.append(self.t0)

    def read(self, *args, **kwargs):
        """ Read TS by gpi or by lonlat """
        df = super(CCITs, self).read(*args, **kwargs)
        if self.exact_index:
            units = self.fid.dataset.variables[self.t0].units
            df = df.set_index(self.t0)
            df = df[df.index.notnull()]
            if len(df.index.values) == 0:
                df.index = pd.DatetimeIndex()
            else:
                df.index = pd.DatetimeIndex(
                    netCDF4.num2date(df.index.values, units=units, calendar='standard',
                             only_use_cftime_datetimes=False))
        return df

    def read_cells(self, cells):
        cell_data = OrderedDict()
        gpis, lons, lats = self.grid.grid_points_for_cell(list(cells))
        for gpi, lon, lat in zip(gpis, lons, lats):
            df = self.read(lon, lat)
            cell_data[gpi] = df
        return cell_data


if __name__ == '__main__':
    ds = CCITs(r'R:\Datapool\ESA_CCI_SM\02_processed\ESA_CCI_SM_v05.2\timeseries\combined',
               exact_index=True)
    ts = ds.read(-104,38)
