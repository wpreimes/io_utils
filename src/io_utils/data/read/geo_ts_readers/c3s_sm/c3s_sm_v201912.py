# -*- coding: utf-8 -*-

"""
Time series reader for C3S v201812 active, combined and passive data
"""
from io_utils.data.read.path_config import PathConfig
from io_utils.data.read.geo_ts_readers.c3s_sm import base_reader
try:
    from io_utils.data.path_configs.c3s_sm.paths_c3s_sm_v201912 import path_settings
except ImportError:
    path_settings = {}
from datetime import datetime

class GeoC3Sv201912Ts(base_reader.GeoC3STs):
    # Reader implementation that uses the PATH configuration from above
    # Flagging should be done with the masking adapter from pytesmo
    _t0_ref = ('t0', datetime(1970,1,1,0,0,0))

    _col_fillvalues = {'sm': [-9999.0],
                       'sm_uncertainty': [-9999.0],
                       _t0_ref[0]: [-3440586.5]}

    _ds_implemented = [('C3S', 'v201912', 'COMBINED', 'DAILY', 'TCDR'),
                       ('C3S', 'v201912', 'ACTIVE', 'DAILY', 'TCDR'),
                       ('C3S', 'v201912', 'PASSIVE', 'DAILY', 'TCDR'),
                       ('C3S', 'v201912', 'COMBINED', 'MONTHLY', 'TCDR'),
                        ('C3S', 'v201912', 'ACTIVE', 'MONTHLY', 'TCDR'),
                        ('C3S', 'v201912', 'PASSIVE', 'MONTHLY', 'TCDR'),
                       ('C3S', 'v201912', 'COMBINED', 'DEKADAL', 'TCDR'),
                       ('C3S', 'v201912', 'ACTIVE', 'DEKADAL', 'TCDR'),
                       ('C3S', 'v201912', 'PASSIVE', 'DEKADAL', 'TCDR')]

    def __init__(self, dataset_or_path, force_path_group=None, **kwargs):
        """
        Parameters
        ----------
        dataset : tuple or string
            e.g. ('C3S', 'v201812', 'COMBINED', 'TCDR')
        force_path_group : str, optional (default: None)
            Select a specific path group from the path config to read.
        kwargs :
            kwargs that are passed to load_path and to initialise the reader.
        """
        if isinstance(dataset_or_path, list):
            dataset_or_path = tuple(dataset_or_path)

        self.dataset = dataset_or_path
        path_config = path_settings[self.dataset] if self.dataset in path_settings.keys() else None
        self.path_config = PathConfig(self.dataset, path_config)
        ts_path = self.path_config.load_path(force_path_group=force_path_group)

        super(GeoC3Sv201912Ts, self).__init__(ts_path, **kwargs)

# check if datasets in reader and in dict match
assert sorted(list(path_settings.keys())) == sorted(GeoC3Sv201912Ts._ds_implemented)


