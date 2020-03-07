# -*- coding: utf-8 -*-

"""
Module description
"""
# TODO:
#   (+) Write a class for this
# ---------
# NOTES:
#   -

# -*- coding: utf-8 -*-


import os
import netCDF4
from datetime import datetime
import numpy as np
from pynetcf.base import Dataset
import pandas as pd

class ScatterImage(Dataset):
    """
    Represents a single (2d) netcdf image with pointed data across 1 dimension
    """

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

    _time_attr = {'standard_name': 'time'}

    def __init__(self, filename, mode='r', obs_dim='obs', dtype_time='str',
                 complevel=6):
        """
        Initialise the 2d scatter image from the Dataset base.

        Parameters
        ----------
        filename : string
            filename of netCDF file. If already exiting then it will be opened
            as read only unless the append keyword is set. if the overwrite
            keyword is set then the file will be overwritten
        mode : string, optional (default: 'r')
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
        obs_dim : str, optional (default: 'obs')
            Name of the (only) dimension along which the data is stored.
        dtype_time : str, optional (default: 'str')
            Choose either 'str' or 'datetime'
        complevel : int or None, optional (default: 6)
            Activate netcdf compression with the selected level (0-9).
        """
        initial_mode = mode
        self.obs_dim = str(obs_dim)

        self.dim = {obs_dim: None}

        self.time_dtype, self.time_unit = self._dtype_time(dtype_time)

        self.var = {'loc_id':
                        {'name': 'loc_id', 'dim': obs_dim, 'attr': self._loc_id_attr,
                         'dtype': np.int32},
                    'lon':
                        {'name': 'lon', 'dim': obs_dim, 'attr': self._lon_attr,
                         'dtype': np.float32},
                    'lat':
                        {'name': 'lat', 'dim': obs_dim, 'attr': self._lat_attr,
                         'dtype': np.float32},
                    'alt':
                        {'name': 'alt', 'dim': obs_dim, 'attr': self._alt_attr,
                         'dtype': np.float32},
                    'time':
                        {'name': 'time', 'dim': obs_dim, 'attr': self._time_attr,
                         'dtype': self.time_dtype}}

        self.builtin_vars = np.array(list(self.var.keys()))

        comp = {'zlib' : False if complevel in [0, None, False] else True,
                'complevel' : complevel}

        super(ScatterImage, self).__init__(filename, mode=initial_mode, **comp)

        if initial_mode == 'w':
            self.add_global_attr('featureType', 'point')
            for name, n in self.dim.items():
                self.create_dim(name, n)
            for _, kwargs in self.var.items():
                self.write_var(data=None, **kwargs)
    
    def _dtype_time(self, t):
        if t == 'str':
            return np.str, None
        elif t == 'date':
            return np.float64, "days since 1900-01-01 00:00:00"
        else:
            raise ValueError('Unknown dtype_time passed : {}'.format(t))
        
        
    def __len__(self):
        loc_id = self.dataset.variables[self.var['loc_id']['name']]
        return loc_id.shape[0]

    @property
    def shape(self) -> tuple:
        return (self.dataset.dimensions[self.obs_dim].size, )

    def __str__(self):
        """
        String representation of class instance.
        """
        if self.dataset is not None:
            str = self.dataset.__str__()
        else:
            str = 'NetCDF file closed.'

        return str

    def __getitem__(self, item):
        """
        Accessing netCDF variable.
        Parameters
        ----------
        item : str
            Variable name.
        Returns
        -------
        var : netcdf4.variable
            NetCDF variable.
        """
        return self.dataset.variables[item]

    def _as_img_df(self, index2d=False):

        data = {}

        num = None
        for var in self.dataset.variables.keys():
            dat = self[var][:][~self[var][:].mask]
            if num is None:
                num = dat.size
            else:
                assert dat.size == num
            data[var] = dat

        df = pd.DataFrame(data=data)

        if index2d:
            lat, lon = self.var['lat']['name'], self.var['lon']['name']
            return df.set_index([lat, lon])
        else:
            loc_id = self.var['loc_id']['name']
            return df.set_index(loc_id)

    def _lookup(self, idx=None, index2d=False):
        """ Look up the passed elements in the df """
        if self.mode in ['r', 'r+', 'a']:
            df = self._as_img_df(index2d)
            if idx is None:
                return df
            else:
                return df.loc[idx]
        else:
            raise IOError("Read operations failed. "
                          "File not open for reading.")

    def _read_loc(self, loc_id=None) -> pd.DataFrame:
        """ Read by locations """
        return self._lookup(loc_id, False)

    def _read_lonlat(self, lon, lat) -> pd.DataFrame:
        """ Read by lon/lat """
        try:
            idx = zip(lon, lat)
        except TypeError:
            idx =zip(np.array([lon]), np.array([lat]))

        return self._lookup(idx, True)

    def read_img(self, *args, **kwargs):
        """
        Read data for a location id or a lon/lat combination
        """
        if len(args) + len(kwargs) == 1:
            return self._read_loc(*args, **kwargs)
        else:
            return self._read_lonlat(*args, **kwargs)

    def write_ts(self, df, lon, lat, alt=None):
        """
        Write down a time series to the given location.

        Parameters
        ---------
        df : pd.DataFrame
            DataFrame (time series)
        lon : float
            Longitude
        lat : float
            latitude
        alt : float, optional (default: None)
        """
        times = df.index.values
        num = times.size

        loc_idx = len(self)
        self.append_var('loc_id', np.arange(loc_idx, loc_idx+num, 1))

        lons = np.repeat(lon, num)
        lats = np.repeat(lat, num)

        if alt is not None:
            alts = np.repeat(alt, num)
        else:
            alts = None

        for name, dat in data.items():
            assert dat.size == num
            if not name in self.dataset.variables.keys():
                self.write_var(name, data=dat, dim=self.obs_dim)
            else:
                self.append_var(name, dat)


    def write_points(self, data, lon, lat, alt=None, time=None):
        """
        Append data for locations to the dataset. Write data in space dimension,
        i.e. arrays represent multiple locations.

        Parameters
        ---------
        data : dict [str : np.array]
            Data of the points
        lon : np.array [float]
            Longitudes of the points
        lat : np.array [float]
            Latitudes of the points
        alt : np.array [float], optional (default: None)
            Altitude of the points
        time : datetime, optional (default: None)
            The (single) time stamp of all points
        """
        num = lon.size
        assert lat.size == num

        loc_idx = len(self)
        self.append_var('loc_id', np.arange(loc_idx, loc_idx+num, 1))

        self.append_var('lon', lon)
        self.append_var('lat', lat)
        if alt is None:
            alt = np.repeat(np.nan, num)
        self.append_var('alt', alt)

        if time is None:
            time = np.nan
        else:
            if self.time_dtype == 'date':
                time = netCDF4.date2num(time, self.time_unit)
            else:
                time = str(time)
        self.append_var('time', np.repeat(time, num))

        for name, dat in data.items():
            assert dat.size == num
            if not name in self.dataset.variables.keys():
                self.write_var(name, data=dat, dim=self.obs_dim)
            else:
                self.append_var(name, dat)




if __name__ == '__main__':
    filepath = r'C:\Temp\myfile.nc'

    ds = ScatterImage(filepath, mode='w')
    data = {'var1': np.array([1.123,2.213,33.2, 33.4])}
    lon = np.array([18,19, 20, 20])
    lat = np.array([48,49, 50, 50])
    ds.write_points(data=data, lon=lon, lat=lat, time=datetime(2000,1,1))
    ds.close()

    ds = ScatterImage(filepath)
    data =ds.read_img(None)
    data = ds.read_img(19, 49)
    data = ds.read_img([1,2])
    data = ds.read_img([18,19],[48,49])