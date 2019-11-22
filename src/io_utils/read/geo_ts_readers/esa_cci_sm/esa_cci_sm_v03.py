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
from io_utils.read.geo_ts_readers.esa_cci_sm.base_reader import CCITs
import numpy as np
from datetime import datetime
import pandas as pd
from collections import OrderedDict

from path_configs.esa_cci_sm.paths_esa_cci_sm_v03 import path_settings

class GeoCCISMv3Ts(CCITs):
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
            dt = pd.to_timedelta(df[t0], unit='d')
            df['t0'] = pd.Series(index=df.index, data=self._t0_ref[1]) + dt
            if self.exact_index:
                df = df.set_index('t0')
                df = df[df.index.notnull()]

        return df

    def read(self, *args, **kwargs):
        return self._add_time(self._replace_with_nan(
             super(GeoCCISMv3Ts, self).read(*args, **kwargs)))

    def read_cells(self, cells):
        cell_data = OrderedDict()
        gpis, lons, lats = self.grid.grid_points_for_cell(list(cells))
        for gpi, lon, lat in zip(gpis, lons, lats):
            df = self.read(lon, lat)
            cell_data[gpi] = df
        return cell_data


# check if datasets in reader and in dict match
assert sorted(list(path_settings.keys())) == sorted(GeoCCISMv3Ts._ds_implemented)
