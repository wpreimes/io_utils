# -*- coding: utf-8 -*-

"""
Time series reader for CCI SM v03 data
"""
# TODO:
#   (+)
#---------
# NOTES:
#   -

from io_utils.read.path_config import PathConfig
from io_utils.read.geo_ts_readers.esa_cci_sm.base_reader import CCITs
import numpy as np
try:
    from io_utils.path_configs.esa_cci_sm.paths_esa_cci_sm_v03 import path_settings
except ImportError:
    path_settings = {}

class GeoCCISMv3Ts(CCITs):
    # Reader implementation that uses the PATH configuration from above

    # implememted subversion that have a set path configuration
    _ds_implemented = [('ESA_CCI_SM', 'v033', 'COMBINED'),
                       ('ESA_CCI_SM', 'v033', 'ACTIVE'),
                       ('ESA_CCI_SM', 'v033', 'PASSIVE')]

    _col_fillvalues = {'sm': [-9999.0],
                       'sm_uncertainty': [-9999.0],
                       't0': [-3440586.5]} # TODO: why this fill value for t0?


    def __init__(self, dataset_or_path, exact_index=False, force_path_group=None, **kwargs):

        if isinstance(dataset_or_path, list):
            dataset_or_path = tuple(dataset_or_path)

        self.dataset = dataset_or_path

        path_config = path_settings[self.dataset] if self.dataset in path_settings.keys() else None
        self.path_config = PathConfig(self.dataset, path_config)
        ts_path = self.path_config.load_path(force_path_group=force_path_group)

        super(GeoCCISMv3Ts, self).__init__(ts_path, exact_index=exact_index,
                                           **kwargs)

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

    def read(self, *args, **kwargs):
        return self._replace_with_nan(super(GeoCCISMv3Ts, self).read(*args, **kwargs))



# check if datasets in reader and in dict match
assert sorted(list(path_settings.keys())) == sorted(GeoCCISMv3Ts._ds_implemented)

if __name__ == '__main__':
    path = r"R:\Projects\CCI_Soil_Moisture_Phase_2\07_data\ESA_CCI_SM_v03.3\073_images_to_ts\combined"
    ds = GeoCCISMv3Ts(path, exact_index=False)
    ts = ds.read(45,15)