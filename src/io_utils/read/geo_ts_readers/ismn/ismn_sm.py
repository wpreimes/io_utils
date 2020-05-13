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

from ismn.interface import ISMN_Interface
import os
import shutil
import numpy as np
from matplotlib.patches import Rectangle
import sys
import matplotlib.pyplot as plt
from io_utils.plot.plot_maps import cp_scatter_map

try:
    from io_utils.path_configs.ismn.paths_ismn import path_settings
except ImportError:
    path_settings = {}


class GeoISMNTs(ISMN_Interface):
    """
    Modified ISMN Reader class, that reads good (G Flag) ISMN values and provides
    functions for reading the station closest to a passed lonlat tuple.
    """
    _ds_implemented = [('ISMN', 'v20191211')]

    def __init__(self, dataset_or_path, network=None, parameters=('soil moisture'),
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
        self.parameters = parameters
        self.network = network
        path_config = path_settings[self.dataset] if self.dataset in path_settings.keys() else None
        self.path_config = PathConfig(self.dataset, path_config)
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

    def plot_station_locations(self, variable='soil moisture',
                               min_depth=0, max_depth=999., filename=None):
        """
        plots available stations on a world map in robinson projection

        Parameters
        ----------
        variable : str, optional (default: 'soil moisture')
            Variable that is use to find stations that measure it
        min_depth : float, optional (default: 0.)
            Only stations that measure variable below this depth are considered.
        max_depth : float, optional (default: 999.)
            Only stations that measure variable above this depth are considered.

        Returns
        -------
        fig: matplotlib.Figure
            created figure instance. If axes was given this will be None.
        ax: matplitlib.Axes
            used axes instance.
        """
        if not (sys.version_info[0] == 3 and sys.version_info[1] == 4):
            colormap = plt.get_cmap('tab20')
        else:
            colormap = plt.get_cmap('Set1')
            
        uniq_networks = self.list_networks()
        colorsteps = np.arange(0, 1, 1 / float(uniq_networks.size))
        rect = []

        lons, lats, values = [], [], []

        network_count = 0
        station_count = 0
        sensors_count = 0

        for j, network in enumerate(uniq_networks):
            network_counted = False
            netcolor = colormap(colorsteps[j])
            rect.append(Rectangle((0, 0), 1, 1, fc=netcolor))
            
            stationnames = self.list_stations(network)
            
            for stationname in stationnames:
                station_counted = False
                station = self.get_station(stationname, network)
                station_vars = station.get_variables()

                if variable not in station_vars:
                    continue

                station_depths_from, station_depths_to = station.get_depths(variable)

                for depth_from, depth_to in zip(station_depths_from, station_depths_to):
                    if (depth_from < min_depth) or (depth_to > max_depth):
                        # skip depths outside of the passed range
                        continue

                    # from here we actually have valid data
                    if not station_counted:
                        station_count += 1
                        station_counted = True

                    if not network_counted:
                        network_count += 1
                        network_counted = True

                    sensors = station.get_sensors(variable, depth_from, depth_to)

                    for sensor in sensors:
                        lons.append(station.longitude)
                        lats.append(station.latitude)
                        values.append(colorsteps[j])
                        sensors_count += 1

        feedback = "{} valid sensors in {} stations in {} networks (of {} potential networks) \n" \
                   "for variable '{}' between {} and {} m depth".format(
            sensors_count, station_count, network_count, len(uniq_networks), variable, min_depth, max_depth)

        print(feedback)

        fig, ax, im = cp_scatter_map(np.array(lons), np.array(lats), np.array(values),
                                     borders=True, states=True, cmap=colormap, show_cbar=False)

        nrows = 8. if len(uniq_networks) > 8 else len(uniq_networks)
        ncols = int(uniq_networks.size / nrows)
        if ncols == 0:
            ncols = 1

        handles, labels = ax.get_legend_handles_labels()
        lgd = ax.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.5, -0.1))

        plt.legend(rect, uniq_networks.tolist(), loc='upper center', ncol=ncols,
                   bbox_to_anchor=(0.5, -0.05), fontsize=4)
        text = ax.text(0.5, 1.2, feedback, transform=ax.transAxes, fontsize='xx-small',
                       horizontalalignment='center')

        fig.set_size_inches([6, 3.5 + 0.25 * nrows])
        if filename is not None:
            fig.savefig(filename, bbox_extra_artists=(lgd, text), dpi=300)
            plt.close(fig)
        else:
            return fig, ax

# check if datasets in reader and in dict match
assert sorted(list(path_settings.keys())) == sorted(GeoISMNTs._ds_implemented)

if __name__ == '__main__':
    networks = ['AMMA-CATCH', 'CARBOAFRICA', 'DAHRA', 'CTP-SMTMN',
              'MySMNet', 'OZNET', 'BIEBRZA-S-1', 'FMI', 'FR-Aqui',
              'HOBE', 'REMEDHUS', 'RSMN', 'SMOSMANIA', 'TERENO',
              'WEGENERNET', 'WSMN', 'BNZ-LTER', 'COSMOS',
              'FLUXNET-AMERIFLUX', 'iRON', 'PBO-H2O', 'RISMA',
              'SCAN', 'USCRN', 'LAB-net']

    reader = GeoISMNTs(('ISMN', 'v20191211'), network=networks, scale_factors=None)
    s = reader.read(0)

    #reader.plot_station_locations(min_depth=0, max_depth=.05, filename='C:\Temp\stations_cci_0.0_to_0.05.png')
    reader.plot_station_locations(min_depth=0.0, max_depth=.1, filename='C:\Temp\stations_cci_0.0_to_0.1.png')
    # reader.plot_station_locations(min_depth=0, max_depth=.051, filename='C:\Temp\stations_0.0_to_0.051.png')
    # reader.plot_station_locations(min_depth=.05, max_depth=.1, filename='C:\Temp\stations_0.05_to_0.1.png')
    # reader.plot_station_locations(min_depth=.051, max_depth=.1, filename='C:\Temp\stations_0.051_to_0.1.png')
    # reader.plot_station_locations(min_depth=.1, max_depth=.2, filename='C:\Temp\stations_0.1_to_0.2.png')
    # reader.plot_station_locations(min_depth=.2, max_depth=.3, filename='C:\Temp\stations_0.2_to_0.3.png')
    # reader.plot_station_locations(min_depth=.3, max_depth=.4, filename='C:\Temp\stations_0.3_to_0.4.png')
    # reader.plot_station_locations(min_depth=.4, max_depth=.5, filename='C:\Temp\stations_0.4_to_0.5.png')
    # reader.plot_station_locations(min_depth=.5, max_depth=.6, filename='C:\Temp\stations_0.5_to_0.6.png')
    # reader.plot_station_locations(min_depth=.6, max_depth=.7, filename='C:\Temp\stations_0.6_to_0.7.png')
    # reader.plot_station_locations(min_depth=.7, max_depth=.8, filename='C:\Temp\stations_0.7_to_0.8.png')
    # reader.plot_station_locations(min_depth=.8, max_depth=.9, filename='C:\Temp\stations_0.8_to_0.9.png')
    # reader.plot_station_locations(min_depth=.9, max_depth=1.0, filename='C:\Temp\stations_0.9_to_1.0.png')




    # reader = GeoISMNTs(('ISMN', 'v20191211'), network=['COSMOS'],
    #                    force_path_group='__test', scale_factors=None)
    # onestat = reader.find_nearest_station(-155.5, 19.9)
    # assert onestat.station == 'SilverSword'
    # ids = reader.get_dataset_ids('soil moisture', min_depth=0, max_depth=0.17)
    # ts = reader.read_ts(ids[0])
    #
    # dat, station, dist = reader.read_sm_nearest_station(lon=onestat.longitude,
    #                                            lat=onestat.latitude)
    # assert dist == 0.
    # assert np.all(
    #     dat[dat.columns[0]].values ==
    #     onestat.read_variable('soil moisture').data['soil moisture'].values)

