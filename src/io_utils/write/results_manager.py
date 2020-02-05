# -*- coding: utf-8 -*-

"""
Xarray Stacked Images Writer.
Create 3D datasets, allows setting spatial and temporal subset (images and time
series)
"""

import xarray as xr
import numpy as np
import pandas as pd
from datetime import datetime
import warnings
import matplotlib.pyplot as plt
import os
from io_utils.utils import safe_arange
from pygeogrids.grids import BasicGrid, CellGrid, lonlat2cell

def minmax(values):
    return np.nanmin(values), np.nanmax(values)

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
        diff_x, diff_y = np.diff(sorted(np.unique(lons))), np.diff(sorted(np.unique(lats)))

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

class RegularStackDataResultsManager(object):

    """ Store netcdf cubes with xarray and dask """

    def __init__(self, dx=0.25, dy=0.25, z=None, z_name='z',
                 llc=Point(-179.875, -89.875), urc=Point(179.875, 89.875),
                 indexed=True, zlib=True, fill_value=9999., chunksize=5.):

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

        self.zlib = zlib
        self.z_name = z_name
        self.fill_value = fill_value

        self.llc, self.urc = llc, urc

        lons, lats = self._coords(dx, dy)
        self.shape = (z.size, lats.size, lons.size)

        gpis = self._gpis('ll') # origin is in the lower left

        self.ds = xr.Dataset(data_vars={'gpi': (['lat', 'lon'], gpis)} if indexed else None,
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

    def _add_empty_2d(self, name):
        # add a empty variable without z dimension of the passed name
        print('Add empty 2D variable {}'.format(name))
        shape = (self.shape[1], self.shape[2])
        self.ds[name] = \
            xr.DataArray(np.full(shape, self.fill_value), dims=['lat', 'lon'],
                         coords=[self.ds.lat, self.ds.lon])

    def _add_empty_3d(self, name):
        # add a empty variable with z dimension of the passed name
        print('Add empty 3D variable {}'.format(name))
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

    def store_stack(self, filename=None, dtypes=np.float32):
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
            if any([isinstance(z, dt) for dt in datetime_obs]):
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
        Add data for a single location. Series is in z-dimension.

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


def usecase_time():
    ### TS case
    time_case = False

    from smecv_grid import SMECV_Grid_v052
    if time_case:
        index = pd.date_range('2000-01-01', '2000-12-31', freq='D')
        z = pd.to_datetime(index).to_pydatetime()
    else:
        index = np.array(list(range(1, 367)))
        z = index

    glob_grid = SMECV_Grid_v052(None)
    land_grid = SMECV_Grid_v052('land')


    ts_writer = RegularStackDataResultsManager(dx=0.25, dy=0.25, z=z, z_name='doy')

    gpis, lons, lats, cells = land_grid.get_grid_points()
    i=0
    for lon, lat in zip(lons, lats):
        if i > 1000: break
        print(i)
        data = pd.DataFrame(index=index,
                            data={'var_{}'.format(i): np.random.rand(366) for i in range(5)})
        ts_writer.write_series(lon, lat, data)
        i+=1

    import time
    start = time.time()
    ts_writer.store_files(r"C:\tmp\collect")
    #writer.store_stack(r"C:\tmp\test.nc")
    end = time.time()
    print('Writing file took {} seconds'.format(end - start))

if __name__ == '__main__':
    time_case = False

    from smecv_grid import SMECV_Grid_v052
    if time_case:
        index = pd.date_range('2000-01-01', '2000-12-31', freq='D')
        z = pd.to_datetime(index).to_pydatetime()
    else:
        index = np.array(list(range(1, 367)))
        z = index

    glob_grid = SMECV_Grid_v052(None)
    land_grid = SMECV_Grid_v052('land')


    ### AREA case
    img_writer = RegularStackDataResultsManager(dx=0.25, dy=0.25, z=z, z_name='doy')

    gpis, lons, lats, cells = land_grid.get_grid_points()
    i=0
    for cell in np.unique(cells):
        print(cell)
        cell_gpis, cell_lons, cell_lats = land_grid.grid_points_for_cell(cell)
        df = pd.DataFrame(index=range(cell_gpis.size), data={'lon': cell_lons,
                                                             'lat': cell_lats,
                                                             'var1': np.random.rand(cell_gpis.size),
                                                             'var2': np.random.rand(cell_gpis.size)})
        img_writer.write_image(df, z=1)
        i+=1

    import time
    start = time.time()
    img_writer.store_stack(r"C:\tmp\test.nc")
    #writer.store_stack(r"C:\tmp\test.nc")
    end = time.time()
    print('Writing file took {} seconds'.format(end - start))



