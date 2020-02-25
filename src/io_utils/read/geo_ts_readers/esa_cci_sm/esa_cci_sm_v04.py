# -*- coding: utf-8 -*-

"""
Time series reader for CCI SM v04 data
"""
# TODO:
#   (+)
#---------
# NOTES:
#   -

from io_utils.read.path_config import PathConfig
from datetime import datetime
from io_utils.path_configs.esa_cci_sm.paths_esa_cci_sm_v04 import path_settings
from io_utils.read.geo_ts_readers.esa_cci_sm.base_reader import GeoCCITs

class GeoCCISMv4Ts(GeoCCITs):
    # Reader implementation that uses the PATH configuration from above

    # exact time variable (days) from reference date
    _t0_ref = ('t0', datetime(1970,1,1,0,0,0))

    # fill values in the data columns
    _col_fillvalues = {'sm': [-9999.0],
                       'sm_uncertainty': [-9999.0],
                       _t0_ref[0]: [-3440586.5,
                                    -9999.0]} # TODO: why has v045 another fillvalue?

    # implememted subversion that have a set path configuration
    _ds_implemented = [('ESA_CCI_SM', 'v045', 'COMBINED'),
                       ('ESA_CCI_SM', 'v045', 'ACTIVE'),
                       ('ESA_CCI_SM', 'v045', 'PASSIVE'),
                       ('ESA_CCI_SM', 'v044', 'COMBINED'),
                       ('ESA_CCI_SM', 'v044', 'ACTIVE'),
                       ('ESA_CCI_SM', 'v044', 'PASSIVE'),
                       ('ESA_CCI_SM', 'v047', 'COMBINED'),
                       ('ESA_CCI_SM', 'v047', 'ACTIVE'),
                       ('ESA_CCI_SM', 'v047', 'PASSIVE')]


    def __init__(self, dataset, exact_index=False, force_path_group=None, **kwargs):

        if isinstance(dataset, list):
            dataset = tuple(dataset)

        self.dataset = dataset

        self.path_config = PathConfig(self.dataset, path_settings[self.dataset])
        ts_path = self.path_config.load_path(force_path_group=force_path_group)

        super(GeoCCISMv4Ts, self).__init__(ts_path, **kwargs)

        self.exact_index = exact_index
        if exact_index and (self.parameters is not None):
            self.parameters.append(self._t0_ref[0])

# check if datasets in reader and in dict match
assert sorted(list(path_settings.keys())) == sorted(GeoCCISMv4Ts._ds_implemented)
