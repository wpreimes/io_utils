# -*- coding: utf-8 -*-

"""
Time series reader for GLDAS v2.1 data
"""

from io_utils.read.path_config import PathConfig
from io_utils.read.geo_ts_readers.gldas.base_reader import GLDASTs
try:
    from io_utils.path_configs.gldas.paths_gldas21 import path_settings
except ImportError:
    path_settings = {}

class GeoGLDAS21Ts(GLDASTs):
    # Reader implementation that uses the PATH configuration from above

    _ds_implemented = [('GLDAS21', 'core')]

    def __init__(self, dataset_or_path, force_path_group=None, **kwargs):

        if isinstance(dataset_or_path, list):
            dataset_or_path = tuple(dataset_or_path)

        self.dataset = dataset_or_path

        path_config = path_settings[self.dataset] if self.dataset in path_settings.keys() else None
        self.path_config = PathConfig(self.dataset, path_config)
        ts_path = self.path_config.load_path(force_path_group=force_path_group)

        super(GeoGLDAS21Ts, self).__init__(ts_path, **kwargs)

# check if datasets in reader and in dict match
assert sorted(list(path_settings.keys())) == sorted(GeoGLDAS21Ts._ds_implemented)