# -*- coding: utf-8 -*-

"""
Time series reader for C3S v201812 active, combined and passive data
"""
from io_utils.read.geo_ts_readers.path_config import PathConfig
from io_utils.read.geo_ts_readers.c3s_sm import base_reader
from path_configs.c3s_sm.paths_c3s_sm_v201912 import path_settings
from datetime import datetime

class GeoC3Sv201912Ts(base_reader.GeoC3STs):
    # Reader implementation that uses the PATH configuration from above
    # Flagging should be done with the masking adapter from pytesmo
    _t0_ref = ('t0', datetime(1970,1,1,0,0,0))

    _col_fillvalues = {'sm': [-9999.0],
                       'sm_uncertainty': [-9999.0],
                       _t0_ref[0]: [-3440586.5]}

    _ds_implemented = [('C3S', 'v201912', 'COMBINED', 'TCDR'),
                       ('C3S', 'v201912', 'ACTIVE', 'TCDR'),
                       ('C3S', 'v201912', 'PASSIVE', 'TCDR')]

    def __init__(self, dataset, force_path_group=None, **kwargs):
        """
        Parameters
        ----------
        dataset : tuple
            e.g. ('C3S', 'v201812', 'COMBINED', 'TCDR')
        force_path_group : str, optional (default: None)
            Select a specific path group from the path config to read.
        kwargs :
            kwargs that are passed to load_path and to initialise the reader.
        """
        self.dataset = tuple(dataset)
        self.path_config = PathConfig(self.dataset, path_settings[self.dataset])
        ts_path = self.path_config.load_path(force_path_group=force_path_group)

        super(GeoC3Sv201912Ts, self).__init__(ts_path, **kwargs)

# check if datasets in reader and in dict match
assert sorted(list(path_settings.keys())) == sorted(GeoC3Sv201912Ts._ds_implemented)

