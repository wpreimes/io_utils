# -*- coding: utf-8 -*-

"""
Time series reader for C3S v201812 active, combined and passive data
"""
# TODO:
#   (+)
#---------
# NOTES:
#   -

from io_utils.data.read.path_config import PathConfig
from io_utils.data.read.geo_ts_readers.c3s_sm import base_reader
try:
    from io_utils.data.path_configs.c3s_sm.paths_c3s_sm_v201812 import path_settings
except ImportError:
    path_settings = {}
import pandas as pd
from datetime import datetime

class GeoC3Sv201812Ts(base_reader.GeoC3STs):
    # Reader implementation that uses the PATH configuration from above
    # Flagging should be done with the masking adapter from pytesmo
    _t0_ref = ('t0', datetime(1970,1,1,0,0,0))

    _col_fillvalues = {'sm': [-9999.0],
                       'sm_uncertainty': [-9999.0],
                       _t0_ref[0]: [-3440586.5, -9999.]}

    _ds_implemented = [('C3S', 'v201812', 'COMBINED', 'DAILY', 'TCDR'),
                       ('C3S', 'v201812', 'ACTIVE', 'DAILY', 'TCDR'),
                       ('C3S', 'v201812', 'PASSIVE', 'DAILY', 'TCDR'),
                       ('C3S', 'v201812', 'COMBINED', 'MONTHLY', 'TCDR'),
                       ('C3S', 'v201812', 'ACTIVE', 'MONTHLY', 'TCDR'),
                       ('C3S', 'v201812', 'PASSIVE', 'MONTHLY', 'TCDR'),
                       ('C3S', 'v201812', 'COMBINED', 'DEKADAL', 'TCDR'),
                       ('C3S', 'v201812', 'ACTIVE', 'DEKADAL', 'TCDR'),
                       ('C3S', 'v201812', 'PASSIVE', 'DEKADAL', 'TCDR')]

    def __init__(self, dataset_or_path, force_path_group=None, **kwargs):
        """
        Parameters
        ----------
        dataset_or_path : tuple or str
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

        super(GeoC3Sv201812Ts, self).__init__(ts_path, **kwargs)


class GeoC3Sv201812FullCDRTs(object):
    # combines the TCDR and ICDR readers and reads data at once

    _ds_implemented = [('C3S', 'v201812', 'COMBINED', 'DAILY'),
                       ('C3S', 'v201812', 'ACTIVE', 'DAILY'),
                       ('C3S', 'v201812', 'PASSIVE', 'DAILY')]

    def __init__(self, dataset, exact_index=False, **kwargs):
        """
        Parameters
        ----------
        dataset : tuple WITHOUT TCDR or ICDR
            e.g. ('C3S', 'v201812', 'COMBINED')
        """
        if isinstance(dataset, list):
            dataset = tuple(dataset)

        self.dataset = dataset
        tcdr_dataset = tuple(list(dataset) + ['TCDR'])
        icdr_dataset = tuple(list(dataset) + ['ICDR'])
        self.tcdr_reader = GeoC3Sv201812Ts(
            tcdr_dataset, exact_index=exact_index, **kwargs)
        self.icdr_reader = GeoC3Sv201812Ts(
            icdr_dataset, exact_index=exact_index, **kwargs)

        self.grid = self.tcdr_reader.grid

    def read(self, *args, **kwargs):
        return pd.concat([self.tcdr_reader.read(*args, **kwargs),
                          self.icdr_reader.read(*args, **kwargs)], axis=0)

# check if implementation match with paths
for ds in GeoC3Sv201812Ts._ds_implemented:
    assert ds in path_settings.keys()
# check if FullCDR implementation match with paths
for ds in GeoC3Sv201812FullCDRTs._ds_implemented:
    assert tuple(list(ds) + ['TCDR'])  in path_settings.keys()
    assert tuple(list(ds) + ['ICDR']) in path_settings.keys()

if __name__ == '__main__':
    ds = GeoC3Sv201812FullCDRTs(('C3S', 'v201812', 'COMBINED', 'DAILY'))
    ts = ds.read(609779)
