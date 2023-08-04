# -*- coding: utf-8 -*-

"""
Time series reader for ERA Interim Land data
"""
# TODO:
#   (+)
#---------
# NOTES:
#   -

from io_utils.data.read.geo_ts_readers.era.base_reader import ERATs
from io_utils.data.read.path_config import PathConfig
try:
    from io_utils.data.path_configs.era.paths_eraint_land import path_settings
except ImportError:
    path_settings = {}

class GeoEraIntGBG4Ts(ERATs):
    # Reader implementation that uses the PATH configuration from above
    _ds_implemented = [('ERAINT-Land', 'GBG4', 'core')]

    def __init__(self, dataset_or_path, force_path_group=None, **kwargs):

        if isinstance(dataset_or_path, list):
            dataset_or_path = tuple(dataset_or_path)

        self.dataset = dataset_or_path

        path_config = path_settings[self.dataset] if self.dataset in path_settings.keys() else None
        self.path_config = PathConfig(self.dataset, path_config)
        ts_path = self.path_config.load_path(force_path_group=force_path_group)

        super(GeoEraIntGBG4Ts, self).__init__(ts_path, **kwargs)

# check if datasets in reader and in dict match
assert sorted(list(path_settings.keys())) == sorted(GeoEraIntGBG4Ts._ds_implemented)
