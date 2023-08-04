# -*- coding: utf-8 -*-

"""
Time series reader for CCI SM v05 data
"""

from io_utils.data.read.path_config import PathConfig
from io_utils.data.read.geo_ts_readers.esa_cci_sm.base_reader import SmecvTs
try:
    from io_utils.data.path_configs.esa_cci_sm.paths_esa_cci_sm_v06 import path_settings
except ImportError:
    path_settings = {}

class GeoCCISMv6Ts(SmecvTs):
    # Reader implementation that uses the PATH configuration from above

    # implememted subversion that have a set path configuration
    _ds_implemented = [
                       ('ESA_CCI_SM', 'v061', 'COMBINED'),
                       ('ESA_CCI_SM', 'v061', 'ACTIVE'),
                       ('ESA_CCI_SM', 'v061', 'PASSIVE'),
                       ]

    _t0 = 't0'

    def __init__(self, dataset_or_path, exact_index=False, force_path_group=None,
                 **kwargs):

        if isinstance(dataset_or_path, list):
            dataset_or_path = tuple(dataset_or_path)

        self.dataset = dataset_or_path

        path_config = path_settings[self.dataset] if self.dataset in path_settings.keys() else None
        self.path_config = PathConfig(self.dataset, path_config)
        ts_path = self.path_config.load_path(force_path_group=force_path_group)

        super(GeoCCISMv6Ts, self).__init__(ts_path, **kwargs)

        self.exact_index = exact_index
        if exact_index and (self.parameters is not None):
            self.parameters.append(self._t0)


# check if datasets in reader and in dict match
assert sorted(list(path_settings.keys())) == sorted(GeoCCISMv6Ts._ds_implemented)



