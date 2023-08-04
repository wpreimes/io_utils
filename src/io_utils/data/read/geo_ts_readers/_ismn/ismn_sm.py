# -*- coding: utf-8 -*-

"""
Module description
"""

from ismn.interface import ISMN_Interface
from io_utils.data.read.path_config import PathConfig
import pandas as pd
from numpy import nan
import os
import shutil
import warnings


try:
    from io_utils.data.path_configs.ismn.paths_ismn import path_settings
except ImportError:
    path_settings = {}


class GeoISMNTs(ISMN_Interface):
    """
    Modified ISMN Reader class, that reads good (G Flag) ISMN values and provides
    functions for reading the station closest to a passed lonlat tuple.
    """
    _ds_implemented = [('ISMN', 'v20191211'),
                       ('ISMN', 'v20210131')]

    def __init__(self, dataset_or_path, network=None,
                 force_path_group=None, scale_factors=None):
        """
        Initialize the reader for ISMN data

        Parameters
        ----------
        dataset_or_path : tuple or str
            Dataset that is implemented in a path config. Or a path directly,
            where the data is stored.
        network : string or list, optional
            Provide name of network to only load the given network
        force_path_group : str, optional (default: None)
            For a certain path group to load the data from.
        scale_factors : dict, optional (default:None)
            Apply the passed multiplicative scales to the selected columns
        """
        if isinstance(dataset_or_path, list):
            dataset_or_path = tuple(dataset_or_path)

        self.dataset = dataset_or_path
        self.network = network
        path_config = path_settings[self.dataset] if self.dataset in path_settings.keys() else None
        self.path_config = PathConfig(self.dataset, path_config)
        ts_path = self.path_config.load_path(force_path_group=force_path_group)

        self.scale_factors = scale_factors
        super(GeoISMNTs, self).__init__(ts_path, network=self.network)

        self.metapath = os.path.join(self.root.root_dir, 'python_metadata')

    def rebuild_metadata(self):
        """
        Remove and rebuild python metadata.
        """
        shutil.rmtree(self.metapath, ignore_errors=True)
        super(GeoISMNTs, self).activate_network(self.network)

    def read(self, *args, **kwargs):
        # read by index and scale
        ret = super(GeoISMNTs, self).read(*args, **kwargs)
        if isinstance(ret, tuple):
            df = ret[0]
            meta = ret[1]
        else:
            df = ret
            meta = None

        if self.scale_factors is not None:
            for n, s in self.scale_factors.items():
                if n in df.columns: df[n] *= s

        df.index = df.index.tz_localize(None)

        if meta is None:
            return df
        else:
            return df, meta

    def read_nearest_station(self, lon, lat, variable='soil_moisture',
                             max_dist=30000, only_good=True, return_flags=False,
                             return_distance=True, **filter_kwargs):
        """
        Read good (G-flagged) time series values for the station closest to the
        passed lon, lat in the passed depths. To mask the time series from this
        function, use a masking adapter. Only stations that measure the passed
        variable will be considered.

        Parameters
        ----------
        lon : float
            Longitude of the point to find the nearest station for
        lat : float
            Latitude of the point to find the nearest station for
        variable : str, optional (default: soil_moisture)
            Variable to read, the according flag will be used if only_good=True.
        max_dist : int
            Maximum allowed distance between the passed lon/lat position and the
            actually found nearest station. If the distance is large, no data is read.
        only_good : bool, optional (default: True)
            If True, drops all lines where soil_moisture_flag is not G.
            If False, returns also the flag column
        return_flags : bool, optional (default: False)
            Returns
        return_distance : bool
            Also return the distance (2 return values), else 1 return value
        filter_kwargs: See ismn.components Sensor.eval() function
                depth : Depth or list or tuple, optional (default: None)
                filter_meta_dict : dict, optional (default: None)
                check_only_sensor_depth_from : bool, optional (default: False)

        Returns
        -------
        data : pd.DataFrame
            Data measured at the station
        nearest_station : ISMN_station
            Station object from which the data was read.
        distance : float
            Distance between the passed coordinates and the read station.
        """
        nearest_station, distance = self.find_nearest_station(lon, lat, True)

        if distance > max_dist:
            warnings.warn('fNo station within the selected distance found: {max_dist}')
            data = None
        else:
            data = []
            metadata = {}
            for sensor in nearest_station.iter_sensors(variable=variable,
                                                       **filter_kwargs):
                ts = sensor.read_data()[[variable, f'{variable}_flag']]
                if only_good:
                    ts.loc[ts[f'{variable}_flag'] != 'G', variable] = nan
                    ts.loc[ts[f'{variable}_flag'] != 'G', f'{variable}_flag'] = nan
                    ts = ts.dropna(how='all')
                if not return_flags:
                    ts = ts[[variable]]
                if self.scale_factors and variable in self.scale_factors.keys():
                    ts[variable] *= self.scale_factors[variable]
                meta = sensor.metadata
                ts.rename(columns={c : f"{c} {str(meta['variable'].depth)}" for c in ts.columns}, inplace=True)
                new_name = f"{meta['variable'].val} {str(meta['variable'].depth)}"
                metadata[new_name] = meta
                data.append(ts)

            data = pd.concat(data, axis=1)
            data.index = data.index.tz_localize(None)

        if return_distance:
            return data, nearest_station, distance
        else:
            return data, nearest_station


# check if datasets in reader and in dict match
assert sorted(list(path_settings.keys())) == sorted(GeoISMNTs._ds_implemented)


