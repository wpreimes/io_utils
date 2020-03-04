# -*- coding: utf-8 -*-

"""
Module description
"""
# TODO:
#   (+) 
#---------
# NOTES:
#   -

from io_utils.read.path_config import PathConfig
import pandas as pd
from io_utils.path_configs.ismn.paths_ismn import path_settings
from ismn.interface import ISMN_Interface
import os
import shutil
import numpy as np

class GeoISMNTs(ISMN_Interface):
    """
    Modified ISMN Reader class, that reads good (G Flag) ISMN values and provides
    functions for reading the station closest to a passed lonlat tuple.
    """
    _ds_implemented = [('ISMN', 'v20191211')]

    def __init__(self, dataset, network=None, parameters=('soil moisture'),
                 force_path_group=None, scale_factors=None):
        """
        Initialize the reader for ISMN data
        Parameters
        ----------
        dataset : tuple
            Dataset that is implemented in a path config.
        network : string or list, optional
            Provide name of network to only load the given network
        force_path_group : str, optional (default: None)
            For a certain path group to load the data from.
        scale_factors : dict, optional (default:None)
            Apply the passed multiplicative scales to the selected columns
        """
        if isinstance(dataset, list):
            dataset = tuple(dataset)

        self.dataset = dataset
        self.parameters = parameters
        self.network = network
        self.path_config = PathConfig(self.dataset, path_settings[self.dataset])
        ts_path = self.path_config.load_path(force_path_group=force_path_group)

        self.scale_factors = scale_factors
        self.metapath = os.path.join(ts_path, 'python_metadata')
        super(GeoISMNTs, self).__init__(ts_path, self.network)

    def reset_python_metadata(self):
        """
        Remove and rebuild python metadata.
        """
        shutil.rmtree(self.metapath)
        super(GeoISMNTs, self).activate_network(self.network)

    def read(self, idx):
        df = super(GeoISMNTs, self).read_ts(idx)
        if self.scale_factors is not None:
            for n, s in self.scale_factors.items():
                if n in df.columns: df[n] *= s

        df.index = df.index.tz_localize(None)

        return df

    def read_sm_nearest_station(self, lon, lat, min_depth=0, max_depth=999,
                                  max_dist=30000, return_distance=True):
        """
        Read good (G-flagged) time series values for the station closest to the
        passed lon, lat in the passed depths. To mask the time series from this
        function, use a masking adapter.

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
        nearest_station : ISMN_station
            Station object from which the data was read.
        distance : float
            Distance between the passed coordinates and the read station.
        """
        if not isinstance(self.parameters, str) and len(self.parameters) > 1:
            raise NotImplementedError # todo: implement so that multiple var work
        else:
            variable = self.parameters if isinstance(self.parameters, str) else self.parameters[0]

        ts_for_station = []
        nearest_station, distance = self.find_nearest_station(lon, lat, True)

        if distance > max_dist:
            print('No station within the selected distance: {}'.format(max_dist))
            df_for_station = None
            distance = None
        else:
            depths_from, depths_to = nearest_station.get_depths(variable)
            for depth_from, depth_to in zip(depths_from, depths_to):
                if (depth_from < min_depth) or (depth_to > max_depth):
                    # skip depths outside of the passed range
                    continue

                sensors = nearest_station.get_sensors(variable, depth_from, depth_to)
                for sensor in sensors:
                    dat = nearest_station.read_variable(variable,
                                                        depth_from=depth_from,
                                                        depth_to=depth_to,
                                                        sensor=sensor)

                    if self.scale_factors is not None and variable in list(self.scale_factors.keys()):
                        dat.data[variable] *= self.scale_factors[variable]
                    for var in dat.data.columns:
                        name = (var, dat.network, dat.station, depth_from,
                                depth_to, sensor)

                        data = dat.data[var]
                        data.name = name
                        ts_for_station.append(data)
            df_for_station = pd.concat(ts_for_station, axis=1)

            df_for_station.index = df_for_station.index.tz_localize(None)

        if return_distance:
            return df_for_station, nearest_station, distance
        else:
            return df_for_station, nearest_station

    def read_longest_sm_nearest_station(self, lon, lat, min_depth=0, max_depth=999,
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
        df, station, dist = self.read_sm_nearest_station(
            lon, lat, min_depth, max_depth, max_dist=max_dist)
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

# check if datasets in reader and in dict match
assert sorted(list(path_settings.keys())) == sorted(GeoISMNTs._ds_implemented)

if __name__ == '__main__':
    networks =  ['AMMA-CATCH', 'CARBOAFRICA', 'DAHRA', 'CTP-SMTMN',
                                      'MySMNet', 'OZNET', 'BIEBRZA-S-1', 'FMI', 'FR-Aqui',
                                      'HOBE', 'REMEDHUS', 'RSMN', 'SMOSMANIA', 'TERENO',
                                      'WEGENERNET', 'WSMN', 'BNZ-LTER', 'COSMOS',
                                      'FLUXNET-AMERIFLUX', 'iRON', 'PBO-H2O', 'RISMA',
                                      'SCAN', 'USCRN', 'LAB-net']

    reader = GeoISMNTs(('ISMN', 'v20191211'), network=networks, scale_factors=None)

    reader.plot_station_locations()




    reader = GeoISMNTs(('ISMN', 'v20191211'), network=['COSMOS'],
                       force_path_group='__test', scale_factors=None)
    onestat = reader.find_nearest_station(-155.5, 19.9)
    assert onestat.station == 'SilverSword'
    ids = reader.get_dataset_ids('soil moisture', min_depth=0, max_depth=0.17)
    ts = reader.read_ts(ids[0])

    dat, station, dist = reader.read_sm_nearest_station(lon=onestat.longitude,
                                               lat=onestat.latitude)
    assert dist == 0.
    assert np.all(
        dat[dat.columns[0]].values ==
        onestat.read_variable('soil moisture').data['soil moisture'].values)

