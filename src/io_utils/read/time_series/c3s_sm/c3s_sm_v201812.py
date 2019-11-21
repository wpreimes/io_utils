# -*- coding: utf-8 -*-

"""
Time series reader for ERA5 and ERA5 Land data
"""
# TODO:
#   (+)
#---------
# NOTES:
#   -

from src.io_utils.read.time_series.path_config import PathConfig
from src.io_utils.read.time_series.c3s_sm import base_reader
import numpy as np
from src.io_utils.read.time_series.c3s_sm.paths_c3s_sm_v201812 import path_settings


class GeoC3Sv201812Ts(base_reader.C3STs):
    # Reader implementation that uses the PATH configuration from above
    # Flagging should be done with the masking adapter from pytesmo

    _col_fillvalues = {'sm': [-9999.0],
                       'sm_uncertainty': [-9999.0]}

    _ds_implemented = [('C3S', 'v201812', 'COMBINED', 'TCDR'),
                       ('C3S', 'v201812', 'ACTIVE', 'TCDR'),
                       ('C3S', 'v201812', 'PASSIVE', 'TCDR')]

    def __init__(self, dataset, **kwargs):
        """
        Parameters
        ----------
        dataset : tuple
            e.g. ('C3S', 'v201812', 'COMBINED', 'TCDR')
        kwargs
        """
        self.dataset = tuple(dataset)
        self.path_config = PathConfig(self.dataset, path_settings[self.dataset])
        ts_path = self.path_config.load_path()

        super(GeoC3Sv201812Ts, self).__init__(ts_path, **kwargs)

    def _replace_with_nan(self, df):
        """
        Replace the fill values in columns defined in __new__ with NaN
        """
        for col in df.columns:
            if col in self._col_fillvalues.keys():
                for fv in self._col_fillvalues[col]:
                    if self.scale_factors is not None and \
                            col in self.scale_factors.keys():
                        fv = fv * self.scale_factors[col]
                    df.loc[df[col] == fv, col] = np.nan
        return df

    def read(self, *args, **kwargs):
        return self._replace_with_nan(
            super(GeoC3Sv201812Ts, self).read(*args, **kwargs))

# check if datasets in reader and in dict match
assert sorted(list(path_settings.keys())) == sorted(GeoC3Sv201812Ts._ds_implemented)

