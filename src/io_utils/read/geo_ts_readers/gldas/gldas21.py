# -*- coding: utf-8 -*-

"""
Time series reader for GLDAS v2.1 data
"""
# TODO:
#   (+)
#---------
# NOTES:
#   -

from io_utils.read.geo_ts_readers.path_config import PathConfig
from io_utils.read.geo_ts_readers.gldas.base_reader import GLDASTs
from path_configs.gldas.paths_gldas21 import path_settings


class GeoGLDAS21Ts(GLDASTs):
    # Reader implementation that uses the PATH configuration from above

    _ds_implemented = [('GLDAS21', 'core'),
                       ('GLDAS21', 'testdata')]

    def __init__(self, dataset, force_path_group=None, **kwargs):
        self.dataset = dataset
        self.path_config = PathConfig(self.dataset, path_settings[self.dataset])
        ts_path = self.path_config.load_path(force_path_group=force_path_group)
        super(GeoGLDAS21Ts, self).__init__(ts_path, **kwargs)

# check if datasets in reader and in dict match
assert sorted(list(path_settings.keys())) == sorted(GeoGLDAS21Ts._ds_implemented)