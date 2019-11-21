# -*- coding: utf-8 -*-

"""
Time series reader for CCI SM v045 data
"""
# TODO:
#   (+)
#---------
# NOTES:
#   -

from src.io_utils.read.time_series.path_config import PathConfig
from src.io_utils.read.time_series.esa_cci_sm.base_reader import CCITs
import numpy as np
from datetime import datetime
import pandas as pd

from src.io_utils.read.time_series.esa_cci_sm.paths_esa_cci_sm_v04 import path_settings



class GeoCCISMv4Ts(CCITs):
    # Reader implementation that uses the PATH configuration from above

    # exact time variable (days) from reference date
    _t0_ref = ('t0', datetime(1970,1,1,0,0,0))

    # fill values in the data columns
    _col_fillvalues = {'sm': [-9999.0],
                       'sm_uncertainty': [-9999.0],
                       _t0_ref[0]: [-9999.0]}

    # implememted subversion that have a set path configuration
    _ds_implemented = [('ESA_CCI_SM', 'v045', 'COMBINED'),
                       ('ESA_CCI_SM', 'v045', 'ACTIVE'),
                       ('ESA_CCI_SM', 'v045', 'PASSIVE'),
                       ('ESA_CCI_SM', 'v044', 'COMBINED'),
                       ('ESA_CCI_SM', 'v044', 'ACTIVE'),
                       ('ESA_CCI_SM', 'v044', 'PASSIVE')]


    def __init__(self, dataset, exact_index=False, **kwargs):
        self.dataset = dataset

        self.path_config = PathConfig(self.dataset, path_settings[self.dataset])
        ts_path = self.path_config.load_path()

        super(GeoCCISMv4Ts, self).__init__(ts_path, **kwargs)

        self.exact_index = exact_index
        if exact_index and (self.parameters is not None):
            self.parameters.append(self._t0_ref[0])


    def _replace_with_nan(self, df):
        """
        Replace the fill values in columns defined in _col_fillvalues with NaN
        """
        for col in df.columns:
            if col in self._col_fillvalues.keys():
                for fv in self._col_fillvalues[col]:
                    if self.scale_factors is not None and \
                            col in self.scale_factors.keys():
                        fv = fv * self.scale_factors[col]
                    df.loc[df[col] == fv, col] = np.nan
        return df

    def _add_time(self, df):
        t0 = self._t0_ref[0]
        if t0 in df.columns:
            df[t0] = pd.Series(index=df.index, data=self._t0_ref[1]) + \
                       pd.to_timedelta(df[t0], unit='d')
        if self.exact_index:
            df = df.set_index(t0)

        return df

    def read(self, *args, **kwargs):
        return self._add_time(self._replace_with_nan(
             super(GeoCCISMv4Ts, self).read(*args, **kwargs)))



# check if datasets in reader and in dict match
assert sorted(list(path_settings.keys())) == sorted(GeoCCISMv4Ts._ds_implemented)
