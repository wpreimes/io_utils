# -*- coding: utf-8 -*-

"""
Xarray Stacked Images Writer.
Create 3D datasets, allows setting spatial and temporal subset (images and time
series)
"""
#TODO. File locking as option for multiple processes?
# todo: Add Point data results manager (for ismn based results)

import xarray as xr
import numpy as np
import pandas as pd
from datetime import datetime
import warnings
import matplotlib.pyplot as plt
import os
from io_utils.utils import safe_arange
from pygeogrids.grids import BasicGrid, CellGrid, lonlat2cell
import copy
from io_utils.write.utils import minmax


def to_reg_cell_grid(grid, cellsize=5.):
    """
    Create RegularCellGrid from BasicGrid or CellGrid

    Parameters
    ----------
    grid : CellGrid or BasicGrid
        Input grid to convert
    cellsize : float, optional (default: 5.)
        Cell size of the CellGrid to create.

    Returns
    -------
    grid : RegularCellGrid
        A regularly gridded CellGrid
    """

    if isinstance(grid, RegularCellGrid) and (grid.cellsize == cellsize):
        return grid

    return RegularCellGrid(grid.arrlon, grid.arrlat, cellsize, gpis=grid.gpis,
                           subset=grid.subset, shape=grid.shape)


class Point(object):

    """ Helper class to combine lon and lat in one Point """

    def __init__(self, lon, lat):

        if lat > 90. or lat <-90:
            raise IOError('{} is out of valid bounds (+-90) for Latitude'.format(lat))
        if lon > 180. or lon <-180:
            raise IOError('{} is out of valid bounds (+-180) for Longitude'.format(lon))

        self.__lon, self.__lat = lon, lat
        self.__loc = (lon, lat)

    def __str__(self):
        return 'Lon: {}, Lat: {}'.format(self.lon, self.lat)

    @property
    def lon(self):
        return self.__lon

    @property
    def lat(self):
        return self.__lat

    @property
    def loc(self):
        return (self.lon, self.lat)

class RegularCellGrid(CellGrid):

    # Special for of a Cell Grid that has equal spacing between grid points

    def __init__(self, lon, lat, cellsize=5., gpis=None, geodatum='WGS84',
                 subset=None, setup_kdTree=False, **kwargs):

        self.cellsize = cellsize
        cells = lonlat2cell(lon, lat, cellsize=cellsize)

        super(RegularCellGrid, self).__init__(lon, lat, cells, gpis, geodatum,
                                              subset=subset, setup_kdTree=setup_kdTree,
                                              **kwargs)

        self.dx, self.dy = self._grid_space()

    def _grid_space(self):
        # find the resolution of the grid and check if it is regular along x and y
        lons, lats = self.get_grid_points()[1], self.get_grid_points()[2]
        diff_x = np.around(np.diff(sorted(np.unique(lons))), 5)
        diff_y = np.around(np.diff(sorted(np.unique(lats))), 5)

        dx = np.max(diff_x)
        assert np.min(diff_x) == dx
        dy = np.max(diff_y)
        assert np.min(diff_y) == dy

        assert np.all(diff_x == dx)
        assert np.all(diff_y == dy)

        return dx, dy


class RegularArea(object):

    """ Helper class to combine lons and lats that span an Area """

    def __init__(self, llc, urc, grid):
        """
        Create an regularly gridded 2d Area.

        Parameters
        ----------
        llc : Point
            Lower left corner point of the Area
        urc : Point
            Upper right corner point of the Area
        grid : BasicGrid or CellGrid
            An independent grid that the area is a subset of.
        """
        self.grid = to_reg_cell_grid(grid)

        self.llc = llc
        self.urc = urc

        self.subset = self._subset_from_corners()

    def _subset(self, llc, urc):

        ind = np.where((self.grid.activearrlon >= llc.lon) &
                       (self.grid.activearrlon <= urc.lon) &
                       (self.grid.activearrlat >= llc.lat) &
                       (self.grid.activearrlat <= urc.lat))

        gpis = self.grid.activegpis[ind]
        lons = self.grid.activearrlon[ind]
        lats = self.grid.activearrlat[ind]

        return gpis, lons, lats

    def _subset_from_corners(self):
        self._assert_corners()

        gpis, lons, lats = self._subset(self.llc, self.urc)

        subset = self.grid.subgrid_from_gpis(gpis)
        subset.shape = (np.unique(lats).size, np.unique(lons).size)

        return subset

    def _assert_corners(self):
        # check if the corner points are also in the grid
        assert self.llc.lon in self.grid.get_grid_points()[1]
        assert self.llc.lat in self.grid.get_grid_points()[2]

    def as_slice(self, d=False):
        """
        Create a lon and lat slice of the Area.

        Parameters
        ---------
        d : bool, optional (default: False)
            Include step size in slice

        Returns
        -------
        lon_slice : slice
            Slice across the area
        lat_slice : slice
            Slice across the area
        """
        return slice(self.llc.lon, self.urc.lon, self.grid.dx if d else None), \
               slice(self.llc.lat, self.urc.lat, self.grid.dy if d else None)


class NcRegGridStack(object):

    """ Store netcdf cubes with xarray and dask """

    def __init__(self, dx=0.25, dy=0.25, z=None, z_name='z',
                 llc=Point(-179.875, -89.875), urc=Point(179.875, 89.875),
                 indexed=True, zlib=True, fill_value=9999.):

        """
        Parameters
        ----------
        dx : float, optional (default: 0.25)
            Regular spacing in x/lon direction
        dy : float, optional (default: 0.25)
            Regular spacing in y/lat direction
        z : np.array
            Z Values, e.g. Timestamps (z dimension of cube)
        z_name : str, optional (default: time)
            Name of the z dimension (e.g. time or depth)
        llc : Point, optional (default: Point(-179.875, -89.875))
            Lower left corner point of the dataset area.
        urc : Point, optional (default: Point(179.875, 89.875))
            Upper right corner point of the dataset area.
        indexed : bool, optional (default: True)
            Add a 2d variable of unique index to each point of the dataset.
        zlib : bool, optional (default: True)
            Compress data when writing to netcdf
        fill_value : float, optional (default: 9999.)
            Fill value nans are replaced with
        """
        if z is None:
            z = [None]

        self.zlib = zlib
        self.z_name = z_name
        self.fill_value = fill_value

        self.llc, self.urc = llc, urc

        lons, lats = self._coords(dx, dy)
        self.shape = (z.size, lats.size, lons.size)

        gpis = self._gpis('ll') # origin is in the lower left

        self.ds = xr.Dataset(
            data_vars={'gpi': (['lat', 'lon'], gpis)} if indexed else None,
            coords={'lon': lons, 'lat': lats, self.z_name: z})

        self.grid = to_reg_cell_grid(self._grid(gpis), 5.)


    @property
    def subset(self):
        return (self.llc, self.urc)

    def _grid(self, gpis):
        # create a pygeogrids object

        lons, lats = np.meshgrid(self.ds.lon.values, np.flipud(self.ds.lat.values))
        lons, lats = lons.flatten(), lats.flatten()
        grid = BasicGrid(lons, lats, gpis=gpis.flatten()).to_cell_grid(5.)

        return grid

    def _gpis(self, origin='ll'):
        """
        Parameters
        ---------
        origin : str, optional (Default: 'll')
            String indication where gpi=0 is.
            ll = lower left, ur=upper right, lr = lower right, ul = upper left

        Returns
        ---------
        gpis : np.ndarray
            Array of GPIs
        """
        origins = ['ll', 'lr', 'ul', 'ur']

        if origin not in origins:
            raise NotImplementedError(
                "Origin {} not implemented. Choose one of: {}"
                    .format(origin, ','.join(origins)))

        n = self.shape[1] * self.shape[2]
        gpis = np.arange(n).reshape(self.shape[1], self.shape[2])

        if origin[0] == 'l':
            gpis = np.flipud(gpis)
        if origin[1] == 'r':
            gpis = np.fliplr(gpis)

        return gpis

    def _coords(self, dx, dy):
        """ Build coord range with chosen resolution over dataset area """
        lons = safe_arange(self.llc.lon, self.urc.lon+dx, dx)
        lats = safe_arange(self.llc.lat, self.urc.lat+dy, dy)
        self.dx, self.dy = dx, dy

        return lons, lats

    def _add_empty_3d(self, name):
        # add a empty variable with z dimension of the passed name
        #print('Add empty 3D variable {}'.format(name))
        self.ds[name] = \
            xr.DataArray(np.full(self.shape, self.fill_value),
                         dims=[self.z_name, 'lat', 'lon'],
                         coords=[self.ds[self.z_name], self.ds.lat, self.ds.lon])

    def _write_img(self, data, **kwargs):
        """
        Write area to dataset.

        Parameters
        ----------
        data : xr.Dataset, 2d arrays to write, keys are variable names
        """
        for var in list(data.data_vars.keys()):
            if var not in self.ds.variables:
                self._add_empty_3d(var)
            self.ds[var].loc[dict(**kwargs)] = data[var]

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


    def store_stack(self, filename=None, global_attrs=None, dtypes=np.float32):
        """
        Write down xarray cute to netcdf file

        Parameters
        ----------
        filename : str
            Path to the stack file to write
        global_attrs : dict, optional (default: None)
            Global attributes
        dtypes : np.float32
            Data types of results, affects compression.
        """
        if global_attrs is None:
            global_attrs = {}

        self.ds = self.ds.assign_attrs(global_attrs)

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

        self.ds.close()

    def store_files(self, path, filename_templ='file_{}.nc',
                    dtypes=np.float32):
        """
        filename_templ :
            {} is replaced by the z indicator (strftime(z) if z is a date time).
        """
        # todo: add option to append to existing file (memory dump)
        # todo: integrate with the other function

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

    def _subset_area(self, llc, urc):
        """
        Read subset of current dataset:

        Parameters
        ----------
        llc : Point
            Lower left corner point of area to read
        urc : Point
            Upper right corner point of area to read

        Returns
        ---------
        subset : xr.Dataset
            Spatial subset of the current Dataset.
        """

        lon_slice, lat_slice = RegularArea(llc, urc, self.grid).as_slice(True)
        subset = self.ds.loc[dict(lon=lon_slice, lat=lat_slice)]

        return subset

    def _df2arr(self, df, llc:Point, urc:Point, lon_name:str, lat_name:str):
        # get the lon and lat extent from df and create a 2d array#
        local_df = df.copy(True)
        area = RegularArea(llc, urc, self.grid)

        local_df = local_df.set_index([lat_name, lon_name]).sort_index()

        _, subset_lons, subset_lats, _ = area.subset.get_grid_points()

        full_df = pd.DataFrame(data={'lon': subset_lons, 'lat': subset_lats})
        full_df = full_df.set_index([lat_name, lon_name]).sort_index()

        for k in local_df.columns:
            full_df[k] = self.fill_value

        full_df.loc[local_df.index] = local_df
        arr = full_df.to_xarray()

        slice_lon, slice_lat = area.as_slice(False)

        return arr, slice_lon, slice_lat

    def spatial_subset(self, llc, urc, in_place=False):
        """
        Cut the current data set to a new subset
        """
        if in_place:
            self.ds = self._subset_area(llc, urc)
            return self.ds
        else:
            return self._subset_area(llc, urc)

    def write_image(self, df, z=None, lat_name='lat', lon_name='lon'):
        """
        Add data for multiple locations at a specific point in z (e.g. time stamp)

        Parameters
        ----------
        z : int or float or str
            Index in z-dimension (e.g. time stamp)
        df : pd.DataFrame
            DataFrame that contains image points.
        lat_name : str, optional (default: 'lat')
            Name of the latitude variable in the data frame.
        lon_name : str, optional (default: 'lon')
            Name of the longitude variable in the data frame.
        """
        if z not in self.ds[self.z_name].values:
            raise ValueError('{} was not found in the {} dimension.'
                             .format(z, self.z_name))

        min_lon, max_lon = minmax(df[lon_name].values)
        min_lat, max_lat = minmax(df[lat_name].values)

        llc = Point(min_lon, min_lat)
        urc = Point(max_lon, max_lat)

        data, slice_lon, slice_lat = self._df2arr(df, llc, urc, lon_name, lat_name)

        kwargs = {'lon' : slice_lon, 'lat' : slice_lat, self.z_name : z}
        self._write_img(data, **kwargs)

    def write_series(self, lon, lat, df):
        """
        Add data for multiple z values, for a single location. Series is in z-dimension.

        Parameters
        ----------
        lon : float
            Longitude of point to write data for
        lat : float
            Latitude of point to write data for
        df : pd.DataFrame
            DataFrame with variables in columns and z-dimension values as index.
        """

        index = df.index.to_numpy()
        data = {k : df[k].values for k in df.columns}

        if not np.all(np.equal(index, self.ds[self.z_name].values)):
            raise IndexError('Index in the passed data'
                             ' frame do not correspond with z values of dataset')

        self._write_ser(data, lon=lon, lat=lat)

    def write_point(self, lon, lat, z, data):
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

        kwargs = {'lon': lon, 'lat': lat, self.z_name: z}
        self._write_pt(data, **kwargs)






