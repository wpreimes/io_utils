# -*- coding: utf-8 -*-

"""
Time series reader for SMAP SM data
"""

from io_utils.read.path_config import PathConfig

from io_utils.read.geo_ts_readers.smap.base_reader import SMAPTs
from collections import OrderedDict
try:
    from io_utils.path_configs.smap.paths_smap import path_settings
except ImportError:
    path_settings = {}

class GeoSpl3smpTs(SMAPTs):
    # Reader implementation that uses the PATH configuration from above

    _ds_implemented = [('SMAP', 'SP3SMPv5', 'ASC'),
                       ('SMAP', 'SP3SMPv5', 'DES'),
                       ('SMAP', 'SP3SMPv6', 'ASC'),
                       ('SMAP', 'SP3SMPv6', 'DES')]

    def __init__(self, dataset_or_path, force_path_group=None, **kwargs):

        if isinstance(dataset_or_path, list):
            dataset_or_path = tuple(dataset_or_path)

        self.dataset = dataset_or_path

        path_config = path_settings[self.dataset] if self.dataset in path_settings.keys() else None
        self.path_config = PathConfig(self.dataset, path_config)
        ts_path = self.path_config.load_path(force_path_group=force_path_group)
        super(GeoSpl3smpTs, self).__init__(ts_path, **kwargs)

    # def read_cells(self, cells):
    #     cell_data = OrderedDict()
    #     gpis, lons, lats = self.grid.grid_points_for_cell(list(cells))
    #     for gpi, lon, lat in zip(gpis, lons, lats):
    #         df = self.read(lon, lat)
    #         cell_data[gpi] = df
    #     return cell_data

# check if datasets in reader and in dict match
assert sorted(list(path_settings.keys())) == sorted(GeoSpl3smpTs._ds_implemented)
