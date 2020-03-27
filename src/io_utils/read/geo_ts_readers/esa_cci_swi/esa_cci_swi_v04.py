# -*- coding: utf-8 -*-

"""
Reader for SWI data from esa cci sm v4 sm data.
"""
from io_utils.read.path_config import PathConfig
from io_utils.path_configs.esa_cci_swi.paths_esa_cci_swi_v04 import path_settings
from io_utils.read.geo_ts_readers.esa_cci_swi.base_reader import GeoCCISWITs

class GeoCCISWIv4Ts(GeoCCISWITs):
    # Reader implementation that uses the PATH configuration from above

    # fill values in the data columns
    _col_fillvalues = {}

    # implememted subversion that have a set path configuration
    _ds_implemented = [('ESA_CCI_SWI', 'v047')]

    def __init__(self, dataset, force_path_group=None, **kwargs):

        if isinstance(dataset, list):
            dataset = tuple(dataset)

        self.dataset = dataset

        self.path_config = PathConfig(self.dataset, path_settings[self.dataset])
        ts_path = self.path_config.load_path(force_path_group=force_path_group)

        super(GeoCCISWIv4Ts, self).__init__(ts_path, **kwargs)

# check if datasets in reader and in dict match
assert sorted(list(path_settings.keys())) == sorted(GeoCCISWIv4Ts._ds_implemented)