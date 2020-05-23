# -*- coding: utf-8 -*-
from io_utils.read.geo_ts_readers.lprm.base_reader import LPRMTs
from io_utils.read.path_config import PathConfig
from datetime import datetime
from io_utils.path_configs.amsr2.paths_amsr2_lprm_v6 import path_settings

class GeoAmsr2LPRMv6Ts(LPRMTs):
    # Reader implementation that uses the PATH configuration from above

    # exact time variable (days) from reference date
    _t0_ref = ('t0', datetime(1970,1,1,0,0,0))

    # fill values in the data columns
    _col_fillvalues = {}

    # implememted subversion that have a set path configuration
    _ds_implemented = [('AMSR2', 'LPRM', 'v6', 'ASC'),
                       ('AMSR2', 'LPRM', 'v6', 'DESC')]

    def __init__(self, dataset, exact_index=False, force_path_group=None, **kwargs):

        if isinstance(dataset, list):
            dataset = tuple(dataset)

        self.dataset = dataset

        self.path_config = PathConfig(self.dataset, path_settings[self.dataset])
        ts_path = self.path_config.load_path(force_path_group=force_path_group)

        super(GeoAmsr2LPRMv6Ts, self).__init__(ts_path, **kwargs)

        self.exact_index = exact_index
        if exact_index and (self.parameters is not None):
            self.parameters.append(self._t0_ref[0])

# check if datasets in reader and in dict match
assert sorted(list(path_settings.keys())) == sorted(GeoAmsr2LPRMv6Ts._ds_implemented)