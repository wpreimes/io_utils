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
import numpy as np
from datetime import timedelta
import xarray as xr
import warnings
from typing import Callable

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


class SmecvTs(GriddedNcOrthoMultiTs):
    # The basic CCI/C3S TS netcdf reader, with some features

    def __init__(self, ts_path, grid=None, exact_index=False, clip_dates=None,
                 ioclass_kws=None, **kwargs):
        """
        Read ESA CCI SM in time series format from netcdf files

        Parameters
        ----------
        ts_path : str
            Path to where the data is stored
        grid : str or pygeogrids.CellGrid, optional (default: None)
            Grid that the time series are searched on
        exact_index : bool, optional (default: False)
            Apply t0 to daily time stamps to read exact observations times.
        clip_dates : tuple[datetime, datetime], optional (default: None)
            Cut the time series to this date range (start, end)
        ioclass_kws : dict, optional (default: None)
            IO class kwargs used by pyntecf
        kwargs:
            Additional kwargs are given to pynetcf OrthoMultiTs.
        """
        self.t0 = 't0' # observation time stamp variable

        if grid is None:
            grid = os.path.join(ts_path, "grid.nc")

        if ioclass_kws is None:
            ioclass_kws = {'read_bulk': True}
        else:
            if 'read_bulk' not in ioclass_kws.keys():
                ioclass_kws['read_bulk'] = True

        if isinstance(grid, CellGrid):
            pass
        else:
            grid = nc.load_grid(grid)

        super(SmecvTs, self).__init__(ts_path, grid, automask=True,
                                    ioclass_kws=ioclass_kws,
                                    **kwargs)

        self.clip_dates = clip_dates

        self.exact_index = exact_index

        if (self.parameters is not None) and self.exact_index and \
                (self.t0 not in self.parameters):
            self.parameters.append(self.t0)

    def _clip_dates(self, df) -> pd.DataFrame:
        # clip data frame to date range based in datetime index
        if isinstance(df.index, pd.MultiIndex):
            return df[(df.index.get_level_values('time') >= self.clip_dates[0]) &
                      (df.index.get_level_values('time') <= self.clip_dates[1])]
        else:
            return df[(df.index >= self.clip_dates[0]) &
                      (df.index <= self.clip_dates[1])]

    def read(self, *args, **kwargs) -> pd.DataFrame:
        """
        Read time series based on lonlat or gpi
        """
        df = super(SmecvTs, self).read(*args, **kwargs)

        if self.exact_index:
            try:
                units = self.fid.dataset.variables[self.t0].units
            except AttributeError:
                units = 'Days since 1970-01-01'

            df = df.loc[(df[self.t0] >= 0) & df[self.t0].notnull()]
            df = df.set_index(self.t0)
            if len(df.index.values) == 0:
                pass
            else:
                df.index = pd.DatetimeIndex(
                    netCDF4.num2date(df.index.values, units=units,
                                     calendar='standard',
                                     only_use_cftime_datetimes=False))

        if self.clip_dates:
            df = self._clip_dates(df)

        return df

    def read_cell_file(self, cell, param='sm'):
        """ Read a full cell file """
        if self.exact_index:
            warnings.warn("Reading cell with exact index not yet supported. Use read_cells()")

        file_path = os.path.join(self.path, '{}.nc'.format("%04d" % (cell,)))
        with nc.Dataset(file_path) as ncfile:
            loc_id = ncfile.variables['location_id'][:]
            time = ncfile.variables['time'][:]
            unit_time = ncfile.variables['time'].units
            delta = lambda t: timedelta(t)
            vfunc = np.vectorize(delta)
            since = pd.Timestamp(unit_time.split('since ')[1])
            time = since + vfunc(time)

            variable = ncfile.variables[param][:]
            variable = np.transpose(variable)
            data = pd.DataFrame(variable, columns=loc_id, index=time)

        if self.clip_dates:
            data = self._clip_dates(data)

        return data

    def read_cells(self, cells):
        """ Read all data for one or multiple cells as a data frame """
        cell_data = []
        gpis, lons, lats = self.grid.grid_points_for_cell(list(cells))
        for gpi, lon, lat in zip(gpis, lons, lats):
            df = self.read(lon, lat)
            df.columns = pd.MultiIndex.from_tuples((gpi, c) for c in df.columns)
            if not df.empty:
                cell_data.append(df)

        if len(cell_data) == 0:
            return pd.DataFrame()
        else:
            return pd.concat(cell_data, axis=0 if self.exact_index else 1)

    def read_agg_cell_data(self, cell, params, format='pd_multidx_df',
                           drop_coord_vars=True, to_replace=None,
                           **kwargs) -> dict or pd.DataFrame:
        """
        Read all time series for a single variable in the selected cell.

        Parameters
        ----------
        cell: int
            Cell number as in the c3s grid
        params: list or str
            Name of the variable(s) to read.
        format : str, optional (default: 'multiindex')
            * pd_multidx_df (default):
                Returns one data frame with gpi as first, and time as
                second index level.
            * gpidict : Returns a dictionary of dataframes, with gpis as keys
                        and time series data as values.
            * var_np_arrays : Returns 2d arrays for each variable and a variable
                              'index' with time stamps.
        to_replace : dict of dicts, optional (default: None)
            Dict for parameters of values to replace.
            e.g. {'sm': {-999999.0: -9999}}
            see pandas.to_replace()

        Additional kwargs are given to xarray to open the dataset.W

        Returns
        -------
        data : dict or pd.DataFrame
            A DataFrame if a single variable was passed, otherwise
            a dict of DataFrames with parameter name as key.
        """
        if self.exact_index:
            warnings.warn("Reading cell with exact index not yet supported. Use read_cells()")

        file_path = os.path.join(self.path, f'{cell:04}.nc')

        params = np.atleast_1d(params)

        if 'location_id' not in params:
            params = np.append(params, 'location_id')

        with xr.open_dataset(file_path, **kwargs) as ds:
            gpis = ds['location_id'].values
            mask = (gpis >= 0)
            gpis = gpis[mask]

            df = ds[params].to_dataframe(dim_order=['locations', 'time'])
            df = df.loc[ds['locations'].values[mask], :]
            df.rename(columns={'location_id': 'gpi'}, inplace=True)

            if drop_coord_vars:
                df.drop(columns=['alt', 'lon', 'lat'], inplace=True)

        if self.clip_dates:
            df = self._clip_dates(df)

        if to_replace is not None:
            df = df.replace(to_replace=to_replace)

        if format.lower() == 'pd_multidx_df':
            index = df.index.set_levels(gpis, level=0) \
                            .set_names('gpi', level=0)
            data = df.set_index(index)

        elif format.lower() == 'gpidict':
            df = df.set_index(df.index.droplevel(0))
            data = dict(tuple(df.groupby(df.pop('gpi'))))

        elif format.lower() == 'var_np_arrays':
            df = df.set_index(df.index.droplevel(0))
            index = df.index.unique()
            data = {'index': index}
            for col in df.columns:
                if col == 'gpi': continue
                data[col] = df.groupby('gpi')[col].apply(np.array)

        else:
            raise NotImplementedError

        return data

    def read_agg_cell_cube(
        self,
        cell:int,
        dt_index:pd.Index,
        params:list,
        param_fill_val:dict=None,
        param_scalf:dict=None,
        param_dtype:dict=None,
        to_replace=None,
        as_xr=False):
        """
        Read aggregated data for a cell.

        Parameters
        ----------
        cell : int
            Cell number to read data for.
        dt_index : pd.Index
            Index of time stamps to read data for.
            e.g. pd.date_range('2000-01-01', '2000-12-31', freq='D')
        params : list
            List of parameters to read
        param_fill_val : dict['str': float | int], optional (default: None)
            Fill values for each parameter to use for missing values,
            e.g. {'sm' : np.nan}
        param_scalf : dict[str: float | int], optional (default: None)
            Parameter names and scale factors, i.e. values that a parameter
            time series is multiplied with after reading.
        param_dtype : dict[str: str], optional (default: None)
            Data types that the parameter columns are converted into.
        to_replace : dict, optional (default: None)
            See read_agg_cell_data()
        as_xr : bool, optional (default: False)
            Read as xarray DataSet.

        Returns
        -------

        """

        def _template(name, gpis, fill_value=np.nan, dtype='float64'):
            ser = pd.Series(index=np.sort(gpis),
                            data=[np.full(len(dt_index), fill_value, dtype=dtype)] * len(gpis))
            ser.name = name
            return ser

        cell_gpi = self.grid.gpis[self.grid.arrcell == cell]
        cell_lons, cell_lats = self.grid.gpi2lonlat(cell_gpi)
        cell_gpi_shape = tuple([int(self.grid.cellsize / self.grid.resolution)] * 2)

        cell_gpi = np.flipud(cell_gpi.reshape(cell_gpi_shape))
        cell_lats = np.flipud(cell_lats.reshape(cell_gpi_shape))
        cell_lons = cell_lons.reshape(cell_gpi_shape)

        #read all data for a cell as data cube..
        if param_fill_val is None:
            param_fill_val = {}

        if param_dtype is None:
            param_dtype = {}

        if param_scalf:
            for p in param_scalf:
                if p not in param_fill_val:
                    warnings.warn(f"{p} : Value is scaled but not replaced, are you sure?")

        data_df = self.read_agg_cell_data(cell,
                                          params=params,
                                          format='var_np_arrays',
                                          to_replace=to_replace)

        for p in params:
            if p not in param_fill_val.keys():
                param_fill_val[p] = np.nan
            if p not in param_dtype.keys():
                param_dtype[p] = 'float64'

        if data_df is None: # file not found
            data_df = {'index': dt_index}
            for p in params:
                fill_value = param_fill_val[p]
                dtype= param_dtype[p]
                data_df[p] = _template(p,
                                       cell_gpi.flatten(),
                                       fill_value=fill_value,
                                       dtype=dtype)

        timestamps = data_df.pop('index')

        data_arr = {}
        for name, ds in data_df.items():
            if ds.index.size != cell_gpi.size:
                missing_gpis = np.setdiff1d(cell_gpi, ds.index.values)
                fill_val = param_fill_val[name]

                ds_missing_gpis = pd.Series(
                    index=missing_gpis,
                    data=[np.repeat(fill_val, len(timestamps))] * len(missing_gpis))

                data_df[name] = pd.concat([ds, ds_missing_gpis], axis=0, sort=True)
                assert len(data_df[name]) == cell_gpi.size, "Unexpected number of gpis"

            data_df[name] = data_df[name].sort_index(ascending=True)

            # from (time, gpi) to (gpi, time)
            arr = np.ndarray.view(np.transpose(np.vstack(data_df[name]))) # transpose?

            newshape = (len(timestamps), *cell_gpi_shape)
            arr = np.reshape(arr, newshape) #flip?

            data_arr[name] = np.ma.masked_equal(arr.astype(param_dtype[name]),
                                                param_fill_val[name],
                                                copy=False)

            param_scalf = {} if param_scalf is None else param_scalf

            if name in param_scalf.keys():
                data_arr[name] *= param_scalf[name]

        timestamps.name = 'time'
        if as_xr:
            data_vars = {}
            for name in data_arr.keys():
                attrs = {'dtype': str(data_arr[name].dtype)}
                if name in param_fill_val.keys():
                    attrs['_FillValue'] = data_arr[name].fill_value
                data_vars[name] = (['time', 'lat', 'lon'],
                                   data_arr[name].filled(),
                                   attrs)

            cube = xr.Dataset(
                data_vars=data_vars,
                coords={'time': timestamps.values.astype('datetime64[s]'),
                        'lon': np.array(np.unique(cell_lons.flatten()), np.float32),
                        'lat': np.array(np.unique(cell_lats.flatten()), np.float32)})

            return cube
        else:
            return data_arr, {'lon': cell_lons, 'lat': cell_lats, 'gpi': cell_gpi}

    def read_applied(self,
                     *read_args,
                     params:list,
                     func:Callable=np.average,
                     func_kwargs=None,
                     name='merged',
                     **read_kwargs):
        """
        For a location combine the time series of multiple variables into
        a single time series using the passed numpy method applied to all arrays.

        Examples:
            GeoSmecvSwiRzsmTs.read_applied(45, 15, pd.mean, name='mean', func_kwargs={'axis': 1)
            GeoSmecvSwiRzsmTs.read_applied(45, 15, np.average, name='mean', func_kwargs={'axis': 1)

        Parameters
        ----------
        read_args, read_kwargs : passed to read(), gpi, lon, lat
        params : list[str]
            List of parameters that are merged (must be available for each location
        func : Callable, optional (default: np.average)
            Will be applied to dataframe columns using pd.DataFrame.apply(..., axis=1)
            additional kwargs for this must be given in func_kwargs
        method_kwargs : dict
            kwargs that are passed to method

        Returns
        -------
        df : pd.DataFrame
            Same as read but from multiple columns
        """
        func_kwargs = dict() if func_kwargs is None else func_kwargs
        func_kwargs['axis'] = 1

        df = self.read(*read_args, **read_kwargs)

        return df[params].apply(func, **func_kwargs).to_frame(name=name)



if __name__ == '__main__':
    path = "/shares/wpreimes/radar/Datapool/ESA_CCI_SM/02_processed/ESA_CCI_SM_v05.2/timeseries/combined/"
    dt_index = pd.date_range('2000-06-01', '2000-06-30', freq='D')

    ds = SmecvTs(path, grid=SMECV_Grid_v052(None), clip_dates=(dt_index[0], dt_index[-1]))

    params = ['sm',
              'flag',
              'dnflag',
              'freqbandID',
              'mode',
              'sensor',
              't0']

    param_fill_val = {'sm': -9999.,
                      'flag': 0,
                      'dnflag': 0,
                      'freqbandID': 0,
                      'mode': 0,
                      'sensor': 0,
                      't0': -9999.,
                      }

    param_dtype = {'adjusted': 'float32',
                   'flag': 'int8',
                   'dnflag': 'int8',
                   'freqbandID': 'int16',
                   'mode': 'int8',
                   'sensor': 'int16',
                   't0': 'float64',
                   }

    to_replace = {param: {np.nan: param_fill_val[param]} for param in params}


    celldata = ds.read_agg_cell_cube(2244,
                                     dt_index=dt_index,
                                     params=params,
                                     param_fill_val = param_fill_val,
                                     param_dtype=param_dtype,
                                     param_scalf=None,
                                     to_replace=to_replace,
                                     as_xr=True)

    celldata.to_netcdf(r"C:\Temp\delete_me\adjusted_ts2img\img\test.nc")