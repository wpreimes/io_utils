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
from pygeobase.io_base import GriddedTsBase
from pygenio.time_series import IndexedRaggedTs
from smecv_grid.grid import SMECV_Grid_v052
from cadati.jd_date import julian2date
import pytz
from datetime import datetime
from pygeogrids import CellGrid

def julian2datetimeindex(j, tz=pytz.UTC):
    """
    Converting Julian days to datetimeindex.
    Parameters
    ----------
    j : numpy.ndarray or int32
        Julian days.
    tz : instance of pytz, optional
        Time zone. Default: UTC
    Returns
    -------
    datetime : pandas.DatetimeIndex
        Datetime index.
    """
    year, month, day, hour, minute, second, microsecond = julian2date(j)

    return pd.DatetimeIndex([datetime(y, m, d, h, mi, s, ms, tz)
                             for y, m, d, h, mi, s, ms in
                             zip(year, month, day, hour, minute,
                                 second, microsecond)])

class CCIDs(GriddedTsBase):

    """
    CCI Dataset class reading genericIO data in the CCI common format

    Data in common input format is
    returned as a pandas.DataFrame for temporal resampling.

    Parameters
    ----------
    path: string
        Path to dataset.
    mode: str, optional
        File mode and can be read 'r', write 'w' or append 'a'. Default: 'r'
    grid: grid object
        Grid on which to work
    fn_format: str, optional
        The filename format of the cell files. Default: '{:04d}'
    Parameters : str or list, optional (default: None)
        limit reading to these columns
    """

    def __init__(self, path, mode='r', grid=None, fn_format='{:04d}',
                 custom_dtype=None):
        if grid is None:
            grid = SMECV_Grid_v052()

        super(CCIDs, self).__init__(path, grid, IndexedRaggedTs,
                                    mode=mode,
                                    fn_format=fn_format,
                                    ioclass_kws={'custom_dtype': custom_dtype})

    def _read_gp(self, gpi, only_valid=False, mask_sm_nan=False,
                 mask_invalid_flags=False, sm_nan=-999999.,
                 mask_jd=False, jd_min=2299160, jd_max=1827933925,
                 valid_flag=0, **kwargs):
        """
        Read data into common format

        Parameters
        ----------
        self: type
            description
        gpi: int
            grid point index
        parameters: list or str, optional (default: None)
            Name of one or multiple columns to read.
        only_valid: boolen, optional
           if set only valid observations will be returned.
           This means that the data will be masked for soil moisture
           NaN values and also for flags other than 0
        mask_sm_nan: boolean, optional
           if set to True then the time series will be masked
           for soil moisture NaN values
        mask_invalid_flags: boolean, optional
           if set then all flags that do not have the value of
           valid_flag are removed
        sm_nan: float, optional
           value to use as soil moisture NaN
        valid_flag: int, optional
           value indicating a valid flag

        Returns
        -------
        ts: pandas.DataFrame
            DataFrame in common format
        """

        ts = super(CCIDs, self)._read_gp(gpi, **kwargs)

        if ts is None:
            return None

        if only_valid:
            mask_sm_nan = True
            mask_invalid_flags = True
        if mask_sm_nan:
            ts = ts[ts['sm'] != sm_nan]
        if mask_invalid_flags:
            ts = ts[ts['flag'] == valid_flag]
        if mask_jd:
            ts = ts[(ts['jd'] >= jd_min) & (ts['jd'] <= jd_max)]
        if ts.size == 0:
            raise IOError("No data for gpi %i" % gpi)

        index_tz = julian2datetimeindex(ts['jd'])
        index_no_tz = pd.DatetimeIndex([i.tz_localize(None) for i in index_tz])

        ts = pd.DataFrame(ts, index=index_no_tz)

        return ts

    def read_cell(self, cell):
        """
        Read complete data set from cell file.

        Parameters
        ----------
        cell: int
            Cell number.

        Returns
        -------
        location_id: numpy.ndarray
            Location ids.
        cell_data: numpy.recarray
            Cell data set.
        """
        if isinstance(self.grid, CellGrid) is False:
            raise TypeError("Associated grid is not of type "
                            "pygeogrids.CellGrid.")

        if self.mode != 'r':
            raise ValueError("File not opened in read mode.")

        filename = os.path.join(self.path, self.fn_format.format(cell))
        self.fid = self.ioclass(filename, mode=self.mode, **self.ioclass_kws)

        cell_data = self.fid.dat_fid.read()
        self.fid.dat_fid.close()

        return self.fid.idx, cell_data


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
    ds = CCIDs(r"\\project9\data-write\RADAR\ESA_CCI_SM\v06.0\python3_new_grid\042_combined_MergedProd")
    ts = ds.read(-104,38)

    ds2 = CCITs(r'R:\Datapool\ESA_CCI_SM\02_processed\ESA_CCI_SM_v05.2\timeseries\combined',
               exact_index=False)
    ts2 = ds2.read(-104,38)
