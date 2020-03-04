# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import pygeogrids as grids
import xarray as xr
import os
from datetime import datetime
from collections import OrderedDict
import shutil
import warnings

#TODO:
# (++) Make the time optional (now placeholder), in case only 1 time per image is saved
# (++) Make the time bands work, in case that image represents a time period
#             e.g. so that the results are stored for the period between 2 dates (e.g. for mean values over time)
#             netcdf4 has this option but I have not found a way to include it here.
# (+) Collect metadata from cell images and apply to global image
# (+) Speed up global image generation
# (+) Store data more efficiently (add image compression etc.)
# (--) Make the resolution variable, for saving irregular gridded data


class RegularGriddedCellData(object):
    # For saving data in cellfiles (for multiprocessing)
    def __init__(self, path, grid=None, times=None, time_bnds=None,
                 reference_time=datetime(1900, 1, 1, 0, 0),
                 resolution=(0.25, 0.25)):
        """
        Cell Data Class uses xarray to write dictionaries of data to specified GPIS.

        Parameters
        -------
        path : str
            Path to which the cell files are saved
        grid: regular grid, optional (default: None -> create one)
            Input regular grid on which the passed GPIs are, if not passed,
             we generate a regular grid with the passed resolution
        times: list, optional (default: None)
            Datetimes for which images are saved
        time_bnds : tuple, optional (default: None)
            NOT IMPLEMENTED
            Time boundaries, to use for each time. To not use boundaries pass
            None. First element are the boundary starts, second the ends.
        reference_time: datetime, optional (default: 1900-01-01 00:00)
            Reference for creating floats from datetimes
        resolution: tuple, optional (default: 0.25 * 0.25 Degree)
            Resolution of the regular grid (lat,lon)
        """

        self.cell_files_path = path
        if not os.path.exists(self.cell_files_path):
            os.makedirs(self.cell_files_path)

        self.times = times
        self.time_bnds = time_bnds

        if self.time_bnds is not None:
            raise NotImplementedError

        self.reference_date = reference_time

        self.global_grid = grids.genreg_grid(*resolution).to_cell_grid(5.)
        if not grid:
            self.grid = self.global_grid
        else:
            self.grid = grid

        self._reset()

    def _reset(self):
        """
        Clears data cache for the current cell
        """
        self.cell = None
        self.file = None
        self.df = None

    def _change_cell(self, cell):
        """
        Writes down the cache and loads data for a new cell (or creates) empty
        data in case cell file does not yet exist.
        """
        self.write()
        self.load_cell_df(cell)

    def load_cell_df(self, cell):
        """
        Load the netcdf file for the passed cell as pandas frame.
        If one already exists, this one is loaded, else one is created.

        Parameters
        ----------
        cell : int
            Cell number, the file with the same name is loaded
        type : str, optional
            'frame' to load as a pandas.DataFrame, 'xr' to load as xarray dataset

        Returns
        -------
        cell_data : pd.DataFrame
        """

        self.file = self._cell2ncpath(cell=cell)

        if os.path.isfile(self.file):
            dataset = xr.open_dataset(self.file)
            df = dataset.to_dataframe()
            df = df.reorder_levels(['time', 'lat', 'lon'])
            self.df = df.sort_index()
            dataset.close()
        else:
            self.df = self._new_cell_df(cell=cell)

        self.cell = cell

    def _new_cell_df(self, cell):
        """
        Create a pandas DataFrame with data for the passed cell in the grid

        Returns
        -------
        df : pandas.DataFrame
            DataFrame for the passed cell
        """

        gpis, lons, lats = self.grid.grid_points_for_cell(cell)

        df_concat = []
        for time in self.times:
            df = pd.DataFrame(data={'time': np.tile(time, lons.size),
                                    'lon': lons, 'lat': lats})
            df_concat.append(df)
        df = pd.concat(df_concat)
        df.set_index(['time', 'lat', 'lon'], inplace=True)
        return df.sort_index()

    def _cell2name(self, cell):
        """
        Create a netcdf file name in the current file path for the passe cell
        number

        Parameters
        ----------
        cell : int
            Cell number, the file name is equal to this number.

        Returns
        -------
        filename : str
            Path for the cell file for the passed cell
        """

        file_pattern = str(cell)
        while len(file_pattern) < 4:
            file_pattern = str(0) + file_pattern

        return os.path.join(self.cell_files_path, file_pattern + '.nc')

    def _cell2ncpath(self, gpi=None, cell=None):
        """
        Creates file path to the netcdf file that contains the passed point or
        cell.

        Parameters
        ----------
        gpi : int
            GPI for which the file path to the netcdf file is created
        cell : int
            Cell number for which the file path to the netcdf file is created.

        Returns
        -------
        filepath : str
            Path to the accoring netcdf file
        """

        if gpi and cell:
            if gpi not in self.grid.grid_points_for_cell(cell)[0]:
                raise ValueError(gpi, 'GPI is not in the passed cell')
            filepath = self._cell2name(cell)
        elif gpi is not None:
            cell = self.grid.gpi2cell(gpi)
            filepath = self._cell2name(cell)
        elif cell is not None:
            filepath = self._cell2name(cell)
        else:
            filepath = None

        return filepath

    def _write_xr(self):
        """
        Transform the current cell data (df) to a xarray dataset.

        Returns
        -------
        df_xr : xarray.Dataset

        """
        return self.df.to_xarray()

    def write(self):
        """
        Write the current cell data to a netcdf file.
        """
        if self.df is not None:
            dataset = self._write_xr()
            try:
                dataset.to_netcdf(self.file, engine='scipy',
                    encoding={var: {'complevel':6, 'zlib':True} for var in dataset.variables \
                              if var not in ['lat', 'lon', 'time']})
            except:
                dataset.to_netcdf(self.file, engine='scipy')

            dataset.close()
        else:
            return

    def check_pt_pos(self, gpi, lon, lat, cell):
        """
        Check if the passed values match with values from the grid.
        """
        cell_shd = self.grid.gpi2cell(gpi)
        lon_shd, lat_shd = self.grid.gpi2lonlat(gpi)

        assert cell == cell_shd
        assert lon == lon_shd
        assert lat == lat_shd

    def add_data(self, data, gpi=None, lonlat=(None, None), cell=None, time=None,
                 write_now=False):
        """
        Add data to the buffer. The buffer contains data for one cell. If the
        passed cell is not the same as the cell in the buffer, the buffer is written
        to file and the correct cell file is loaded/created.
        Therefore in terms of performance it makes sense to change the cell as
        rarely as possible (add data for all points for cell 1, add data for
        all points for cell 2,...(see example scripts))

        Parameters
        ----------
        data : dict
            Dictionary of variable names (keys) and according values (items)
        gpi : int, optional
            GPI for the data to store
            Either lonlat or gpi must be passed, or both
        lonlat : tuple, optional
            (Longitude, Latitude) for the data to store.
            Either lonlat or gpi must be passed, or both
        cell : int, optional
            Cell number for the data to store.
            If this is None in will be taken from the grid.
        time : datetime
            Time for the data to store, must be one of times from the init
        write_now : bool
            Write to a netcdf file after adding the data (slow).
        """

        if not data:
            data = {}

        lon, lat = lonlat[0], lonlat[1]
        if not lat or not lon:
            gpi = int(gpi)
            lon, lat = self.grid.gpi2lonlat(gpi)
        elif not gpi:
            gpi = self.grid.find_nearest_gpi(lon, lat)
        else:
            if lon and lat and gpi:
                pass
            else:
                raise ValueError('Pass a GPI and/or LonLat')

        if not cell:
            cell = self.grid.gpi2cell(gpi)
        else:
            cell = int(cell)

        # check this in case the user enters something wrong
        self.check_pt_pos(gpi, lon, lat, cell)

        if time not in self.times:
            raise ValueError('Time does not correspond to time in the definition')

        if (not self.cell) or (cell != self.cell):
            self._change_cell(cell)

        data['cell'] = int(cell)
        data['gpi'] = int(gpi)

        index = pd.MultiIndex.from_tuples([(time, lat, lon)], names=['time', 'lat', 'lon'])

        gpi_df = pd.DataFrame(index=index, data=data).sort_index()

        col_compare = np.in1d(gpi_df.columns.values, self.df.columns.values).tolist()
        if not all(col_compare):
            for col in gpi_df.columns.values:
                if col not in self.df.columns.values:
                    self.df[col] = np.nan

        self.df.loc[gpi_df.index, gpi_df.columns] = gpi_df.loc[gpi_df.index, :]

        if write_now:
            self.write()

    def _scan_cellfiles(self):
        """
        Looks for cells in the directory, that are also in the global grid

        Returns
        -------
        cells: list
            List of valid cells that were found
        """
        cells = []
        for filename in os.listdir(self.cell_files_path):
            try:
                cell = int(filename[0:4])
            except:
                continue
            if cell in self.global_grid.get_cells():
                cells.append(cell)
        return cells

    def empty_temp_files(self):
        """
        Deltes the content of the temporary storage, that contains the cell files
        that are merged into a global file.
        """
        files = os.listdir(self.cell_files_path)
        for file in files:
            os.remove(os.path.join(self.cell_files_path, file))
        os.rmdir(os.path.join(self.cell_files_path))

    def make_global_file(self, filepath=None, filename='global.nc', fill_nan=True,
                         mfdataset=False, keep_cell_files=False, drop_variables=None,
                         global_meta_dict=None, var_meta_dicts=None):
        """
        Merge all cell files in the cell files path to a global netcdf image file.
        TODO: There are many ways to do this, a more efficient way would be preferred.
        Parameters
        -------
        filepath : str, optional
            Path where the global file is saved to
        filename : str, optional
            Filename of the global file
        fill_nan: bool, optional
            Select True to merge only existing files without filling missing cells
            with NaNs.
            This may lead to anomalies in the merged rendered image if the AOI is
            incoherent but speed up process.
        mfdataset : bool, optional
            This is a faster version of the merging with an external library.
            Needs the tools package installed. Does not fill missing cells
        keep_cell_files : bool, optional
            Keep the cell files after merging, if this is set to False the cell
            files will be deleted after creating the global image.
        drop_variables: string or iterable, optional
            A variable or list of variables to exclude from being parsed from the
            dataset. This may be useful to drop variables with problems or
            inconsistent values.
        global_meta_dict : OrderedDict, optional
            Global (file) meta data
        var_meta_dicts : OrderedDict of OrderedDicts, optional
            Dictionary containing the variable as a key and a dictionary of
            metadata for the variable
        """

        # TODO: Add metadata from input
        if not filepath:
            filepath = os.path.join(self.cell_files_path)

        glob_file = os.path.join(filepath, filename)

        if mfdataset:
            cell_data = xr.open_mfdataset(os.path.join(self.cell_files_path, '*.nc'))
            cell_data.to_netcdf(glob_file)
        else:
            if len(os.listdir(self.cell_files_path)) == 0:
                return

            firstfile = os.listdir(self.cell_files_path)[0]
            variables = xr.open_dataset(os.path.join(self.cell_files_path, firstfile),
                                        drop_variables=drop_variables).variables.keys()
            if fill_nan:
                self.grid = self.global_grid
            else:
                self.grid = (self.global_grid).subgrid_from_cells(self._scan_cellfiles())

            global_data = None

            for i, cell in enumerate(self.grid.get_cells()):
                print(cell)
                cellfile = self._cell2ncpath(cell=cell)
                if os.path.isfile(cellfile):
                    cell_data = xr.open_dataset(cellfile,
                                                drop_variables=drop_variables)
                else:
                    self.load_cell_df(cell)
                    empty_cell_data = self.df
                    for var in variables:
                        if var not in empty_cell_data.index.names:
                            empty_cell_data[var] = np.nan
                    cell_data = empty_cell_data.to_xarray()

                if global_data is None:
                    global_data = cell_data
                else:
                    try:
                        global_data = xr.merge([global_data, cell_data])
                    except:
                        print('Could not merge file for cell %s to global file' % cell)

                    cell_data.close()

            if global_meta_dict is not None:
                if isinstance(global_meta_dict, dict):
                    global_meta_dict = OrderedDict(global_meta_dict)
                global_data = global_data.assign_attrs(global_meta_dict)

            if var_meta_dicts is not None:
                for varname, var_meta in var_meta_dicts.items():
                    if varname in global_data.variables:
                        if isinstance(var_meta, dict):
                            var_meta = OrderedDict(var_meta)
                        global_data[varname].attrs = var_meta

            try:
                global_data.to_netcdf(glob_file, mode='w', engine='scipy',
                    encoding={var: {'complevel':6, 'zlib':True} for var in global_data.variables \
                              if var not in ['lat', 'lon', 'time']})
            except:
                global_data.to_netcdf(glob_file, mode='w', engine='scipy')


        if not keep_cell_files:
            self.empty_temp_files()

        return


def test_random_adding(limit=None):
    """
    # add data randomly for multiple cells, this leads to opening and closing
    # the file and writing the buffer for each iteration, which is slow.
    """
    from smecv_grid.grid import SMECV_Grid_v042
    import sys

    grid = SMECV_Grid_v042()

    incells = [2137, 2173, 2209]
    if 'win' in sys.platform:
        path = os.path.join(r'C:\Temp\test_random_adding')
    else:
        path = os.path.join('/tmp', 'test_random_adding')

    times = pd.DatetimeIndex(start='2000-01-15', end='2000-03-15', freq='M')

    # dimensions
    celldata = RegularGriddedCellData(path, grid, [t for t in times])

    # create random gpi order
    gpis, lons, lats, cells = [], [], [], []
    for cell in incells:
        cgpis, clons, clats = grid.grid_points_for_cell(cell)
        ccells = [cell] * len(cgpis)
        gpis += cgpis.tolist()
        lons += clons.tolist()
        lats += clats.tolist()
        cells += ccells

    jobs = pd.DataFrame(data={'gpi': gpis, 'lon': lons, 'lat': lats, 'cell': cells})
    jobs = jobs.sample(frac=1)

    for i, (r, row) in enumerate(jobs.iterrows()):
        gpi, lon, lat, cell = int(row['gpi']), row['lon'], row['lat'], int(row['cell'])
        if limit and (i > limit):
            break
        for time in times:
            data_dict = {'var1': np.random.rand(1)[0],
                         'var2': np.random.rand(1)[0],
                         'var3': np.random.rand(1)[0]}

            celldata.add_data(data_dict, gpi=gpi, time=time, write_now=True)

    print('write global')
    var_meta = OrderedDict({'var1': OrderedDict({'var1a': '1', 'var1b': '2'})})
    global_meta = OrderedDict({'global': 'i am global'})
    celldata.make_global_file(global_meta_dict=global_meta, keep_cell_files=True,
                              var_meta_dicts=var_meta, fill_nan=False)


def test_ordered_adding(limit=None):
    """
    # add data per cell for each gpi, which is fast
    """
    from smecv_grid.grid import SMECV_Grid_v042
    import sys

    wn = True

    grid = SMECV_Grid_v042()

    cells = [2137, 2173, 2209, 2247, 2319, 1234, 2244]
    if 'win' in sys.platform:
        path = os.path.join(r'C:\Temp\test_ordered_adding')
    else:
        path = os.path.join('/tmp', 'test_ordered_adding')
    if os.path.exists(path): shutil.rmtree(path)

    times = pd.DatetimeIndex(start='2000-01-15', end='2000-03-15', freq='M')

    time_bnds_starts = pd.DatetimeIndex(start='2000-01-01', end='2000-03-01',
                                        freq='M')
    time_bnds_ends = pd.DatetimeIndex(start='2000-01-31', end='2000-03-31',
                                      freq='M')

    time_bnds = (time_bnds_starts, time_bnds_ends)

    # dimensions
    celldata = RegularGriddedCellData(path, grid, [t for t in times])

    for cell in cells:
        gpis, lons, lats = grid.grid_points_for_cell(cell)
        for i, gpi in enumerate(gpis):
            if limit and (i > limit):
                break
            for time in times:
                data_dict = {'var1': np.random.rand(1)[0],
                             'var2': np.random.rand(1)[0],
                             'var3': np.random.rand(1)[0],
                             'var4': np.random.rand(1)[0],
                             'var5': np.random.rand(1)[0],
                             'var6': np.random.rand(1)[0],
                             'var7': np.random.rand(1)[0],
                             'var8': np.random.rand(1)[0],
                             'var9': np.random.rand(1)[0],
                             'var10': np.random.rand(1)[0],
                             'var11': np.random.rand(1)[0],
                             'var12': np.random.rand(1)[0],
                             'var13': np.random.rand(1)[0],
                             'var14': np.random.rand(1)[0],
                             'var15': np.random.rand(1)[0],
                             'var16': np.random.rand(1)[0],
                             'var17': np.random.rand(1)[0]}

                celldata.add_data(data_dict, gpi=gpi, time=time)

        celldata.write()

    print('write global')
    var_meta = OrderedDict({'var1': OrderedDict({'var1a': '1', 'var1b': '2'})})
    global_meta = OrderedDict({'global': 'i am global'})

    celldata.make_global_file(global_meta_dict=global_meta, var_meta_dicts=var_meta,
                              keep_cell_files=True, fill_nan=False)


class ReadNcImg(object):
    def __init__(self, filepath, resxy=(0.25, 0.25), lat_var='lat', lon_var='lon',
                 z_var='time', cell_center_origin=True):
        """
        Wrapper Class for reading 2D images at a certain time stamp from an nc file

        Parameters
        ----------
        filepath : str
            Path to a file that contains the data to plot
        time : datetime.datetime
            Time to read the variable for or None if there is only 1 time.
        resxy : tuple or None
            X and Y resolution of the netcdf image
            If None is passed we assume that the data is on an irregular grid and
            make scatter plot maps instead of regular gridded maps (as for ISMN stations).
        lat_var : str, optional (default: 'lat')
            The name of the variable in the netcdf file that refers to the latitude
            of the observation.
        lon_var : str, optional (default: 'lon')
            The name of the variable in the netcdf file that refers to the longitude
            of the observation.
        z_var : str, optional (default: 'time')
            Name of the z dimension variable name in the netcdf file.
        cell_center_origin : bool, optional (default: True)
            Whether the origin of the point is in the middle of the pixel or not.
        """
        if resxy is None:
            self.irregular = True
        else:
            self.irregular = False
        self.cell_center_origin = cell_center_origin

        self.index_name = [lat_var, lon_var]
        self.z_var = z_var

        self.resxy = resxy

        self.filepath = filepath
        self.filename = os.path.basename(os.path.normpath(filepath))[:-3]
        self.parent_dir = os.path.abspath(os.path.join(filepath, os.pardir))
        self.ds = self._open()

        self.time = None
        self.df = None # will be done when needed

    def _grid(self):
        """
        Create a grid (gpis, lats, lons) with the selected resolution. This is
        used to store the data in a gridded fashion.
        """
        c = 2 if self.cell_center_origin else 1.
        lons = (np.arange(360 * int(1. / self.resxy[0])) * self.resxy[0]) - (180. - (self.resxy[0] / c))
        lats = (np.arange(180 * int(1. / self.resxy[1])) * self.resxy[1]) - (90. - (self.resxy[1] / c))
        gpis = np.array(range(0, int(180. * (1. / self.resxy[0]) * 360. * (1. / self.resxy[1]))))

        return gpis, lons, lats

    def _open(self):
        """
        Open a xarray dataset, if possible with scipy
        """
        try:
            ds = xr.open_dataset(self.filepath, engine='scipy')
        except TypeError:
            ds = xr.open_dataset(self.filepath)

        return ds

    def _load(self, ds, time):
        """
        Load data from the xarray dataset at a time stamp as a pandas data frame.
        """
        if time is not None:
            df_file = ds.sel({self.z_var : time}) \
                .to_dataframe() \
                .reset_index(inplace=False) \
                .set_index(self.index_name)
        else:
            df_file = ds.to_dataframe() \
                .reset_index(inplace=False) \
                .set_index(self.index_name)

        if not self.irregular:
            df_file = df_file.loc[df_file.index.dropna()]

        return df_file


    def read(self, time=None, vars=None):
        """
        Read one or multiple variables from the netcdf file to a data frame.
        If there are multiple dates in the file, a time must be passed.

        Parameters
        ----------
        time : datetime.datetime or str, optional (default: None)
            Time of the variable to read
        vars : list or str, optional (default: None)
            Name of the variable(s) to load from the file.
        """

        if isinstance(vars, str):
            vars = [vars]

        loaded_vars = []
        if time == self.time:
            if self.df is not None:
                if vars is not None:
                    if all([var in self.df.columns for var in vars]):
                        loaded_vars = vars  # all done
                    else:
                        loaded_vars = [var in self.df.columns for var in vars]
        else:
            self.clear()

        if not loaded_vars == vars:
            if time is None:
                try: # load as datetime
                    time = pd.to_datetime(self.ds.time.values[0])
                except ValueError:
                    try: # load as anything
                        time = self.ds.time.values[0]
                    except AttributeError:
                        time = None

            df_file = self._load(self.ds, time)

            if not df_file.index.is_unique:
                warnings.warn('Duplicate locations found in the loaded data. Continue as irregular data.')
                self.irregular = True


            if not self.irregular:
                gpis, lons, lats = self._grid()
                lons, lats = np.meshgrid(lons, lats)

                df = pd.DataFrame(index=None, data={'gpi': gpis,
                                                    'lat': lats.flatten(),
                                                    'lon': lons.flatten()})
                df = df.set_index(self.index_name)

                if vars is None:
                    df = pd.DataFrame(index=df.index, data=df_file)
                else:
                    vars_to_load = [var for var in vars if var not in loaded_vars]
                    for var in vars_to_load:
                        df[var] = df_file[var]
            else:
                df = df_file

                if vars is not None:
                    df = df.drop(columns=[var for var in df.columns if var not in vars])

            self.df = df
            self.time = time
        else:
            print('Data is already loaded. Use data in memory.')

        return self.df

    def clear(self):
        self.df_lc = None
        self.df = None
        self.time = None


    def filter_with_grid(self, grid, fillna=False):
        """
        Reduce to loaded data to points of the passed grid. The resolution and
        locations have to match.

        Parameters
        ----------
        grid : pygeogrids.CellGrid
            The grid that is used to reduce the loaded data.
        fillna : bool, optional (default: False)
            Fill values in the global data frame that are excluded with nans,
            otherwise they are dropped.

        Returns
        -------
        filtered_df : pd.DataFrame
            The loaded df, but filtered to the passed grid.
        """
        gpis, lons, lats, cells = grid.get_grid_points()
        subset_index = pd.MultiIndex.from_arrays([lats, lons], names=['lat', 'lon'])

        df = self.df.copy(True)

        df_filtered = df.loc[subset_index, :]
        if fillna:
            df = pd.DataFrame(index=df.index, data={col:np.nan for col in df.columns})
            df.loc[df_filtered.index] = df_filtered
        else:
            df = df_filtered

        return df

if __name__ == '__main__':
    infile = r"\\?\C:\Temp\nc_compress\test1_with_test2.nc"
    ds = ReadNcImg(filepath=infile)
    ds.read(time=None, vars='n_obs')