# -*- coding: utf-8 -*-

"""
Time series reader for ERA5 and ERA5 Land data
"""
# TODO:
#   (+)
#---------
# NOTES:
#   -

from io_utils.read.path_config import PathConfig
from io_utils.read.geo_ts_readers.merra.base_reader import MERRATs
try:
    from io_utils.path_configs.merra.paths_merra2 import path_settings
except ImportError:
    path_settings = {}

class GeoMerra2Ts(MERRATs):
    # Reader implementation that uses the PATH configuration from above

    _ds_implemented = [('MERRA2', 'core')]

    def __init__(self, dataset_or_path, force_path_group=None, **kwargs):

        if isinstance(dataset_or_path, list):
            dataset_or_path = tuple(dataset_or_path)

        self.dataset = dataset_or_path
        path_config = path_settings[self.dataset] if self.dataset in path_settings.keys() else None
        self.path_config = PathConfig(self.dataset, path_config)
        ts_path = self.path_config.load_path(force_path_group=force_path_group)
        
        super(GeoMerra2Ts, self).__init__(ts_path, **kwargs)


# check if datasets in reader and in dict match
assert sorted(list(path_settings.keys())) == sorted(GeoMerra2Ts._ds_implemented)