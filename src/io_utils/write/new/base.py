# -*- coding: utf-8 -*-

"""
Module description
"""
# TODO:
#   (+) 
#---------
# NOTES:
#   -

import os
import xarray as xr
import netCDF4
import time
import numpy as np
import datetime
from collections import OrderedDict

class DatasetError(Exception):
    pass

class NcBase(object):

    """ Dataset base that used the netcdf4 backend """

    def __init__(self, filename, mode='r', file_format="NETCDF4", autoscale=True,
                 automask=True, glob_attr=None, complevel=6):

        self.filename = filename
        self.file_format = file_format
        self.mode = mode

        self.comp = {'zlib' : False if complevel in [0, None, False] else True,
                     'complevel' : complevel}

        try:
            self.dataset = netCDF4.Dataset(self.filename, self.mode,
                                           format=self.file_format)
        except RuntimeError:
            raise IOError("File {} does not exist".format(filename))

        self.autoscale = autoscale
        self.automask = automask

        self.dataset.set_auto_scale(autoscale)
        self.dataset.set_auto_mask(automask)

        if glob_attr is None:
            self.global_attr = {}
        else:
            self.global_attr = glob_attr

        s = "%Y-%m-%d %H:%M:%S"
        self.global_attr['date_created'] = datetime.datetime.now().strftime(s)

    def create_dim(self, name, n):
        """
        Create dimension for NetCDF file.
        if it does not yet exist

        Parameters
        ----------
        name : str
            Name of the NetCDF dimension.
        n : int or None
            Size of the dimension.
        """
        if name not in self.dataset.dimensions.keys():
            self.dataset.createDimension(name, size=n)

    def write_var(self, name, data=None, dim=None, attr=None, dtype=None,
                  zlib=None, complevel=None, chunksizes=None, **kwargs):
        """
        Create or overwrite values in a NetCDF variable. The data will be
        written to disk once flush or close is called

        Parameters
        ----------
        name : str
            Name of the NetCDF variable.
        data : np.ndarray, optional
            Array containing the data.
            if not given then the variable will be left empty
        dim : tuple, optional
            A tuple containing the dimension names.
        attr : dict, optional
            A dictionary containing the variable attributes.
        dtype: data type, string or numpy.dtype, optional
            if not given data.dtype will be used
        zlib: boolean, optional
            explicit compression for this variable
            if not given then global attribute is used
        complevel: int, optional
            explicit compression level for this variable
            if not given then global attribute is used
        chunksizes : tuple, optional
            chunksizes can be used to manually specify the
            HDF5 chunksizes for each dimension of the variable.
        """
        if attr is None:
            attr = {}

        fill_value = None
        if '_FillValue' in attr:
            fill_value = attr.pop('_FillValue')

        if dtype is None:
            dtype = data.dtype

        if zlib is None:
            zlib = self.comp['zlib']
        if complevel is None:
            complevel = self.comp['complevel']

        if name in self.dataset.variables.keys():
            var = self.dataset.variables[name]
        else:
            var = self.dataset.createVariable(
                name, dtype, dim, fill_value=fill_value,
                zlib=zlib, complevel=complevel, chunksizes=chunksizes,
                **kwargs)

        for attr_name in attr:
            attr_value = attr[attr_name]
            var.setncattr(attr_name, attr_value)

        var.set_auto_scale(self.autoscale)
        if data is not None:
            var[:] = data

    def append_var(self, name, data, **kwargs):
        """
        append data along unlimited dimension(s) of variable

        Parameters
        ----------
        name : string
            Name of variable to append to.
        data : numpy.array
            Numpy array of correct dimension.

        Raises
        ------
        IOError
            if appending to variable without unlimited dimension
        """
        if name in self.dataset.variables.keys():
            var = self.dataset.variables[name]
            dim_unlimited = []
            key = []
            for index, dim in enumerate(var.dimensions):
                unlimited = self.dataset.dimensions[dim].isunlimited()
                dim_unlimited.append(unlimited)
                if not unlimited:
                    # if the dimension is not unlimited set the slice to :
                    key.append(slice(None, None, None))
                else:
                    # if unlimited set slice of this dimension to
                    # append meaning
                    # [var.shape[index]:]
                    key.append(slice(var.shape[index], None, None))

            dim_unlimited = np.array(dim_unlimited)
            nr_unlimited = np.where(dim_unlimited)[0].size
            key = tuple(key)
            # if there are unlimited dimensions we can do an append
            if nr_unlimited > 0:
                var[key] = data
            else:
                raise IOError(''.join(('Cannot append to variable that ',
                                       'has no unlimited dimension')))
        else:
            self.write_var(name, data, **kwargs)


    def _set_global_attr(self):
        """
        Write global attributes to NetCDF file.
        """
        self.dataset.setncatts(self.global_attr)
        self.global_attr = {}

    def flush(self):
        if self.dataset is not None:
            if self.mode in ['w', 'r+']:
                self._set_global_attr()
                self.dataset.sync()


class XrBase(object):
    """ Dataset base that used the xarray backend """
    def __init__(self, filename, mode='r', file_format="NETCDF4",
                 glob_attr=None, complevel=6):
        """"
        Parameters:
        ----------
        filename : str
            Path to the the file to create or to read.
        mode : str, optional (default: 'r')
            'w' will overwrite any existing file, 'r+' or 'a' open the file in
            append mode and 'r' allow reading only.
        file_format : str, optional (default: 'NETCDF4')
            File format of input/output file. If 'GRIB' is selected, we use
            cfgrib to read the file, but any output will be a NETCDF4 file.
            Other options:
            * NETCDF4: Data is stored in an HDF5 file, using netCDF4 API
              features.
            * NETCDF4_CLASSIC: Data is stored in an HDF5 file, using only
              netCDF 3 compatible API features.
            * NETCDF3_64BIT: 64-bit offset version of the netCDF 3 file format,
              which fully supports 2+ GB files, but is only compatible with
              clients linked against netCDF version 3.6.0 or later.
            * NETCDF3_CLASSIC: The classic netCDF 3 file format. It does not
              handle 2+ GB files very well.
        glob_attr : dict, optional (default: None)
            Global attributes for the netcdf file to assign
        complevel : int or None, optional (default: 6)
            Compression level (0-9), 0 or None means no compression
        """
        self.filename = filename
        self.mode = mode

        self.comp = {'zlib' : False if complevel in [0, None, False] else True,
                     'complevel' : complevel}

        if os.path.isfile(self.filename) and self.mode in ['r', 'r+', 'a']:
            if file_format == 'GRIB': # grib is only allowed as input format
                engine = 'cfgrib'
                file_format = 'NETCDF4'
            else:
                engine = 'netcdf4'
            self.dataset = xr.open_dataset(self.filename, engine=engine)
            self.global_attr = self.dataset.attrs
        else:
            self.dataset = xr.Dataset()
            self.global_attr = glob_attr if glob_attr is not None else {}

        self.unlimited_dims = []
        self.file_format = file_format

    def shape(self, d='dim'):
        """ Get the shape of features of this object """
        if d == 'dim':
            return self.dataset.dims
            # return tuple([self.dataset.dims[d] for d in self.dataset.dims])
        else:
            raise NotImplementedError

    def create_dim(self, name, coords=None):
        """
        Create dimension if it doesnt yet exist or expand an existing one

        Parameters
        ----------
        name : str
            Name of the NetCDF dimension.
        coords : int or None or array, optional (default: None)
            Size of the dimension (int), unlimited (None), or the coords that
            fill the dimension (array).
        """
        if coords is None:
            self.unlimited_dims.append(name)
            #coords = []

        if name not in self.dataset.dims.keys():
            # Ordered dict for python 3.5 compatibility
            self.dataset = self.dataset.expand_dims(OrderedDict([(name, coords)]))
        else:
            print('Dimension {} already exists, skip creation'.format(name))

    def _append_coords(self, name, new_coords):
        """
        Add new coordinates to an existing dimension (at the end).

        Parameters
        ----------
        name : str
            Name of the dimension to append to
        new_vals: np.array
            Values that the dimension is extended with.
        """

        if name not in self.dataset.dims:
            self.create_dim(name, new_coords)
        else:
            old_coords = self.dataset[name].values
            coords = np.append(old_coords, new_coords)
            self.dataset = self.dataset.reindex({name: coords})

    def write_var(self, name, data=None, dim=None, attr=None, dtype=None):
        """
        Create or overwrite values in a NetCDF variable. The data will be
        written to disk once flush or close is called

        Parameters
        ----------
        name : str
            Name of the NetCDF variable.
        data : np.ndarray, optional
            Array containing the data.
            if not given then the variable will be left empty
        dim : tuple, optional
            A tuple containing the dimension names. Order matters!
        attr : dict, optional
            A dictionary containing the variable attributes.
        dtype: data type, string or numpy.dtype, optional
            if not given data.dtype will be used
        zlib: boolean, optional
            explicit compression for this variable
            if not given then global attribute is used
        complevel: int, optional
            explicit compression level for this variable
            if not given then global attribute is used
        chunksizes : tuple, optional
            chunksizes can be used to manually specify the
            HDF5 chunksizes for each dimension of the variable.
        """
        encoding = {}

        # if data.shape != self.shape('dim'):
        #     raise ValueError('Data dimension do not match dataset dimensions.'
        #                      'Expected {}, got {}'.format(self.shape('dim'), data.shape))
        if dtype is None:
            encoding['dtype'] = data.dtype

        if '_FillValue' in attr:
            encoding['_FillValue'] = attr.pop('_FillValue')

        encoding['zlib'] = self.comp['zlib']
        encoding['complevel'] = self.comp['complevel']

        var = xr.Variable(dims=dim, data=data, attrs=attr,
                          encoding=encoding)

        self.dataset = self.dataset.assign({name: var})

    def append_var(self, name, data, dim, **kwargs):
        """
        append data along unlimited dimension(s) of variable

        Parameters
        ----------
        name : string
            Name of variable to append to.
        data : numpy.array
            Numpy array of correct dimension.
        dim : list [str]
            According dimensions for data
        axis : tuple or str
            Name of the unlimited dimension(s) that the data is appended to.

        Raises
        ------
        IOError
            if appending to variable without unlimited dimension
        """
        # Find out what the unlimited dims of data are
        d_ultd = []
        d_ltd = []
        for d in dim:
            if d in self.unlimited_dims:
                d_ultd.append(d)
            else:
                d_ltd.append(d)

        if name in self.dataset.variables.keys():

            var = self.dataset.variables[name]




            dim_unlimited = []
            key = []
            for index, dim in enumerate(var.dims):
                unlimited = self.dataset.dimensions[dim].isunlimited()
                dim_unlimited.append(unlimited)
                if not unlimited:
                    # if the dimension is not unlimited set the slice to :
                    key.append(slice(None, None, None))
                else:
                    # if unlimited set slice of this dimension to
                    # append meaning
                    # [var.shape[index]:]
                    key.append(slice(var.shape[index], None, None))

            dim_unlimited = np.array(dim_unlimited)
            nr_unlimited = np.where(dim_unlimited)[0].size
            key = tuple(key)
            # if there are unlimited dimensions we can do an append
            if nr_unlimited > 0:
                var[key] = data
            else:
                raise IOError(''.join(('Cannot append to variable that ',
                                       'has no unlimited dimension')))
        else:
            self.write_var(name, data, dim, **kwargs)

    def _set_global_attr(self):
        """
        Write global attributes to NetCDF file.
        """
        s = "%Y-%m-%d %H:%M:%S"
        self.global_attr['date_created'] = datetime.datetime.now().strftime(s)
        self.dataset.assign_attrs(self.global_attr)

    def flush(self):
        if self.dataset is not None:
            if self.mode in ['w', 'r+']:
                self._set_global_attr()
                self.dataset.to_netcdf(self.filename, format=self.file_format,
                                       unlimited_dims=self.unlimited_dims)


class Dataset(object):

    """
    NetCDF file wrapper class that makes some things easier

    Parameters
    ----------
    filename : string
        filename of netCDF file. If already exiting then it will be opened
        as read only unless the append keyword is set. if the overwrite
        keyword is set then the file will be overwritten
    name : string, optional
        will be written as a global attribute if the file is a new file
    file_format : string, optional
        file format
    mode : string, optional
        access mode. default 'r'
        'r' means read-only; no data can be modified.
        'w' means write; a new file is created, an existing file with the
            same name is deleted.
        'a' and 'r+' mean append (in analogy with serial files); an existing
            file is opened for reading and writing.
        Appending s to modes w, r+ or a will enable unbuffered shared access
        to NETCDF3_CLASSIC or NETCDF3_64BIT formatted files. Unbuffered
        access may be useful even if you don't need shared access, since it
        may be faster for programs that don't access data sequentially.
        This option is ignored for NETCDF4 and NETCDF4_CLASSIC
        formatted files.
    zlib : boolean, optional
        Default True
        if set netCDF compression will be used
    complevel : int, optional
        Default 4
        compression level used from 1(low compression) to 9(high compression)
    autoscale : bool, optional
        If disabled data will not be automatically scaled when reading and
        writing
    automask : bool, optional
        If disabled data will not be masked during reading.
        This means Fill Values will be used instead of NaN.
    """

    def __init__(self, filename, name=None, file_format="NETCDF4", backend='netCDF4',
                 mode='r', zlib=True, complevel=4,
                 autoscale=True, automask=True):

        self.dataset_name = name
        self.filename = filename
        self.file = None
        self.file_format = file_format
        self.buf_len = 0
        self.global_attr = {}
        self.global_attr['id'] = os.path.split(self.filename)[1]
        s = "%Y-%m-%d %H:%M:%S"
        self.global_attr['date_created'] = datetime.datetime.now().strftime(s)
        if self.dataset_name is not None:
            self.global_attr['dataset_name'] = self.dataset_name
        self.zlib = zlib
        self.complevel = complevel
        self.mode = mode
        self.autoscale = autoscale
        self.automask = automask

        if self.mode == "a" and not os.path.exists(self.filename):
            self.mode = "w"
        if self.mode == 'w':
            self._create_file_dir()

        try:
            self.dataset = netCDF4.Dataset(self.filename, self.mode,
                                           format=self.file_format)
        except RuntimeError:
            raise IOError("File {} does not exist".format(self.filename))

        self.dataset.set_auto_scale(self.autoscale)
        self.dataset.set_auto_mask(self.automask)

    def _create_file_dir(self):
        """
        Create directory for file to sit in.
        Avoid race condition if multiple instances are
        writing files into the same directory.
        """
        path = os.path.dirname(self.filename)
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except OSError:
                time.sleep(1)
                self._create_file_dir()

    def _set_global_attr(self):
        """
        Write global attributes to NetCDF file.
        """
        self.dataset.setncatts(self.global_attr)
        self.global_attr = {}

    def create_dim(self, name, n):
        """
        Create dimension for NetCDF file.
        if it does not yet exist

        Parameters
        ----------
        name : str
            Name of the NetCDF dimension.
        n : int
            Size of the dimension.
        """
        if name not in self.dataset.dimensions.keys():
            self.dataset.createDimension(name, size=n)

    def write_var(self, name, data=None, dim=None, attr={}, dtype=None,
                  zlib=None, complevel=None, chunksizes=None, **kwargs):
        """
        Create or overwrite values in a NetCDF variable. The data will be
        written to disk once flush or close is called

        Parameters
        ----------
        name : str
            Name of the NetCDF variable.
        data : np.ndarray, optional
            Array containing the data.
            if not given then the variable will be left empty
        dim : tuple, optional
            A tuple containing the dimension names.
        attr : dict, optional
            A dictionary containing the variable attributes.
        dtype: data type, string or numpy.dtype, optional
            if not given data.dtype will be used
        zlib: boolean, optional
            explicit compression for this variable
            if not given then global attribute is used
        complevel: int, optional
            explicit compression level for this variable
            if not given then global attribute is used
        chunksizes : tuple, optional
            chunksizes can be used to manually specify the
            HDF5 chunksizes for each dimension of the variable.
        """

        fill_value = None
        if '_FillValue' in attr:
            fill_value = attr.pop('_FillValue')

        if dtype is None:
            dtype = data.dtype

        if zlib is None:
            zlib = self.zlib
        if complevel is None:
            complevel = self.complevel

        if name in self.dataset.variables.keys():
            var = self.dataset.variables[name]
        else:
            var = self.dataset.createVariable(name, dtype,
                                              dim, fill_value=fill_value,
                                              zlib=zlib, complevel=complevel,
                                              chunksizes=chunksizes, **kwargs)

        for attr_name in attr:
            attr_value = attr[attr_name]
            var.setncattr(attr_name, attr_value)

        var.set_auto_scale(self.autoscale)
        if data is not None:
            var[:] = data

    def append_var(self, name, data, **kwargs):
        """
        append data along unlimited dimension(s) of variable

        Parameters
        ----------
        name : string
            Name of variable to append to.
        data : numpy.array
            Numpy array of correct dimension.

        Raises
        ------
        IOError
            if appending to variable without unlimited dimension
        """
        if name in self.dataset.variables.keys():
            var = self.dataset.variables[name]
            dim_unlimited = []
            key = []
            for index, dim in enumerate(var.dimensions):
                unlimited = self.dataset.dimensions[dim].isunlimited()
                dim_unlimited.append(unlimited)
                if not unlimited:
                    # if the dimension is not unlimited set the slice to :
                    key.append(slice(None, None, None))
                else:
                    # if unlimited set slice of this dimension to
                    # append meaning
                    # [var.shape[index]:]
                    key.append(slice(var.shape[index], None, None))

            dim_unlimited = np.array(dim_unlimited)
            nr_unlimited = np.where(dim_unlimited)[0].size
            key = tuple(key)
            # if there are unlimited dimensions we can do an append
            if nr_unlimited > 0:
                var[key] = data
            else:
                raise IOError(''.join(('Cannot append to variable that ',
                                       'has no unlimited dimension')))
        else:
            self.write_var(name, data, **kwargs)

    def read_var(self, name):
        """
        reads variable from netCDF file

        Parameters
        ----------
        name : string
            name of the variable
        """

        if self.mode in ['r', 'r+']:
            if name in self.dataset.variables.keys():
                return self.dataset.variables[name][:]

    def add_global_attr(self, name, value):
        self.global_attr[name] = value

    def flush(self):
        if self.dataset is not None:
            if self.mode in ['w', 'r+']:
                self._set_global_attr()
                self.dataset.sync()

    def close(self):
        if self.dataset is not None:
            self.dataset.flush()
            self.dataset.close()
            self.dataset = None

    def __enter__(self):
        return self

    def __exit__(self, value_type, value, traceback):
        self.dataset.close()
