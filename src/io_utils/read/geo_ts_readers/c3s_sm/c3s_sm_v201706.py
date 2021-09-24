# -*- coding: utf-8 -*-

"""
Time series reader for C3S v201706 active, combined and passive data
"""
# TODO:
#   (+)
#---------
# NOTES:
#   -

from io_utils.read.path_config import PathConfig
from io_utils.read.geo_ts_readers.c3s_sm import base_reader
import pandas as pd
from pytesmo.validation_framework.adapters import SelfMaskingAdapter
from datetime import datetime

try:
    from io_utils.path_configs.c3s_sm.paths_c3s_sm_v201706 import path_settings
except ImportError:
    path_settings = {}

class GeoC3Sv201706Ts(base_reader.GeoC3STs):
    # Reader implementation that uses the PATH configuration from above
    # Flagging should be done with the masking adapter from pytesmo

    # exact time variable (days) from reference date
    _t0_ref = ('t0', datetime(1970,1,1,0,0,0))

    # fill values in the data columns
    _col_fillvalues = {'sm': [-9999.0],
                       'sm_uncertainty': [-9999.0],
                       _t0_ref[0]: [-9999.0]}

    _ds_implemented = [('C3S', 'v201706', 'COMBINED', 'DAILY', 'TCDR'),
                       ('C3S', 'v201706', 'COMBINED', 'DAILY', 'ICDR'),
                       ('C3S', 'v201706', 'ACTIVE', 'DAILY', 'TCDR'),
                       ('C3S', 'v201706', 'ACTIVE', 'DAILY', 'ICDR'),
                       ('C3S', 'v201706', 'PASSIVE', 'DAILY', 'TCDR'),
                       ('C3S', 'v201706', 'PASSIVE', 'DAILY', 'ICDR')]

    def __init__(self, dataset_or_path, exact_index=False, force_path_group=None,
                 **kwargs):
        """
        Parameters
        ----------
        dataset : tuple or str
            e.g. ('C3S', 'v201706', 'COMBINED', 'TCDR') or path as string
        kwargs
        """
        if isinstance(dataset_or_path, list):
            dataset_or_path = tuple(dataset_or_path)

        self.dataset = dataset_or_path
        path_config = path_settings[self.dataset] if self.dataset in path_settings.keys() else None
        self.path_config = PathConfig(self.dataset, path_config)
        ts_path = self.path_config.load_path(force_path_group=force_path_group)

        super(GeoC3Sv201706Ts, self).__init__(ts_path, **kwargs)

        self.exact_index = exact_index
        if exact_index and (self.parameters is not None):
            self.parameters.append(self._t0_ref[0])


class GeoC3Sv201706FullCDRTs(object):
    # combines the TCDR and ICDR readers and reads data at once

    _ds_implemented = [('C3S', 'v201706', 'COMBINED', 'DAILY'),
                       ('C3S', 'v201706', 'ACTIVE', 'DAILY'),
                       ('C3S', 'v201706', 'PASSIVE', 'DAILY')]

    def __init__(self, dataset, exact_index=False, **kwargs):
        """
        Parameters
        ----------
        dataset : tuple WITHOUT TCDR or ICDR
            e.g. ('C3S', 'v201706', 'COMBINED')
        """
        if isinstance(dataset, list):
            dataset = tuple(dataset)

        self.dataset = dataset
        tcdr_dataset = tuple(list(dataset) + ['TCDR'])
        icdr_dataset = tuple(list(dataset) + ['ICDR'])
        self.tcdr_reader = GeoC3Sv201706Ts(
            tcdr_dataset, exact_index=exact_index, **kwargs)
        self.icdr_reader = GeoC3Sv201706Ts(
            icdr_dataset, exact_index=exact_index, **kwargs)

        self.grid = self.tcdr_reader.grid

    def read(self, *args, **kwargs):
        return pd.concat([self.tcdr_reader.read(*args, **kwargs),
                          self.icdr_reader.read(*args, **kwargs)], axis=0)


# check if implementation match with paths
for ds in GeoC3Sv201706Ts._ds_implemented:
    assert ds in path_settings.keys()
# check if FullCDR implementation match with paths
for ds in GeoC3Sv201706FullCDRTs._ds_implemented:
    assert tuple(list(ds) + ['TCDR'])  in path_settings.keys()
    assert tuple(list(ds) + ['ICDR']) in path_settings.keys()

# ==============================================================================
if __name__ == '__main__':
    for record in ['TCDR', 'ICDR']:
        for dataset in ['COMBINED', 'ACTIVE', 'PASSIVE']:
            reader = GeoC3Sv201706Ts(
                dataset_or_path=('C3S', 'v201706', dataset, 'DAILY', record),
                grid=None,
                exact_index=True,
                ioclass_kws={'read_bulk': True},
                parameters=['sm', 'sm_uncertainty', 'flag'],
                scale_factors={'sm': 100.})
            reader = SelfMaskingAdapter(reader, '==', 0, 'flag')
            ts = reader.read(-108,40)
            print(ts)