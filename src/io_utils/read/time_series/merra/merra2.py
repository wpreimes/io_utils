# -*- coding: utf-8 -*-

"""
Time series reader for ERA5 and ERA5 Land data
"""
# TODO:
#   (+)
#---------
# NOTES:
#   -

from src.io_utils.read.time_series.path_config import PathConfig
from src.io_utils.read.time_series.merra.base_reader import MERRATs

from src.io_utils.read.time_series.merra.paths_merra2 import path_settings


class GeoMerra2Ts(MERRATs):
    # Reader implementation that uses the PATH configuration from above

    _ds_implemented = [('MERRA2', 'core')]

    def __init__(self, dataset, **kwargs):
        self.dataset = dataset
        self.path_config = PathConfig(self.dataset, path_settings[self.dataset])
        ts_path = self.path_config.load_path()
        super(GeoMerra2Ts, self).__init__(ts_path, **kwargs)


# check if datasets in reader and in dict match
assert sorted(list(path_settings.keys())) == sorted(GeoMerra2Ts._ds_implemented)