# -*- coding: utf-8 -*-

"""
Time series reader for ERA5 and ERA5 Land data
"""
# TODO:
#   (+)
#---------
# NOTES:
#   -

from io_utils.read.geo_ts_readers.path_config import PathConfig
from io_utils.read.geo_ts_readers.merra.base_reader import MERRATs
from path_configs.merra.paths_merra2 import path_settings


class GeoMerra2Ts(MERRATs):
    # Reader implementation that uses the PATH configuration from above

    _ds_implemented = [('MERRA2', 'core')]

    def __init__(self, dataset, force_path_group=None, **kwargs):
        self.dataset = dataset
        self.path_config = PathConfig(self.dataset, path_settings[self.dataset])
        ts_path = self.path_config.load_path(force_path_group=force_path_group)
        super(GeoMerra2Ts, self).__init__(ts_path, **kwargs)


# check if datasets in reader and in dict match
assert sorted(list(path_settings.keys())) == sorted(GeoMerra2Ts._ds_implemented)