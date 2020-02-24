# -*- coding: utf-8 -*-

"""
Time series reader for SMAP SM data
"""

from io_utils.read.path_config import PathConfig
from io_utils.read.geo_ts_readers.smap.base_reader import SMAPTs
from path_configs.smap.paths_smap import path_settings
from collections import OrderedDict

class GeoSMAPTs(SMAPTs):
    # Reader implementation that uses the PATH configuration from above

    _ds_implemented = [('SMAP', 'SP3SMPv5', 'ASC'),
                       ('SMAP', 'SP3SMPv5', 'DES'),
                       ('SMAP', 'SP3SMPv6', 'ASC'),
                       ('SMAP', 'SP3SMPv6', 'DES')]

    def __init__(self, dataset, force_path_group=None, **kwargs):

        if isinstance(dataset, list):
            dataset = tuple(dataset)

        self.dataset = dataset
        self.path_config = PathConfig(self.dataset, path_settings[self.dataset])
        ts_path = self.path_config.load_path(force_path_group=force_path_group)
        super(GeoSMAPTs, self).__init__(ts_path, **kwargs)

    def read_cells(self, cells):
        cell_data = OrderedDict()
        gpis, lons, lats = self.grid.grid_points_for_cell(list(cells))
        for gpi, lon, lat in zip(gpis, lons, lats):
            df = self.read(lon, lat)
            cell_data[gpi] = df
        return cell_data

# check if datasets in reader and in dict match
assert sorted(list(path_settings.keys())) == sorted(GeoSMAPTs._ds_implemented)