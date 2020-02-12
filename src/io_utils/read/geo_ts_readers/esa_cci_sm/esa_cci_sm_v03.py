# -*- coding: utf-8 -*-

"""
Time series reader for CCI SM v03 data
"""
# TODO:
#   (+)
#---------
# NOTES:
#   -

from io_utils.read.geo_ts_readers.path_config import PathConfig
from io_utils.read.geo_ts_readers.esa_cci_sm.base_reader import GeoCCITs
from datetime import datetime
from path_configs.esa_cci_sm.paths_esa_cci_sm_v03 import path_settings

class GeoCCISMv3Ts(GeoCCITs):
    # Reader implementation that uses the PATH configuration from above

    # exact time variable (days) from reference date
    _t0_ref = ('t0', datetime(1970,1,1,0,0,0))

    # fill values in the data columns
    _col_fillvalues = {'sm': [-9999.0],
                       'sm_uncertainty': [-9999.0],
                       _t0_ref[0]: [-3440586.5]} # TODO: why this fill value for t0?

    # implememted subversion that have a set path configuration
    _ds_implemented = [('ESA_CCI_SM', 'v033', 'COMBINED'),
                       ('ESA_CCI_SM', 'v033', 'ACTIVE'),
                       ('ESA_CCI_SM', 'v033', 'PASSIVE')]

    def __init__(self, dataset, exact_index=False, force_path_group=None, **kwargs):
        self.dataset = dataset

        self.path_config = PathConfig(self.dataset, path_settings[self.dataset])
        ts_path = self.path_config.load_path(force_path_group=force_path_group)

        super(GeoCCISMv3Ts, self).__init__(ts_path, **kwargs)

        self.exact_index = exact_index
        if exact_index and (self.parameters is not None):
            self.parameters.append(self._t0_ref[0])


# check if datasets in reader and in dict match
assert sorted(list(path_settings.keys())) == sorted(GeoCCISMv3Ts._ds_implemented)
