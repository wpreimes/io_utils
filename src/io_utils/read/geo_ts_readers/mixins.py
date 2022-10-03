import warnings
import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import netCDF4 as nc
from pygeogrids.grids import CellGrid
import xarray as xr

class ContiguousRaggedTsCellReaderMixin:

    """
    Adds functionality to read whole cells. Can be added to time series
    readers that use the cell file structure of pynetcf.
    """

    path: str
    grid: CellGrid

    def read_cell_file(self, cell, param='sm', fill_value=None):
        """
        Reads a single variable for all points of a cell.

        Parameters
        ----------
        cell: int
            Cell number, will look for a file <cell>.nc that must exist.
            The file must contain a variable `location_id` and `time`.
            Time must have an attribute of form '<unit> since <refdate>'
        param: str, optional (default: 'sm')
            Variable to extract from files
        fill_value: float or int, optional (default: None)
            Value to use for gaps, None uses fill value from file

        Returns
        -------
        df: pd.DataFrame
            A data frame holding all data for the cell.
        """

        try:
            fnformat = getattr(self, 'fn_format') + '.nc'
        except AttributeError:
            fnformat = "{:04d}.nc"

        file_path = os.path.join(self.path, fnformat.format(cell))

        with nc.Dataset(file_path) as ncfile:
            loc_id = ncfile.variables['location_id'][:]
            loc_id = loc_id[~loc_id.mask].data.flatten()
            row_size = ncfile.variables['row_size'][:]
            row_size = row_size[~row_size.mask].data

            time = ncfile.variables['time'][:].data
            unit_time = ncfile.variables['time'].units
            variable = ncfile.variables[param][:]
            if fill_value is None:
                fill_value = variable.fill_value
            variable = variable.filled(fill_value)

        if fill_value is None:
            fill_value = np.nan

        cutoff_points = np.cumsum(row_size)
        index = np.sort(np.unique(time))
        times = np.split(time, cutoff_points)[:-1]
        datas = np.split(variable, cutoff_points)[:-1]

        assert len(times) == len(datas)

        filled = np.full((len(datas), len(index)), fill_value=fill_value)
        idx = np.array([np.isin(index, t) for t in times])
        filled[idx] = variable

        delta = lambda t: timedelta(t)
        vfunc = np.vectorize(delta)
        since = pd.Timestamp(unit_time.split('since ')[1])
        index = since + vfunc(index)

        filled = np.transpose(np.array(filled))

        data = pd.DataFrame(index=index, data=filled, columns=loc_id)

        if hasattr(self, 'clip_dates') and self.clip_dates:
            if hasattr(self, '_clip_dates'):
                data = self._clip_dates(data)
            else:
                warnings.warn("No method `_clip_dates` found.")

        return data

    def read_agg_cell_data(self, cell, param, format='pd_multidx_df',
                           to_replace=None) -> dict or pd.DataFrame:
        """
        Read all time series for a single variable in the selected cell.

        Parameters
        ----------
        cell: int
            Cell number as in the c3s grid
        param: list or str
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
        if hasattr(self, 'exact_index') and self.exact_index:
            warnings.warn("Reading cell with exact index not yet supported. "
                          "Use read_cells()")

        params = np.atleast_1d(param)

        df = []
        for p in params:
            _df = self.read_cell_file(cell, p)
            idx = pd.MultiIndex.from_product([_df.columns.values, _df.index.values],
                                             names=['locations', 'time'])
            data = _df.transpose().values.flatten()
            _df = pd.DataFrame(index=idx, data={p: data})
            df.append(_df)

        df = pd.concat(df, axis=1)

        locations = df.index.get_level_values('locations').values
        gpis = np.unique(locations)

        df.index = df.index.set_levels(np.arange(len(gpis)), level=0)

        if hasattr(self, 'clip_dates') and self.clip_dates:
            if hasattr(self, '_clip_dates'):
                df = self._clip_dates(df)
            else:
                warnings.warn("No method `_clip_dates` found.")

        if to_replace is not None:
            df = df.replace(to_replace=to_replace)

        if format.lower() == 'pd_multidx_df':
            index = df.index.set_levels(gpis, level=0) \
                .set_names('gpi', level=0)
            data = df.set_index(index)

        elif format.lower() == 'gpidict':
            if 'gpi' not in df.columns:
                df['gpi'] = locations
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


class OrthoMultiTsCellReaderMixin:
    """
    Adds functionality to read whole cells. Can be added to time series
    readers that use the cell file structure of pynetcf.
    """

    path: str
    grid: CellGrid

    def read_cell_file(self, cell, param='sm'):
        """
        Reads a single variable for all points of a cell.

        Parameters
        ----------
        cell: int
            Cell number, will look for a file <cell>.nc that must exist.
            The file must contain a variable `location_id` and `time`.
            Time must have an attribute of form '<unit> since <refdate>'
        param: str, optional (default: 'sm')
            Variable to extract from files

        Returns
        -------
        df: pd.DataFrame
            A data frame holding all data for the cell.
        """

        try:
            fnformat = getattr(self, 'fn_format') + '.nc'
        except AttributeError:
            fnformat = "{:04d}.nc"

        file_path = os.path.join(self.path, fnformat.format(cell))

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

        if hasattr(self, 'clip_dates') and self.clip_dates:
            if hasattr(self, '_clip_dates'):
                data = self._clip_dates(data)
            else:
                warnings.warn("No method `_clip_dates` found.")

        return data

    def read_cells(self, cells, param=None):
        """
        Read all data for one or multiple cells as a data frame.
        Can read multiple parameters at once, and will return a dataframe
        with a MultiIndex as columns.
        This will iterate over each point in each cell. So it is much slower
        than the `read_cell_file` function!

        Parameters:
        -----------
        cells: int or np.ndarray
            a list of cells to read.
        params: list or str, optional (default: None)
            Parameter(s) to read from the file.
            If None are passed, all are selected.
        """
        cell_data = []
        gpis, lons, lats = self.grid.grid_points_for_cell(list(cells))
        for gpi, lon, lat in zip(gpis, lons, lats):
            df = self.read(lon, lat)
            if param is not None:
                df = df[np.atleast_1d(param)]
            df.columns = pd.MultiIndex.from_tuples((gpi, c) for c in df.columns)
            if not df.empty:
                cell_data.append(df)

        if len(cell_data) == 0:
            return pd.DataFrame()
        else:
            axis = 0
            # if hasattr(self, 'exact_index') and self.exact_index:
            #     axis = 1

            return pd.concat(cell_data, axis=axis)

    def read_agg_cell_data(self, cell, param, format='pd_multidx_df',
                           drop_coord_vars=True, to_replace=None,
                           **kwargs) -> dict or pd.DataFrame:
        """
        Read all time series for a single variable in the selected cell.

        Parameters
        ----------
        cell: int
            Cell number as in the c3s grid
        param: list or str
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
        if hasattr(self, 'exact_index') and self.exact_index:
            warnings.warn("Reading cell with exact index not yet supported. "
                          "Use read_cells()")

        try:
            fnformat = getattr(self, 'fn_format') + '.nc'
        except AttributeError:
            fnformat = "{:04d}.nc"

        file_path = os.path.join(self.path, fnformat.format(cell))

        params = np.atleast_1d(param)

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

        if hasattr(self, 'clip_dates') and self.clip_dates:
            if hasattr(self, '_clip_dates'):
                df = self._clip_dates(df)
            else:
                warnings.warn("No method `_clip_dates` found.")

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

