# -*- coding: utf-8 -*-

"""
Time series reader for GLDAS v2.0 data
"""
# TODO:
#   (+)
#---------
# NOTES:
#   -

from io_utils.read.path_config import PathConfig
from io_utils.read.geo_ts_readers.gldas.base_reader import GLDASTs
from io_utils.path_configs.gldas.paths_gldas20 import path_settings


class GeoGLDAS20Ts(GLDASTs):
    # Reader implementation that uses the PATH configuration from above

    _ds_implemented = [('GLDAS20', 'core')]

    def __init__(self, dataset, force_path_group=None, **kwargs):

        if isinstance(dataset, list):
            dataset = tuple(dataset)

        self.dataset = dataset
        self.path_config = PathConfig(self.dataset, path_settings[self.dataset])
        ts_path = self.path_config.load_path(force_path_group=force_path_group)
        super(GeoGLDAS20Ts, self).__init__(ts_path, **kwargs)


# check if datasets in reader and in dict match
assert sorted(list(path_settings.keys())) == sorted(GeoGLDAS20Ts._ds_implemented)
