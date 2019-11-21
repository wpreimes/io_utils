# -*- coding: utf-8 -*-
from multi_reader import MultiReader
from pynetcf.time_series import GriddedNcOrthoMultiTs
import os
import pygeogrids
from pygeogrids.netcdf import load_grid
import sys
from rsroot import root_path
from old.ESA_CCI_interface import ESA_CCI_SM_cfg
import pandas as pd
import numpy as np
from ismn.interface import ISMN_Interface
from collections import OrderedDict
import copy


def cci_fract(cci_product_name):
    """
    Get the parameter  and the version from the passed CCI product name
    Parameters
    ----------
    cci_product_name : str
        The string that is evaluated

    Returns
    -------
    version : str
        Version string (eg: 3.2 or 4.1)
    product : str
        Product string (eg: ACTIVE, PASSIVE, COMBINED_ADJUSTED)
    """

    parts = cci_product_name.split('_')

    version, product = parts[1], parts[2:]
    product = '_'.join(product)
    version = '%s.%s' % (version[0], version[1])

    return version, product


def cfg_path_for_version(version):
    """
    Get the path of the config file for reading CCI data.
    For each supported version a file with the version number in the name
    must be there

    Parameters
    -------
    version : str
        CCI version corresponding to the name of the cdf file.
        e.g. '4.4'
    Returns
    -------
    cfg_file : str
        Path to the config file for the current OS
    """

    if 'win' in sys.platform:
        cfg_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'cci_cfg_local', 'win', 'ESA_CCI_SM_v0{}.cfg'.format(version))
    else:
        cfg_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'cci_cfg_local', 'linux', 'ESA_CCI_SM_v0{}.cfg'.format(version))

    return cfg_file


class ISMNTs(ISMN_Interface):
    """
    Modified ISMN Reader class, that reads good (G Flag) ISMN values and provides
    functions for reading the station closest to a passed lonlat tuple.
    """

    def __init__(self, path_to_data, resample='D', network=None, scale_factors=None):
        """
        Initialize the reader for ISMN data

        Parameters
        ----------
        path_to_data : str
            Path to the downloaded ISMN data
        resample : str, optional (default: D)
            Resample the ISMN observations before returning them
        network : string or list, optional
            Provide name of network to only load the given network
        scale_factors : dict, optional (default:None)
            Apply the passed multiplicative scales to the selected columns
        """
        self.resample = resample
        self.good_flags = ['G']  # good flags (that are actually read)
        self.variable = 'soil moisture'  # read only SM in this class
        self.scale_factors = scale_factors
        super(ISMNTs, self).__init__(path_to_data, network)

    def read_G_sm_idx(self, idx):
        df = super(ISMNTs, self).read_ts(idx)
        for n, s in self.scale_factors.items():
            if n in df.columns: df[n] *= s

        sm_flag_dat_col_name = '{}_flag'.format(self.variable)
        # filter with flags
        df = df[self.variable].loc[df[sm_flag_dat_col_name].isin(self.good_flags)].to_frame(self.variable)

        df.index = df.index.tz_localize(None)

        if self.resample:
            df = df.resample(self.resample).mean()

        return df

    def read_G_sm_nearest_station(self, lon, lat, min_depth=0, max_depth=999,
                                  max_dist=30000, return_distance=True):
        """
        Read good (G-flagged) time series values for the station closest to the
        passed lon, lat in the passed depths.

        Parameters
        ----------
        lon : float
            Longitude of the point to find the nearest station for
        lat : float
            Latitude of the point to find the nearest station for
        min_depth : float, optional (default: 0)
            The minimum valid depth in m
        max_depth : float, optional (default: 999)
            The maximum valid depth in m
        max_dist : int
            Maximum allowed distance between the passed lon/lat position and the
            actually found nearest station. If the distance is large, no data is read.
        return_distance : bool
            Also return the distance (2 return values), else 1 return value

        Returns
        -------
        data : pd.DataFrame
            Data measured at the station
        distance : float
            Distance between the passed coordinates and the read station.
        """
        ts_for_station = []
        nearest_station, distance = self.find_nearest_station(lon, lat, True)

        if distance > max_dist:
            print('No station within the selected distance: {}'.format(max_dist))
            df_for_station = None
            distance = None
        else:
            str_flags = ''.join(self.good_flags)

            depths_from, depths_to = nearest_station.get_depths(self.variable)
            for depth_from, depth_to in zip(depths_from, depths_to):
                if (depth_from < min_depth) or (depth_to > max_depth):
                    # skip depths outside of the passed range
                    continue

                sensors = nearest_station.get_sensors(self.variable, depth_from, depth_to)
                for sensor in sensors:
                    dat = nearest_station.read_variable(self.variable,
                                                        depth_from=depth_from,
                                                        depth_to=depth_to,
                                                        sensor=sensor)

                    if self.scale_factors is not None and self.variable in list(self.scale_factors.keys()):
                        dat.data[self.variable] *= self.scale_factors[self.variable]
                    name = '{var}_{network}_{station}_{flags}_{df}-{dt}_{sensor}'
                    name = name.format(var=self.variable, network=dat.network,
                                       flags=str_flags, station=dat.station,
                                       df=depth_from, dt=depth_to, sensor=sensor)

                    sm_flag_dat_col_name = '{}_flag'.format(self.variable)
                    data = dat.data[self.variable].loc[dat.data[sm_flag_dat_col_name].isin(self.good_flags)].to_frame(
                        name)
                    ts_for_station.append(data)
            df_for_station = pd.concat(ts_for_station, axis=1)

            df_for_station.index = df_for_station.index.tz_localize(None)

            if self.resample:
                df_for_station = df_for_station.resample(self.resample).mean()

        if return_distance:
            return df_for_station, distance
        else:
            return df_for_station

    def read_longest_G_sm_nearest_station(self, lon, lat, min_depth=0, max_depth=999,
                                          max_dist=30000):
        """
        Read one single (the longest) SM time series from the nearest station in
        the valid depth range provided.

        Parameters
        ----------
        lon : float
            Longitude of the point to find the nearest station for
        lat : float
            Latitude of the point to find the nearest station for
        min_depth : float, optional (default: 0)
            The minimum valid depth in m
        max_depth : float, optional (default: 999)
            The maximum valid depth in m
        max_dist : int
            Maximum allowed distance between the passed lon/lat position and the
            actually found nearest station. If the distance is large, no data is read.

        Returns
        -------
        longest_sm_ts : pd.DataFrame
            The longest SM time series in the valid depth for the nearest station.
        """
        df, dist = self.read_G_sm_nearest_station(lon, lat, min_depth, max_depth,
                                                  max_dist=max_dist)
        if df is None:
            return None, None

        n_max = 0
        max_col = None

        for col in df.columns:
            ts = df[col].dropna()
            n_col = ts.index.values.size
            if n_col > n_max:
                n_max = n_col
                max_col = col

        return df[[max_col]].rename(columns={max_col: 'soil moisture'}), dist


class CCITs(object):
    """
    Read CCI SM (flagged) data
    """

    def __init__(self, version, product, dropna=True, cfg_file=None, read_flags=None,
                 grid=None, resample='D', scale_factors=None, **kwargs):
        """
        Read a CCI time series

        Parameters
        ----------
        version : str
            Version string of the CCI product to read
        product : str
            product to read from the file
        dropna : bool
            Replace 9999 with nans
        cfg_file : str, optional (default: None)
            path to the config file for reading the cci data
            If None is passed we search one a default directory
                (../data-read-write/cci_cfg_local/<os>)
        read_flags : list, optional (default: [0])
            List of flags for which we read observations, others are not read
            and not in the returned data frame!
            If None is passed, all vales are returned.
        grid : pygeogrids.CellGrid, optional (default: None)
            Grid to use for reading, if None is passed the one from the cfg file is
            used.
        resample : str, optional (default: D)
            How the data frame is resampled after reading
        scale_factors : dict, optional (default: None)
            Multiplicative scale factor (item) for the columns (key)
        kwargs : dict, optional
            Other kwargs to use (e.g ioclass_kws or parameters)
        """
        self.resample = resample
        self.dropna = dropna
        self.product = product
        self.scale_factors = scale_factors
        self.reader = ESA_CCI_SM_cfg(version='ESA_CCI_SM_v0%s' % version,
                                     product=product, cfg_file=cfg_file, grid=grid,
                                     **kwargs)
        self.read_flags = read_flags
        if self.read_flags is not None:
            self.read_flags = list([read_flags]) if not isinstance(read_flags, list) else read_flags
            self.flag_name = 'flag'
            if ('parameter' in kwargs.keys()) and (self.flag_name not in kwargs['parameter']):
                kwargs.parameters.append(self.flag_name)

        self.grid = self.reader.grid  # type: pygeogrids.CellGrid

    def read_ts(self, *args):
        try:
            df_cci = pd.DataFrame(self.reader.read(*args))
        except IOError:
            df_cci = pd.DataFrame()

        if 'sm_noise' in df_cci.columns:
            df_cci = df_cci.rename(columns={'sm_noise': 'sm_uncertainty'})

        if df_cci.empty:
            if 'ADJUSTED' in self.product:
                return pd.DataFrame(columns=['adjusted'])
            else:
                return pd.DataFrame(columns=['sm', 'sm_uncertainty', 'flag'])

        if self.scale_factors is None:
            raise ValueError(self.scale_factors,
                             "Need to pass scale factors to define the SM col")

        sm_col = list(self.scale_factors.keys())[0]

        if self.read_flags is not None:
                df_cci = df_cci.loc[df_cci[self.flag_name].isin(self.read_flags), :]
                df_cci = df_cci.drop(columns=[self.flag_name])

        if not df_cci.empty:
            if 'ADJUSTED' in self.product:
                if self.dropna:
                    df_cci = df_cci.dropna(subset=[sm_col])
            else:
                placeholder = np.nanmin(df_cci[sm_col])

                # just so we never delete any actual data:
                if placeholder not in [-9999., -999999., -999900.]:
                    placeholder = -9999.

                for col in df_cci.columns:
                    df_cci.loc[df_cci[col] == placeholder, col] = np.nan

                if self.dropna:
                    df_cci = df_cci.dropna(subset=[sm_col])

        if not df_cci[sm_col].empty:
            for col, sf in self.scale_factors.items():
                if col in df_cci.columns:
                    df_cci[col] *= sf

        if self.resample:
            df_cci = df_cci.resample(self.resample).mean()

        return df_cci


#####C3S######################################################################
class C3STs(object):
    def __init__(self, tcdr_path, icdr_path=None, grid_path=None, read_flags=None,
                 dropna=True, scale_factors=None, resample='D',  **kwargs):
        """
        Read a C3S time series

        Parameters
        ----------
        tcdr_path : str
            Path to the TCDR time series
        icdr_path : str, optional (default: None)
            Path to the ICDR time series
        grid_path : str, optional (default: None)
            Path to the grid file to use, if None is passed, find the grid.nc in
            the TCDR path
        read_flags : tuple, optional (default: [0])
            List of flags for which we read observations, others are not read
            and not in the returned data frame!
            If None is passed, all vales are returned.
        dropna : bool, optional (default: True)
            Replace missing values in the SM column with nans
        resample : str, optional (default: D)
            How the data frame is resampled after reading
        scale_factors : dict, optional (default: None)
            Multiplicative scale factor (item) for the columns (key)
        kwargs : dict, optional
            Other kwargs to use (e.g ioclass_kws or parameters)
        """

        if grid_path is None:
            grid_path = os.path.join(tcdr_path, "grid.nc")

        self.read_flags = read_flags
        if self.read_flags is not None:
            self.read_flags = list([read_flags]) if not isinstance(read_flags, list) else read_flags
            self.flag_name = 'flag'
            if ('parameters' in kwargs.keys()) and (self.flag_name not in kwargs['parameters']):
                kwargs['parameters'].append(self.flag_name)

        self.scale_factors = scale_factors
        self.dropna = dropna
        self.resample = resample
        self.grid = load_grid(grid_path)
        self.tcdr = GriddedNcOrthoMultiTs(tcdr_path, self.grid, **kwargs)
        if icdr_path:
            self.icdr = GriddedNcOrthoMultiTs(icdr_path, self.grid, **kwargs)
        else:
            self.icdr = None


    def read_ts(self, *args, **kwargs):
        df = self.tcdr.read(*args, **kwargs)
        if self.icdr:
            df_icdr = self.icdr.read(*args, **kwargs)
            df = pd.concat([df, df_icdr], axis=0)

        sm_col = list(self.scale_factors.keys())[0]

        if self.dropna:
            placeholder = np.nanmin(df[sm_col])
            # just so we never delete any actual data:
            if placeholder not in [-9999., -999999., -999900.]:
                placeholder = -9999.
            for col in df.columns:
                df.loc[df[col] == placeholder, col] = np.nan
            df = df.dropna(subset=[sm_col])

        if not df[sm_col].empty:
            for col, sf in self.scale_factors.items():
                if col in df.columns:
                    df[col] *= sf

        if self.read_flags is not None:
            df = df.loc[df[self.flag_name].isin(self.read_flags), :]
            df = df.drop(columns=[self.flag_name])

        if self.resample:
            df = df.resample(self.resample).mean()

        return df


#####ECMWF-models################################################################
class ERATs(GriddedNcOrthoMultiTs):

    def __init__(self, ts_path, grid_path=None, resample='D', **kwargs):
        if grid_path is None:
            grid_path = os.path.join(ts_path, "grid.nc")

        self.resample = resample
        grid = load_grid(grid_path)
        super(ERATs, self).__init__(ts_path, grid, **kwargs)

    def read_ts(self, *args, **kwargs):
        df = super(ERATs, self).read_ts(*args, **kwargs)
        if self.resample:
            df = df.resample(self.resample).mean()

        return df


#####MERRA#####################################################################
class MERRATs(GriddedNcOrthoMultiTs):
    """
    Read reshuffled hourly or monthly merra2 ts data under a given path.
    """

    def __init__(self, ts_path=None, grid_path=None, resample='D', **kwargs):
        if grid_path is None:
            grid_path = os.path.join(ts_path, "grid.nc")

        self.resample = resample
        grid = load_grid(grid_path)
        super(MERRATs, self).__init__(ts_path, grid, **kwargs)

    def read(self, *args, **kwargs):
        df = super(MERRATs, self).read(*args, **kwargs)

        if self.resample:
            df = df.resample(self.resample).mean()
        return df


class GLDASTs(GriddedNcOrthoMultiTs):
    def __init__(self, ts_path, grid_path=None, resample='D', **kwargs):
        if grid_path is None:
            grid_path = os.path.join(ts_path, "grid.nc")
        self.resample = resample

        grid = load_grid(grid_path)
        super(GLDASTs, self).__init__(ts_path, grid, **kwargs)

    def read(self, *args, **kwargs):
        df = super(GLDASTs, self).read(*args, **kwargs)

        if self.resample:
            df = df.resample(self.resample).mean()
        return df


def ts_data_path(name, force_r):
    """
    Get the paths for the selected product.

    Parameters
    ----------
    name : str
        Name of the product to read.
    force_r : bool
        Set True to force reading from R:

    Returns
    -------

    """
    ############################# ECMWF products ###################################
    if name == 'ERAINT':
        if 'win' in sys.platform:
            path = os.path.join(root_path.d, 'data-read', 'ERAINT', 'netcdf')
        else:
            path = os.path.join('/', 'data-read', 'USERS', 'wpreimes', 'ERAINT',
                                'netcdf')

        if os.path.isdir(path) and not force_r:
            print('Found local files for ERA Interim 6H data')
        else:
            print('Found no local files for ERA Interim 6H data. Use data on R.')
            path = os.path.join(root_path.r, 'Datapool_processed', 'ECMWF_reanalysis',
                                'ERAINT', 'datasets', 'netcdf')


    elif name == 'ERA_LAND_GBG4':
        if 'win' in sys.platform:
            path = os.path.join(root_path.d, 'data-read', 'ERALand_gbg4',
                                'netcdf')
        else:
            path = os.path.join('/', 'data-read', 'USERS', 'wpreimes', 'ERALand_gbg4',
                                'netcdf')

        if os.path.isdir(path) and not force_r:
            print('Found local files for ERA Land gbg4 6H data')
        else:
            print('Found no local files for ERA Land gbg4 6H data. Use data on R.')
            path = os.path.join(root_path.r, 'Datapool_processed',
                                'ECMWF_reanalysis', 'ERALAND', 'datasets',
                                'netcdf_gbg4')

    elif name == 'ERA_INTERIM_LAND':
        if 'win' in sys.platform:
            path = os.path.join(root_path.d, 'data-read', 'ERA_Interim_Land', 'datasets',
                                'netcdf')
        else:
            path = os.path.join('/', 'data-read', 'USERS', 'wpreimes', 'ERA_Interim_Land',
                                'netcdf')

        if os.path.isdir(path) and not force_r:
            print('Found local files for ERA Interim Land data')
        else:
            print('Found no local files for ERA Interim Land data. Use data on R.')
            path = os.path.join(root_path.r, 'Datapool_processed',
                                'ECMWF_reanalysis', 'ERA_Interim_Land', 'datasets',
                                'netcdf')

    elif name == 'ERA5':
        if 'win' in sys.platform:
            path = os.path.join(root_path.d, 'data-read', 'ERA5', 'timeseries', 'netcdf')
        else:
            path = os.path.join('/', 'data-read', 'USERS', 'wpreimes', 'ERA5', 'timeseries',
                                'netcdf')

        if os.path.isdir(path) and not force_r:
            print('Found local files for ERA5 6H data')
        else:
            print('Found no local files for ERA5 6H data. Use data on R.')
            path = os.path.join(root_path.r, 'Datapool_processed', 'ECMWF_reanalysis',
                                'ERA5', 'datasets', 'netcdf')


    elif name == 'ERA5-Land':
        if 'win' in sys.platform:
            path = os.path.join(root_path.d, 'data-read', 'ERA5-Land', 'sm_lai_precip',
                                'timeseries', 'netcdf')
        else:
            path = os.path.join('/', 'data-read', 'USERS', 'wpreimes', 'ERA5-Land',
                                'sm_lai_precip', 'timeseries', 'netcdf')

        if os.path.isdir(path) and not force_r:
            print('Found local files for ERA5-Land data')
        else:
            print('Found no local files for ERA5-Land data. Use data on R.')
            path = os.path.join(root_path.r, 'Datapool_processed', 'ECMWF_reanalysis',
                                'ERA5-Land', 'datasets', 'soilmoisture_lai')
    ############################# GLDAS products ###################################

    elif name == 'GLDAS1':
        if 'win' in sys.platform:
            path = os.path.join(root_path.d, 'data-read', 'GLDAS_v1',
                                'netcdf')
        else:
            path = os.path.join('/', 'data-read', 'USERS', 'wpreimes', 'GLDAS_v1',
                                'netcdf')

        if os.path.isdir(path):
            print('Found local files for GLDAS1 3H data')
        else:
            print('Found no local files for GLDAS v1 3H data. Use data on R.')
            path = os.path.join(root_path.r, 'Datapool_processed', 'GLDAS',
                                'GLDAS_NOAH025SUBP_3H', 'datasets', 'netcdf')


    elif name == 'GLDAS2.0':
        if 'win' in sys.platform:
            path = os.path.join(root_path.d, 'data-read', 'GLDAS_v2',
                                'netcdf')
        else:
            path = os.path.join('/', 'data-read', 'USERS', 'wpreimes',
                                'GLDAS_v2', 'netcdf')

        if os.path.isdir(path):
            print('Found local files for GLDAS v2 3H data')
        else:
            print('Found no local files for GLDAS v2 3H data. Use data on R.')
            path = os.path.join(root_path.r, 'Datapool_processed', 'GLDAS',
                                'GLDAS_NOAH025_3H.020', 'datasets',
                                'netcdf_reprocessed')

    elif name == 'GLDAS2.1':
        if 'win' in sys.platform:
            path = os.path.join(root_path.d, 'data-read', 'GLDAS_v21', 'netcdf')
        else:
            path = os.path.join('/', 'data-read', 'USERS', 'wpreimes', 'GLDAS_v21',
                                'netcdf')

        if os.path.isdir(path):
            print('Found local files for GLDAS v21 3H data')
        else:
            print('Found no local files for GLDAS v21 3H data. Use data on R.')
            path = os.path.join(root_path.r, 'Datapool_processed', 'GLDAS',
                                'GLDAS_NOAH025_3H.2.1', 'datasets', 'netcdf')

    ############################# MERRA products ###################################
    elif name == 'MERRA2':
        if 'win' in sys.platform:

            path = os.path.join(root_path.d, 'data-read', 'MERRA2_D', 'M2T1NXLND.5.12.4_6hourly')
        else:
            path = os.path.join('/', 'data-read', 'USERS', 'wpreimes', 'MERRA2_D',
                                'M2T1NXLND.5.12.4_6hourly')

        if os.path.isdir(path):
            print('Found local files for daily merra2')
        else:
            print('Found no local files for daily merra2. Use data on R.')
            path = os.path.join(root_path.r, 'Datapool_processed', 'Earth2Observe',
                                'MERRA2', 'M2T1NXLND.5.12.4_6hourly')

    ################################ C3s ######################################
    elif name == 'C3S_COMBINED_v201706':
        if 'win' in sys.platform:
            path_tcdr = os.path.join(
                root_path.d, 'data-read', 'C3S', 'v201706', 'TCDR', '063_images_to_ts', 'combined-daily')
            path_icdr = os.path.join(
                root_path.d, 'data-read', 'C3S', 'v201706', 'ICDR', '063_images_to_ts', 'combined-daily')
        else:
            path_tcdr = os.path.join(
                '/' 'data-read', 'USERS', 'wpreimes', 'C3S', 'v201706', 'TCDR', '063_images_to_ts',
                'combined-daily')
            path_icdr = os.path.join(
                '/' 'data-read', 'USERS', 'wpreimes', 'C3S', 'v201706', 'ICDR', '063_images_to_ts',
                'combined-daily')

        if os.path.isdir(path_tcdr):
            print('Found local files for daily C3S 201706 TCDR')
        else:
            print('Found no local files for daily C3S 201706 TCDR. Use data on R.')
            path_tcdr = os.path.join(
                root_path.r, 'Datapool_processed', 'C3S', 'v201706', 'TCDR',
                '063_images_to_ts', 'combined-daily')

        if os.path.isdir(path_icdr):
            print('Found local files for daily C3S 201706 ICDR')
        else:
            print('Found no local files for daily C3S 201706 ICDR. Use data on R.')
            path_icdr = os.path.join(
                root_path.r, 'Datapool_processed', 'C3S', 'v201706', 'ICDR',
                '063_images_to_ts', 'combined-daily')
            if not os.path.isdir(path_icdr):
                print('No ICDR data found on R, using TCDR only')
                path_icdr = None

        path = {'TCDR': path_tcdr, 'ICDR': path_icdr}

    elif name == 'C3S_COMBINED_v201812':
        if 'win' in sys.platform:
            path_tcdr = os.path.join(
                root_path.d, 'data-read', 'C3S', 'v201812', 'TCDR', '063_images_to_ts', 'combined-daily')
            path_icdr = os.path.join(
                root_path.d, 'data-read', 'C3S', 'v201812', 'ICDR', '063_images_to_ts', 'combined-daily')
        else:
            path_tcdr = os.path.join(
                '/' 'data-read', 'USERS', 'wpreimes', 'C3S', 'v201812', 'TCDR', '063_images_to_ts',
                'combined-daily')
            path_icdr = os.path.join(
                '/' 'data-read', 'USERS', 'wpreimes', 'C3S', 'v201812', 'ICDR', '063_images_to_ts',
                'combined-daily')

        if os.path.isdir(path_tcdr):
            print('Found local files for COMBINED daily C3S 201812 TCDR')
        else:
            print('Found no local files for COMBINED daily C3S 201812 TCDR. Use data on R.')
            path_tcdr = os.path.join(
                root_path.r, 'Datapool_processed', 'C3S', 'v201812', 'TCDR',
                '063_images_to_ts', 'combined-daily')

        if os.path.isdir(path_icdr):
            print('Found local files for COMBINED daily C3S 201812 ICDR')
        else:
            print('Found no local files for COMBINED daily C3S 201812 ICDR. Use data on R.')
            path_icdr = os.path.join(
                root_path.r, 'Datapool_processed', 'C3S', 'v201812', 'ICDR',
                '063_images_to_ts', 'combined-daily')
            if not os.path.isdir(path_icdr):
                print('No COMBINED ICDR data found on R, using TCDR only')
                path_icdr = None

        path = {'TCDR': path_tcdr, 'ICDR': path_icdr}

    elif name == 'C3S_ACTIVE_v201812':
        if 'win' in sys.platform:
            path_tcdr = os.path.join(
                root_path.d, 'data-read', 'C3S', 'v201812', 'TCDR', '063_images_to_ts', 'active-daily')
            path_icdr = os.path.join(
                root_path.d, 'data-read', 'C3S', 'v201812', 'ICDR', '063_images_to_ts', 'active-daily')
        else:
            path_tcdr = os.path.join(
                '/' 'data-read', 'USERS', 'wpreimes', 'C3S', 'v201812', 'TCDR', '063_images_to_ts',
                'active-daily')
            path_icdr = os.path.join(
                '/' 'data-read', 'USERS', 'wpreimes', 'C3S', 'v201812', 'ICDR', '063_images_to_ts',
                'active-daily')

        if os.path.isdir(path_tcdr):
            print('Found local files for daily ACTIVE C3S 201812 TCDR')
        else:
            print('Found no local files for daily ACTIVE C3S 201812 TCDR. Use data on R.')
            path_tcdr = os.path.join(
                root_path.r, 'Datapool_processed', 'C3S', 'v201812', 'TCDR',
                '063_images_to_ts', 'active-daily')

        if os.path.isdir(path_icdr):
            print('Found local files for daily ACTIVE C3S 201812 ICDR')
        else:
            print('Found no local files for daily ACTIVE C3S 201812 ICDR. Use data on R.')
            path_icdr = os.path.join(
                root_path.r, 'Datapool_processed', 'C3S', 'v201812', 'ICDR',
                '063_images_to_ts', 'active-daily')
            if not os.path.isdir(path_icdr):
                print('No ACTIVE ICDR data found on R, using TCDR only')
                path_icdr = None

        path = {'TCDR': path_tcdr, 'ICDR': path_icdr}

    elif name == 'C3S_PASSIVE_v201812':
        if 'win' in sys.platform:
            path_tcdr = os.path.join(
                root_path.d, 'data-read', 'C3S', 'v201812', 'TCDR', '063_images_to_ts', 'passive-daily')
            path_icdr = os.path.join(
                root_path.d, 'data-read', 'C3S', 'v201812', 'ICDR', '063_images_to_ts', 'passive-daily')
        else:
            path_tcdr = os.path.join(
                '/' 'data-read', 'USERS', 'wpreimes', 'C3S', 'v201812', 'TCDR', '063_images_to_ts',
                'passive-daily')
            path_icdr = os.path.join(
                '/' 'data-read', 'USERS', 'wpreimes', 'C3S', 'v201812', 'ICDR', '063_images_to_ts',
                'passive-daily')

        if os.path.isdir(path_tcdr):
            print('Found local files for daily PASSIVE C3S 201812 TCDR')
        else:
            print('Found no local files for daily PASSIVE C3S 201812 TCDR. Use data on R.')
            path_tcdr = os.path.join(
                root_path.r, 'Datapool_processed', 'C3S', 'v201812', 'TCDR',
                '063_images_to_ts', 'passive-daily')

        if os.path.isdir(path_icdr):
            print('Found local files for daily PASSIVE C3S 201812 ICDR')
        else:
            print('Found no local files for daily PASSIVE C3S 201812 ICDR. Use data on R.')
            path_icdr = os.path.join(
                root_path.r, 'Datapool_processed', 'C3S', 'v201812', 'ICDR',
                '063_images_to_ts', 'passive-daily')
            if not os.path.isdir(path_icdr):
                print('No PASSIVE ICDR data found on R, using TCDR only')
                path_icdr = None

        path = {'TCDR': path_tcdr, 'ICDR': path_icdr}

    ############################# ISMN products ###################################
    elif name == 'ISMN_USA':
        if 'win' in sys.platform:
            path = os.path.join(root_path.d, 'data-read', 'ISMN', 'USA')
        else:
            path = os.path.join('/', 'data-read', 'USERS', 'wpreimes', 'ISMN',
                                'USA')

        if os.path.isdir(path):
            print('Found local files for USA ISMN data')
        else:
            raise ValueError(name, 'No data on R: for some reason')
    elif name == 'ISMN_selection':
        if 'win' in sys.platform:
            path = os.path.join(root_path.d, 'data-read', 'ISMN', 'global_selection')
        else:
            path = os.path.join('/', 'data-read', 'USERS', 'wpreimes', 'ISMN_selection',
                                'global_selection')

        if os.path.isdir(path):
            print('Found local files for good, global ISMN data')
        else:
            raise ValueError(name, 'No data on R: for some reason')

    elif name == 'ISMN_global':
        if 'win' in sys.platform:
            path = os.path.join(root_path.d, 'data-read', 'ISMN', 'global')
        else:
            path = os.path.join('/', 'data-read', 'USERS', 'wpreimes', 'global',
                                'global_selection')

        if os.path.isdir(path):
            print('Found local files for global ISMN data')
        else:
            raise ValueError(name, 'No data on R: for some reason')

    else:
        raise NameError(name, 'No pathes for the selected product stored.')

    return path


def col_scalef(name):
    """
    Set specific scale factors for columns of the datasets

    Parameters
    ----------
    name : str
        Product name

    Returns
    -------
    cols_scalef : dict
        Variable columns and according scale factors that the reader must apply
    """

    # perferred SM columns must be the first element!!!!!!!!!!!!!!!!!!

    if 'CCI' in name:
        if 'ADJUSTED' in name:
            return OrderedDict([('adjusted', 1.)])
        else:
            # it is always called uncertainty!!
            return OrderedDict([('sm', 1.), ('sm_uncertainty', 1.)])

    if name == 'ERAINT':
        return OrderedDict([('swvl1', 1.), ('swvl2', 1.), ('swvl3', 1.), ('swvl4', 1.)])
    elif name == 'ERA_LAND':
        return OrderedDict([('sm_era', 1.)])
    elif name == 'ERA_LAND_GBG4':
        return OrderedDict([('39', 1.), ('40', 1.), ('41', 1.), ('42', 1.)])
    elif name == 'ERA_INTERIM_LAND':
        return OrderedDict([('sm_era', 1.)])
    elif name == 'ERA5':
        return OrderedDict([('swvl1', 1.)])
    elif name == 'ERA5-Land':
        return OrderedDict([('swvl1', 1.)])
    elif name == 'GLDAS1':
        return OrderedDict([('086_L1', 0.01)])
    elif name == 'GLDAS2.0':
        return OrderedDict([('SoilMoi0_10cm_inst', 0.01), ('SoilMoi100_200cm_inst', 0.01),
                            ('SoilMoi10_40cm_inst', 0.01), ('SoilMoi40_100cm_inst', 0.01)])
    elif name == 'GLDAS2.1':
        return OrderedDict([('SoilMoi0_10cm_inst', 0.01), ('SoilMoi100_200cm_inst', 0.01),
                            ('SoilMoi10_40cm_inst', 0.01), ('SoilMoi40_100cm_inst', 0.01)])
    elif name == 'MERRA2':
        return OrderedDict([('SFMC', 1.), ('GWETTOP', 1.)])
    elif name in ['ISMN_global', 'ISMN_selection', 'ISMN_USA']:
        return OrderedDict([('soil moisture', 1.)])
    elif name in ['C3S_COMBINED_v201706', 'C3S_COMBINED_v201812',
                  'C3S_ACTIVE_v201706', 'C3S_ACTIVE_v201812',
                  'C3S_PASSIVE_v201706', 'C3S_PASSIVE_v201812']:
        return OrderedDict([('sm', 1.), ('sm_uncertainty', 1.)])

    else:
        raise NameError('Selected product {} is not supported, check spelling'.format(name))

def load_ts_reader(product, force_r=False, **kwargs):
    """
    Get the reader for the product

    Parameters
    ----------
    product : str
        Name of the product to get the reader for
    force_r : bool
        Force to create a reader that uses default data paths on R:
    kwargs: dict
        Other kwargs that are passed to the respective reader
            dropna : bool
            scale_factors : dict (col_name : scale_factor)

    Returns
    -------
    reader :
        The reader class

    """
    reader_kwargs = copy.deepcopy(kwargs)

    if 'scale_factors' not in kwargs.keys():
        scale_factors = col_scalef(product)
    else:
        scale_factors = reader_kwargs.pop('scale_factors')

    if 'CCI' in product:
        version, cciprod = cci_fract(product)
        if 'cfg_file' not in reader_kwargs.keys():
            cfg_path = cfg_path_for_version(version)
            reader_kwargs['cfg_file'] = cfg_path

        reader = CCITs(version=version, product=cciprod,
                       scale_factors=scale_factors, **reader_kwargs)
    else:
        ts_path = ts_data_path(product, force_r=force_r)
        if product in ['ERA_INTERIM_LAND', 'ERA_LAND_GBG4', 'ERA5', 'ERAINT', 'ERA5-Land']:
            reader = ERATs(ts_path=ts_path, scale_factors=scale_factors, **reader_kwargs)
        elif product in ['GLDAS1', 'GLDAS2.0', 'GLDAS2.1']:
            reader = GLDASTs(ts_path, scale_factors=scale_factors, **reader_kwargs)
        elif product in ['MERRA2']:
            reader = MERRATs(ts_path, scale_factors=scale_factors, **reader_kwargs)
        elif product in ['ISMN_global', 'ISMN_selection', 'ISMN_USA']:
            reader = ISMNTs(ts_path, scale_factors=scale_factors, **reader_kwargs)  # no bulk reader
        elif product in ['C3S_COMBINED_v201706', 'C3S_COMBINED_v201812',
                         'C3S_ACTIVE_v201706', 'C3S_ACTIVE_v201812',
                         'C3S_PASSIVE_v201706', 'C3S_PASSIVE_v201812',]:
            tcdr_path = ts_path['TCDR']
            icdr_path = ts_path['ICDR']
            reader = C3STs(tcdr_path=tcdr_path, icdr_path=icdr_path,
                scale_factors=scale_factors, **reader_kwargs)
        else:
            raise NameError('Selected product {} is not supported, check spelling'.format(product))

    return reader


def usecase_MultiReader():
    reader = MultiReader(dataset_cols={'CCI_44_COMBINED': ['sm', 'sm_uncertainty'],
                                       'CCI_45_COMBINED': ['sm', 'sm_uncertainty'],
                                       'C3S_COMBINED_v201812': ['sm', 'sm_uncertainty'],
                                       'C3S_PASSIVE_v201812': ['sm', 'sm_uncertainty'],
                                       'MERRA2': ['SFMC'],
                                       'GLDAS2.1': ['SoilMoi0_10cm_inst'],
                                       'ERA5': ['swvl1'],
                                       'ERA_LAND_GBG4': ['39'],
                                       'ERA5-Land': ['swvl1']},
                         dataset_kwargs={'CCI_44_COMBINED': {'dropna': True, 'ioclass_kws': {'read_bulk': True}},
                                         'CCI_45_COMBINED': {'dropna': True, 'ioclass_kws': {'read_bulk': True}},
                                         'C3S_v201812_COMBINED': {'dropna': True,
                                                                  'ioclass_kws': {'read_bulk': True}},
                                         'C3S_v201812_PASSIVE': {'dropna': True,
                                                                 'ioclass_kws': {'read_bulk': True}},
                                         'MERRA2': {'ioclass_kws': {'read_bulk': True}},
                                         'GLDAS2.1': {'ioclass_kws': {'read_bulk': True}},
                                         'ERA5': {'ioclass_kws': {'read_bulk': True}},
                                         'ERA_LAND_GBG4': {'ioclass_kws': {'read_bulk': True}},
                                         'ERA5-Land': {'ioclass_kws': {'read_bulk': True}}})
    df = reader.read_ts(-91.625, 32.875)


if __name__ == '__main__':

    reader = load_ts_reader('C3S_COMBINED_v201812', force_r=True,
                            read_flags=[0], parameters=['sm'],
                            ioclass_kws={'read_bulk':True})

    ts=reader.read_ts(15,45)

    usecase_MultiReader()

    # #####CCI adjusted
    # reader = load_ts_reader('CCI_45_COMBINED_QCM_ADJUSTED', dropna=True, read_flags=[0],
    #                    ioclass_kws={'read_bulk':True},
    #                    cfg_file=r"D:\data-write\paper_results\iter3\hsp_model_frames\CCI_45_COMBINED\qcm_model_hsp\temp_config.cfg")
    # ts_cci = reader.read_ts(2, 47.422)['sm']
    #
    # reader = load_ts_reader('CCI_41_COMBINED_ADJUSTED_LMP_FULL_INIT_FREE', dropna=True)
    # ts = reader.read_ts(12, 45)['adjusted']
    #
    # ts.loc[ts == -999999.] = np.nan
    #
    # # ISMN
    # reader = load_ts_reader('ISMN_selection')
    # df, dist = reader.read_G_sm_nearest_station(-120.875, 38.375, 0, 999)
    # df, dist = reader.read_G_sm_nearest_station(-120.875, 38.375, 0, 0.05)
    # df, dist = reader.read_longest_G_sm_nearest_station(-120.875, 38.375)
    # df, dist = reader.read_longest_G_sm_nearest_station(-120.875, 38.375, 0, 0.05)
    #
    #
    # reader = load_ts_reader('ISMN')
    # station = reader.find_nearest_station(-110, 40)
    # idx = reader.get_dataset_ids('soil moisture')
    # ts = reader.read_ts(idx[100])
    # #####