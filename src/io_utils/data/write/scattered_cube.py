# -*- coding: utf-8 -*-

"""
Module description
"""
# TODO:
#   (+) Write a class for this
#---------
# NOTES:
#   -

# -*- coding: utf-8 -*-

"""
The results manager stores validation results in netcdf format.
"""

import os
import netCDF4
from datetime import datetime
import xarray as xr
import numpy as np
import copy
import warnings
import pandas as pd
from netCDF4 import Dataset

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

def netcdf_results_manager(results, fname, save_path, global_attr={}, zlib=True):
    """
    Function for writing the results of the validation process as NetCDF file.

    Parameters
    ----------
    results : dict of dicts
        Keys: Combinations of (referenceDataset.column, otherDataset.column)
        Values: dict containing the results from metric_calculator
    save_path : string
        Path where the file/files will be saved.
    global_attr : dict
        Global attributes
    """
    for key in results.keys():
        filename = os.path.join(save_path, fname)
        if not os.path.exists(filename):
            ncfile = netCDF4.Dataset(filename, 'w')

            s = "%Y-%m-%d %H:%M:%S"
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
                kwargs = {'fill_value': -99999}
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


class NcScatteredStack(object):

    """ Store netcdf cube of ungridded data """

    _loc_id_attr = {'long_name': 'location_id'}

    _lon_attr = {'standard_name': 'longitude',
                'long_name': 'location longitude',
                'units': 'degrees_east',
                'valid_range': (-180.0, 180.0)}

    _lat_attr = {'standard_name': 'latitude',
                'long_name': 'location latitude',
                'units': 'degrees_north', 'valid_range': (-90.0, 90.0)}

    _alt_attr = {'standard_name': 'height',
                'long_name': 'vertical distance above the surface',
                'units': 'm', 'positive': 'up', 'axis': 'Z'}

    def __init__(self, filepath, z=None, z_name='z', zlib=True,
                 fill_value=9999.):

        if not os.path.isfile(filepath):
            mode = 'w'
        else:
            mode = 'r'

        if z is None:
            z = [None]

        self.zlib = bool(zlib)
        self.z_name = str(z_name)
        self.fill_value = fill_value

        self.ds = Dataset(filepath, mode)

        self._assign_attrs({'creation_date': datetime.now()},
                           {'lon' : self._lon_attr, 'lat': self._lat_attr,
                            'alt': self._alt_attr, 'loc_id': self._loc_id_attr})

        self._store(filepath)


    @property
    def shape(self) -> tuple:
        return (self.ds['lon'].size, self.ds['lat'].size, self.ds['alt'].size,
                self.ds[self.z_name].size)

    def _add_empty_3d(self, lon, lat, name):
        # add a empty variable with z dimension of the passed name
        print('Add empty 3D variable {}'.format(name))
        self.ds[name] = \
            xr.DataArray(np.full(self.shape, self.fill_value),
                         dims=[self.z_name, 'lat', 'lon'],
                         coords=[self.ds[self.z_name], self.ds.lat, self.ds.lon])

    def _write_ser(self, data, **kwargs):
        """
        Write (time) series of multiple variables in data frame
        """
        for var in data.keys():

            if var not in self.ds.variables:
                self._add_empty_3d(var)

            assert data[var].size == self.ds[self.z_name].size

            dat = data[var]
            dat[np.isnan(dat)] = self.fill_value
            self.ds[var].loc[dict(**kwargs)] = dat

    def _write_pt(self, data, **kwargs):
        # takes arrays of lon, lat, z and data dict of arrays
        for var in data.keys():

            if var not in self.ds.variables:
                self._add_empty_3d(var)

            dat = data[var]
            dat[np.isnan(dat)] = self.fill_value

            self.ds[var].loc[dict(**kwargs)] = dat

    def _assign_attrs(self, global_attrs=None, var_attrs=None):
        """ Assign global and variable attributes """
        if global_attrs is None:
            global_attrs = {}

        if var_attrs is None:
            var_attrs = {}

        for var, attr in var_attrs.items():
            self.ds.variables[var].assign_attrs(var_attrs)

        self.ds = self.ds.assign_attrs(global_attrs)

    def _store(self, filename=None, global_attrs=None, var_attrs=None,
               dtypes=np.float32):
        """
        Write down xarray cute to netcdf file

        Parameters
        ----------
        filename : str
            Path to the stack file to write
        global_attrs : dict, optional (default: None)
            Global attributes
        var_attrs : dict of dicts, optional (default: None)
            Variables (keys) and the attributes (values) as dicts
        dtypes : np.float32
            Data types of results, affects compression.
        """
        self._assign_attrs(global_attrs, var_attrs)

        try:
            if self.zlib:
                encoding = {}
                for var in self.ds.variables:
                    if var not in ['lat', 'lon', self.z_name]:
                        encoding[var] = {'complevel': 9, 'zlib': True,
                                         'dtype': dtypes,
                                         '_FillValue': self.fill_value}
            else:
                encoding = None
            self.ds.to_netcdf(filename, engine='netcdf4', encoding=encoding)
        except:  # todo: specifiy exception
            warnings.warn('Compression failed, store uncompressed results.')
            self.ds.to_netcdf(filename, engine='netcdf4')

    def close(self):
        self.ds.close()

    def store_files(self, path, filename_templ='file_{}.nc',
                    global_attrs=None, var_attrs=None,
                    dtypes=np.float32):
        """
        filename_templ :
            {} is replaced by the z indicator (strftime(z) if z is a date time).
        """
        # todo: add option to append to existing file (memory dump)
        # todo: integrate with the other function

        self._assign_attrs(global_attrs, var_attrs)


        if self.zlib:
            encoding = {}
            for var in self.ds.variables:
                if var not in ['lat', 'lon', self.z_name]:
                    encoding[var] = {'complevel': 9, 'zlib': True,
                                     'dtype': dtypes,
                                     '_FillValue': self.fill_value}
        else:
            encoding = None
        datetime_obs = [np.datetime64, datetime]
        for z in self.ds[self.z_name]:
            if any([isinstance(z.values, dt) for dt in datetime_obs]):
                pydatetime=pd.to_datetime(z.values).to_pydatetime()
                datestr = datetime.strftime(pydatetime, '%Y%m%d')
                filename = filename_templ.format(datestr)
            else:
                filename = filename_templ.format(str(z.values))
            try:
                self.ds.loc[{self.z_name: z}].to_netcdf(os.path.join(path, filename),
                                                       engine='netcdf4', encoding=encoding)
            except:  # todo: specifiy exception
                warnings.warn('Compression failed, store uncompressed results.')
                self.ds.loc[{self.z_name: z}].to_netcdf(os.path.join(path, filename),
                                                       engine='netcdf4')

        self.ds.close()

    def write_point(self, lon, lat, z, data):
        # DUPLICATE
        """
        Add data for a single point and a single z value.

        Parameters
        ---------
        lon : np.array or list (1d)
            Longitude of the point to write, same size as lat and z
        lat : np.array or list (1d)
            Latitude of the point to write, same size as lon and z
        z : np.array or list (1d)
            3rd dimension value of the point to write, same size as lon and lat
        data : dict
            Dictionary of variables and values to write.
            Values must have same size as lon, lat and z.
        """

        data = copy.deepcopy(data)

        if not isinstance(lon, (np.ndarray, list)):
            lon = np.array([lon])
        if not isinstance(lat, (np.ndarray, list)):
            lat = np.array([lat])
        if not isinstance(z, (np.ndarray, list)):
            z = np.array([z])

        if not lon.size == lat.size == z.size:
            raise ValueError('Sizes of passed dimension dont match '
                '(lon={}, lat={}, ref={})'.format(lon.size, lat.size, z.size))
        else:
            n = lon.size

        for k, v in data.items():
            if not isinstance(v, (np.ndarray, list)):
                data[k] = np.array([v])
            if data[k].size != n:
                raise ValueError('Size of variable {}, does not match sizes of '
                                 'dimensions: {} vs. {}'.format(k, data[k].size, n))

        # z values must already be in the dimension
        assert np.all(i in self.ds[self.z_name] for i in z)

        data['lat'] = lat
        data['lon'] = lon

        kwargs = {self.z_name: z}
        self._write_pt(data, **kwargs)
