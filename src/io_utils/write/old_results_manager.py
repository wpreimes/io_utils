# -*- coding: utf-8 -*-

'''
The results manager stores validation results as netcdf files.
'''

import os
import netCDF4

from datetime import datetime
import pandas as pd
import numpy as np
import warnings
from collections import OrderedDict
import xarray as xr
import ntpath
import copy


def compress_nc(infile, replace=True, dtypes=np.float32):
    """
    Compress a target netcdf file

    Parameters
    ----------
    infile : str
        Path to the target netcdf file
    replace : bool, optional (default: True)
        Overwrite the input file with the compressed one.
    """
    ds = xr.open_dataset(infile)

    path = os.path.abspath(os.path.join(infile, os.pardir))
    filename = ntpath.basename(infile)
    outfile = os.path.join(path, 'compressed_' + filename)

    ds.to_netcdf(outfile, mode='w',
                 encoding={var: {'complevel': 9, 'zlib': True, 'dtype': dtypes}
                           for var in ds.variables \
                           if var not in ['lat', 'lon', 'time']})
    ds.close()
    if replace:
        os.remove(infile)
        os.rename(outfile, infile)


def build_filename(root, key):
    """
    Create savepath/filename that does not exceed 255 characters
    Parameters
    ----------
    root : str
        Directory where the file should be stored
    key : list of tuples
        The keys are joined to create a filename from them. If the length of the
        joined keys is too long we shorten it.
    Returns
    -------
    fname : str
        Full path to the netcdf file to store
    """
    ds_names = []
    for ds in key:
        if isinstance(ds, tuple):
            ds_names.append('.'.join(ds))
        else:
            ds_names.append(ds)

    fname = '_with_'.join(ds_names)
    ext = 'nc'

    if len(os.path.join(root, '.'.join([fname, ext]))) > 255:
        ds_names = [str(ds[0]) for ds in key]
        fname = '_with_'.join(ds_names)

        if len(os.path.join(root, '.'.join([fname, ext]))) > 255:
            fname = 'validation'

    return os.path.join(root, '.'.join([fname, ext]))


def netcdf_results_manager(results, save_path, filename=None, zlib=True, fv=99999):
    """
    Function for writing the results of the validation process as NetCDF file.

    Parameters
    ----------
    results : dict of dicts
        Keys: Combinations of (referenceDataset.column, otherDataset.column)
        Values: dict containing the results from metric_calculator
    save_path : str
        Path where the file/files will be saved.
    filename : str, optional (default: None)
        Name of the file under which the results are stored. If this is None,
        we build a filename from the keys of results.
    zlib : bool, optional (default: True)
        Activate netcdf compression (level 6 of 9).
    """
    for key in results.keys():
        if not filename:
            fname = build_filename(save_path, key)
        else:
            fname = filename
        filename = os.path.join(save_path, fname)
        if not os.path.exists(filename):
            ncfile = netCDF4.Dataset(filename, 'w')

            global_attr = {}
            s = "%Y-%m-%d %H:%M:%NcRegGridStack"
            global_attr['date_created'] = datetime.now().strftime(s)
            ncfile.setncatts(global_attr)

            ncfile.createDimension('dim', None)
        else:
            ncfile = netCDF4.Dataset(filename, 'a')

        index = len(ncfile.dimensions['dim'])
        for field in results[key]:

            if field in ncfile.variables.keys():
                var = ncfile.variables[field]
            else:
                var_type = results[key][field].dtype
                kwargs = {'fill_value': fv}
                # if dtype is a object the assumption is that the data is a
                # string
                if var_type == object:
                    var_type = str
                    kwargs = {}

                if zlib:
                    kwargs['zlib'] = True,
                    kwargs['complevel'] = 6

                var = ncfile.createVariable(field, var_type,
                                            'dim', **kwargs)
            var[index:] = results[key][field]

        ncfile.close()


class Results(object):
    # todo: use arrays instead of dataframes to speed things up?
    def __init__(self, lon_name='lon', lat_name='lat', z_name='time'):
        """
        Parameters
        ----------
        lon_name : str, optional (default: 'lon')
            Name, under which the longitude values will be stored.
        lat_name : str, optional (default: 'lat')
            Name, under which the latitude values will be stored.
        z_name : str, optional (default: 'time')
            Name of the third dimension, if values are passed in z.
        z: np.array, optional (default: None)
            Values that create the third dimension, e.g. a list of time stamps.
        """
        self.data = None # dataframe or dict of dataframes
        self.z_name = z_name
        self.z = None # True or False, indicates if 2d or 3d
        self.__lonlat = (lon_name, lat_name)
        self.__glob_attrs = None
        self.__var_attrs = None

    def _add_empty(self, z):
        # only for 3d
        assert self.z == True
        if self.data is None:
            self.data = {}
        self.data[z] = pd.DataFrame()

    def _df4z(self, z):
        assert self.z == True
        return self.data[z]

    def _hasz(self, z):
        return z in self.data.keys()

    @property
    def shape(self):
        return (len(data), [df.index.size for df in self.data],
                [df.index.nlevels for df in self.data])

    @property
    def lon_name(self):
        return self.__lonlat[0]

    @property
    def lat_name(self):
        return self.__lonlat[1]

    @property
    def glob_attrs(self):
        return self.__glob_attrs

    @property
    def var_attrs(self):
        return self.__var_attrs

    @glob_attrs.setter
    def glob_attrs(self, attrs, ):
        """
        Set the global attributes (global metadata.

        Parameters
        ----------
        attrs : dict
        """
        s = "%Y-%m-%d %H:%M:%NcRegGridStack"
        attrs['date_created'] = datetime.now().strftime(s)
        self.__glob_attrs = attrs

    @var_attrs.setter
    def var_attrs(self, attrs):
        """
        Set the variable attributes (var metadata)

        Parameters
        ----------
        attrs : dict of dicts
        """
        self.__var_attrs = attrs

    def _assert_shape_2D(self, lons, lats, data, n_times=None):
        """
        Check if the size of the passed data is ok.

        Parameters
        ----------
        lons : np.array
            Lons array
        lats : np.array
            Lats array
        data : dict
            Data arrays in dict with variable names as keys
        n_times : int (optional, default: None)
            Time dimension size
        """
        if not (lats.shape == lons.shape):
            raise IOError('2D Lat and Lon shapes do not match ({} vs. {})'
                          .format(lat.shape, lon.shape))
        else:
            lonlat_shape = lats.shape

        for k, v in data.items():
            if n_times is not None:
                if not (v.shape[0] == n_times):
                    raise IOError('2D Variable {} in data has different shape than time. ({} vs. {})'.
                                  format(k, v.shape[2], n_times))
            if v.shape[1:] != lonlat_shape:
                raise IOError('2D Variable {} in data has different shape than lat/lon. ({} vs. {})'.
                              format(k, v.shape, lonlat_shape))

    def _2d_index(self, lons, lats):
        # lons : np.array all longitudes (same length as lats)
        # lats : np.array, all latitudes (same length as lons)
        # timestamps : np.array, timestamps
        row_index_arrs = (lons, lats)
        row_index_names = (self.lon_name, self.lat_name)
        return pd.MultiIndex.from_arrays(row_index_arrs, names=row_index_names)

    def _assert_shape_1D(self, lons, lats, data, n_times=None):
        if not (lats.size == lons.size):
            raise IOError('1D Lat and Lon sizes do not match ({} vs. {})'.format(lat.size, lon.size))
        else:
            lonlat_size = lats.size

        for k, v in data.items():
            if n_times is not None:
                if not (v.shape[0] == n_times):
                    raise IOError('1D Variable {} in data has different shape than time. ({} vs. {})'.
                                  format(k, v.shape[0], n_times))
            if v.shape[1] != lonlat_size:
                raise IOError('1D Variable {} in data has different shape than lat/lon. ({} vs. {})'.
                              format(k, v.size, lonlat_size))

    def add_data_nd(self, lons, lats, data, z=None):
        if z is not None:
            if self.z == False:
                raise IOError('Cannot add data without third dimension after initialising '
                              'object with {}'.format(self.z))
            elif self.z is None:
                self.z = True
            assert self.z == True
            self._assert_shape_2D(lons, lats, data, len(z))
            dim_arrs = (z, lats, lons)
            dim_names = (self.z_name, self.lat_name, self.lon_name)
        else:
            if self.z == True:
                raise IOError('Cannot add 3d data (with z values) after initialising object without z dimension')
            elif self.z is None:
                self.z =False
            assert self.z == False
            self._assert_shape_2D(lons, lats, data, None)
            dim_arrs = (lats, lons)
            dim_names = (self.lat_name, self.lon_name)

        index = pd.MultiIndex.from_arrays(dim_arrs, names=dim_names)
        df = pd.DataFrame(index=index, data={n: v for n, v in data.items()})
        self.data = pd.concat([self.data, df], axis=0)

    def _add_list_no_z(self, lons, lats, data):
        """
        Add data to the current image.

        Parameters
        ----------
        lons : np.array (1d)
            Same lengths as lats
        lats : np.array (1d)
            Same length as lons
        data : dict
            Values are 1d arrays with same size as lons/lats
        """
        if self.z == True:
            raise IOError('Cannot add 2d data (without z values) after initialising '
                          'object with third dimension.')
        elif self.z is None:
            self.z = False

        assert self.z == False # always

        self._assert_shape_1D(lons, lats, data, None)

        df = pd.DataFrame(index=self._2d_index(lons, lats), data=data)

        self.data = pd.concat([self.data, df], axis=0)

    def _add_list_z(self, lons, lats, data, z):
        if self.z == False:
            raise IOError('Cannot add 3d data (without z values) after initialising '
                          'object without third dimension.')
        elif self.z is None:
            self.z = True

        assert self.z == True  # always

        self._assert_shape_1D(lons, lats, data, len(z))

        df = pd.DataFrame(index=self._2d_index(lons, lats), data=data)

        self.data = pd.concat([self.data, df], axis=0)

    def _add_arr_no_z(self, lons, lats, data):
        """
        Add data in array shape, without a thir dimension

        Parameters
        ----------
        lons : np.array
            2d array (grid) that represents the locations of data
        lats : np.array
            2d array (grid) that represents the locations of data
        data : dict
            Dict of 2d arrays the contain the data.

        Returns
        -------

        """
        assert lons.shape == lat.shape
        lonlat_shape = lons.shape
        for d, v in data.items():
            assert v.shape == lonlat_shape
        pass # check and add data


    def add_data_1d(self, lons, lats, data, z=None):
        """
        Add results to the data frame

        Parameters
        ----------
        lons : np.array
            Longitudes of values in vals
        lats : np.array
            Latitudes of vals
        data : dict
            Keys are the variable names and vals are arrays (of same size as
            lats and lons) of according values.
        zs: np.array
            Array of values over the third dimension for the cube, e.g
            datetimes or depths or heights. Or None to store 2d data.
        """
        if z is not None:
            if self.z == False:
                raise IOError('Cannot add data without third dimension after '
                              'initialising object with time')
            elif self.z is None:
                self.z = True
            assert self.z == True
            self._assert_shape_1D(lons, lats, data, len(z))

            for z in zs:
                if not self._hasz(z):
                    self._add_empty([z])
                df = pd.DataFrame(index=self._2d_index(lons, lats), data=data)
            # time_cols = np.array(np.meshgrid(z, np.array(list(data.keys()))))\
            #     .T.reshape(-1, len(z))
            # col_index = pd.MultiIndex.from_tuples(tuple(map(tuple, time_cols)),
            #                                       names=[self.z_name, 'variables'])
            # iterables = ()
            # row_index_arrs = tuple([i for i in z]) + (lats*len(z), lons*len(z))
            # row_index_names = (self.z_name, self.lat_name, self.lon_name)


        else:
            if self.z == True:
                raise IOError('Cannot add 3d data (with z values) after initialising object without time')
            elif self.z is None:
                self.z =False
            assert self.z == False
            self._assert_shape_1D(lons, lats, data, None)
            # col_index = list(data.keys())
            row_index_arrs = (lats, lons)
            row_index_names = (self.lat_name, self.lon_name)

        row_index = pd.MultiIndex.from_arrays(row_index_arrs, names=row_index_names)
        df = pd.DataFrame(index=row_index_arrs)
        # row_index = pd.MultiIndex.from_arrays(row_index_arrs, names=row_index_names)
        # df = pd.DataFrame(index=row_index, columns=col_index)
        #
        # if z is not None:
        #     for k, v in data.items():
        #         for i, t in enumerate(z):
        #             df[t, k] = v[i]
        # else:
        #     for k, v in data.items():
        #         df[k] = v

        self.data = pd.concat([self.data, df], axis=0)

    def to_xarray(self):
        """
        Convert the stored information to a xarray dataset.

        Returns
        -------
        ds : xr.dataset
            The xarray image, with a lat and lon dimension and variables and
            according metadata.
        """
        # build the empty xarray dataset
        # iterate over all times in dataframe
        # fill the dataset over the time dimension
        pass

        # coords = {self.lon_name: self.data.index.get_level_values(self.lon_name).values,
        #           self.lat_name: self.data.index.get_level_values(self.lat_name).values}
        # if self.z is not None:
        #     coords[self.z_name] = np.unique(self.data.columns.get_level_values(self.z_name))
        # xr.Dataset(coords=coords)
        # if self.z is not None:
        #     dss = [self.data]
        #     coords = [self.data.index
        #     coords = [self., self.lat_name, self.time_name]
        #     xr.Dataset(data=self.data, coords=,
        #                dims=[self.lon_name, self.lat_name, self.z_name])
        # else:
        #     xr.Dataset(data=self.data, coords=[slef.])
        # ds = self.data.to_xarray()
        #
        # if self.var_attrs:
        #     ds = ds.assign_attrs(self.glob_attrs)
        #
        # if self.var_attrs:
        #     for n, d in self.var_attrs.items():
        #         if n in ds.variables:
        #             if isinstance(d, dict):
        #                 d = OrderedDict(d)
        #             ds[n].attrs = d
        #
        # return ds


class NcResultsManager(object):
    """
    Stores validation results on a regular or irregular grid.
    """

    """
    It should:

        - Be opened and closed via 'with' and via 'close()'
        - It should allow storing results for multiple points in time and/or
            multiple depths
        - Contain a buffer that is filled and dumped into a nc file when full,
            then emptied and filled again, then merged with data in file, dumpted etc.
        - Allow setting metadata for global attributes and variable attributes
        - Allow compression of results
        - 

    """

    def __init__(self, save_path, zlib=True, force_points=False,
                 buffr_size=None):
        '''
        Create a data frame from the jobs.
        Add options for compression and for buffer storing?
        Parameters
        -------
        save_path : str
            Root folder where we store the results.
        zlib : bool, optional (default: True)
            Activate compression of all results.
        force_points : bool, optional (default: False)
            By default, we try to store the results in a grid, only if there a
            duplicate locations, we fall back to a (less efficient) point format.
            If this is True, the point format is always used (not recommended
            for global validations with satellite data).
        buffr_size : int, optional (default: None)
            Write the results down if after this many points are stored in the buffer.
            If buffr_size is None, then the buffer will only be written upon
            __exit__().
        '''
        self.save_path = save_path
        self.zlib = zlib
        self.ncformat = 'point' if force_points else None
        self.buffr_size = buffr_size

        # data storage
        self.res = dict()  # names and dataframes that will become files

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print('exc_type: {}'.format(exc_type))
            print('exc_value: {}'.format(exc_val))
            print('exc_traceback: {}'.format(exc_tb))

        self.close()
        return True

    def get_buffer_size(self):
        return [self.res[k].index.size for k in self.res.keys()]

    def close(self):
        self._to_netcdf()

    def _add_empty(self, name, lon_name, lat_name):
        self.res[name] = Results(lon_name, lat_name)

    # def add_dict(self, data, lon_name='lon', lat_name='lat'):
    #     for name, result in data.items():
    #         self.add(name, result, lon_name=lon_name, lat_name=lat_name)

    def add(self, name, data, times=None, lon_name='lon', lat_name='lat'):
        """
        Add results from dictionary to buffer

        Parameters
        ---------
        name : str or tuple
            The name if the dataset (as in self.dfs)
        data : dict
            Keys are variable names (e.g. gpi, lon, lat, etc.), values are arrays
            (of same length) with according values
        time_name : np.array of datetimes, optional (default: None)
            For each array in data[var], time must have one value.
        lon_name : str, optional (default: 'lon')
            The name of the longitude variable in data
        lat_name : str, optional (default: 'lat')
            The name of the latitude variable in data
        """
        if lon_name not in data.keys():
            raise IOError('Data must contain Longitude Dimension data named {}'.
                          format(lon_name))
        if lat_name not in data.keys():
            raise IOError('Data must contain Latitude Dimension data named {}'.
                          format(lat_name))

        lons = data[lon_name]
        lats = data[lat_name]

        dim_lon = len(lons.shape)
        dim_lat = len(lats.shape)

        if dim_lat != dim_lon:
            raise IOError('Latitude/Longitude dimensions do not match')
        else:
            dim = dim_lat

        if name not in self.res.keys():
            self._add_empty(name, lon_name, lat_name)

        dat = copy.deepcopy(data)

        dat.pop(lon_name)
        dat.pop(lat_name)

        if dim == 1:
            self.res[name].add_data_1d(lons, lats, dat, times)
        elif dim == 2:
            self.res[name].add_data_2d(lons, lats, dat, times)
        else:
            raise IOError('Found dat dimension {}, which is not supported'.format(dim))

        print('Buffer size after adding data: {}'.format(self.get_buffer_size()))

        # todo: check buffer and write down
        #if self.res[name] > self.buffr_size:


    def set_attrs(self, name, glob_attrs, var_attrs):
        """
        Set the global attributes of the respective file.

        Parameters
        ----------
        name : str or tuple
            Name of the dataset for which the attributes are set.
        glob_attrs : dict
            Dictionary of global attributes (keys) and their values
        var_attrs : dict of dicts
            Dictionary of variable and the attributes
        """
        self.res[name].glob_attrs = glob_attrs
        self.res[name].var_attrs = var_attrs

    def _to_netcdf(self, filename=None, fill_value=-9999., dtypes=np.float32):
        """
        Write the data from memory to disk as a netcdf file.
        """
        for name, r in self.res.items():
            if filename is None:
                if not isinstance(name, str):
                    build_fname = True
                else:
                    build_fname = False

                if build_fname:
                    filename = build_filename(self.save_path, name)
                else:
                    filename = os.path.join(self.save_path, name + '.nc')

            if self.ncformat == 'point':
                data = {}
                for col in r.data:
                    data[col] = r.data[col].values
                data['lat'] = r.data.index.get_level_values('lat').values
                data['lon'] = r.data.index.get_level_values('lon').values
                data = {name: data}
                netcdf_results_manager(data, self.save_path, filename=filename,
                                       zlib=self.zlib)
            else:
                try:
                    dataset = r.to_xarray()
                    try:
                        if self.zlib:
                            encoding = {}
                            for var in dataset.variables:
                                if var not in [r.lat_name, r.lon_name, 'time']:
                                    dataset.variables[var][:] = \
                                        dtypes(dataset.variables[var].fillna(fill_value))
                                    encoding[var] = {'complevel': 9, 'zlib': True,
                                                     '_FillValue': fill_value}
                        else:
                            encoding = None
                        dataset.to_netcdf(filename, engine='netcdf4', encoding=encoding)
                    except:  # todo: specifiy exception
                        warnings.warn('Compression failed, store uncompressed results.')
                        dataset.to_netcdf(filename, engine='netcdf4')

                    dataset.close()
                except:  # todo: specify exception?
                    self.ncformat = 'point'
                    self._to_netcdf()


if __name__ == '__main__':
    path = r'C:\Temp\test_compress'

    writer = NcResultsManager(save_path=path, zlib=True, buffr_size=None, force_points=None)

    gpis = np.array(list(range(1, 20)))
    lat = np.array(list(range(30, 30 + len(gpis), 1)))
    lat2 = np.array(list(range(-30, -30 + len(gpis), 1)))
    lon = np.array(list(range(-119, -119 + len(gpis), 1)))
    lon2 = np.array(list(range(119, 119 + len(gpis), 1)))
    n_obs = np.array([np.random.randint(0, 1000, len(gpis)), np.random.randint(0, 1000, len(gpis))])
    data = np.array([np.array([1] * len(gpis)), np.array([1] * len(gpis))])
    empty = np.array([np.array([np.nan] * len(gpis)),  np.array([np.nan] * len(gpis))])
    times = np.array([np.array([datetime(2000,1,1)] * len(gpis)),
                      np.array([datetime(2002,1,1)] * len(gpis))])
    # s = np.array(['s%i' %i for i in gpis])
    n = np.array([np.random.random_sample(len(lon)),np.random.random_sample(len(lon))])

    results = {('test1', 'test2'):
                   dict(lat=lat, lon=lon, n_obs=n_obs, n=n, data=data, empty=empty)}

    results2 = {('test1', 'test2'):
                    dict(lat=lat, lon=lon2, n_obs=n_obs, n=n, data=data, empty=empty)}

    results3 = {('test1', 'test2'):
                    dict(lat=lat2, lon=lon, n_obs=n_obs, n=n, data=data, empty=empty)}

    for name, result in results.items():
        writer.add(name, result, times=times)
    for name, result in results2.items():
        writer.add(name, result, times=times)
    for name, result in results3.items():
        writer.add(name, result, times=times)

    writer.close()

    # one = r"\\project10\data-write\USERS\wpreimes\C3S_Prod_Intercomparison\with_ERA5\global\out\joined.nc"
    # other = r"\\project10\data-write\USERS\wpreimes\C3S_Prod_Intercomparison\with_ERA5\global\out\third.nc"
    # out_file = r"\\project10\data-write\USERS\wpreimes\C3S_Prod_Intercomparison\with_ERA5\global\out\global.nc"
    # ds1 = xr.open_dataset(one)
    # df1 = ds1.to_dataframe().dropna(how='all')
    # ds2 = xr.open_dataset(other)
    # df2 = ds2.to_dataframe().dropna(how='all')
    # df = df1.append(df2, sort=False)
    # df.drop_duplicates().to_xarray().to_netcdf(out_file, mode='w', engine='scipy')

    # gpis = np.array(list(range(1,10)))
    # lat = np.array(list(range(30,30+len(gpis),1)))
    # lon = np.array(list(range(-119,-119+len(gpis),1)))
    # n_obs = np.random.randint(0,1000,len(gpis))
    # s = np.array(['s%i' %i for i in gpis])
    # n = np.random.random_sample(len(lon))
    #
    #
    # results = {('test1','test2') :
    #                dict(lat=lat, lon=lon, gpi=gpis, n_obs=n_obs, s=s, n=n)}
    #
    # path = r'C:\Temp\nc_compress'
    #
    # var_attrs = {'n_obs': {'name':'Number of Observations', 'smthg_else':1}}
    # glob_attrs = {'test1':'test', 'test2': 'test'}
    #
