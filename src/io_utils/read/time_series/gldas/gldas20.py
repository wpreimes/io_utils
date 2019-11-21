# -*- coding: utf-8 -*-

"""
Time series reader for GLDAS v2.0 data
"""
# TODO:
#   (+)
#---------
# NOTES:
#   -

from src.io_utils.read.time_series.path_config import PathConfig
from src.io_utils.read.time_series.gldas.base_reader import GLDASTs
from src.io_utils.read.time_series.gldas.paths_gldas20 import path_settings


class GeoGLDAS20Ts(GLDASTs):
    # Reader implementation that uses the PATH configuration from above

    _ds_implemented = [('GLDAS20', 'core')]

    def __init__(self, dataset, **kwargs):

        self.dataset = dataset
        self.path_config = PathConfig(self.dataset, path_settings[self.dataset])
        ts_path = self.path_config.load_path()
        super(GeoGLDAS20Ts, self).__init__(ts_path, **kwargs)


# check if datasets in reader and in dict match
assert sorted(list(path_settings.keys())) == sorted(GeoGLDAS20Ts._ds_implemented)
