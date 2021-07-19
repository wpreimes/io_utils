# -*- coding: utf-8 -*-

"""
Time series reader for CCI SM v06 data
"""

from io_utils.read.path_config import PathConfig
import numpy as np
from io_utils.read.geo_ts_readers.other_base_readers.cci_genio_base_reader import CCIDs
try:
    from io_utils.path_configs.esa_cci_sm.paths_esa_cci_sm_v06 import path_settings
except ImportError:
    path_settings = {}

class GeoCCISMv6GenioTs(CCIDs):
    # Reader implementation that uses the PATH configuration from above

    # implememted subversion that have a set path configuration
    _ds_implemented = []
    _fillval = -999999.

    def __init__(self, dataset_or_path, exact_index=False, force_path_group=None,
                 parameters=None, **kwargs):

        if exact_index:
            raise NotImplementedError

        if isinstance(dataset_or_path, list):
            dataset_or_path = tuple(dataset_or_path)

        if isinstance(parameters, str):
            parameters = [parameters]

        self.parameters = parameters
        self.dataset = dataset_or_path

        path_config = path_settings[self.dataset] if self.dataset in path_settings.keys() else None
        self.path_config = PathConfig(self.dataset, path_config)
        ts_path = self.path_config.load_path(force_path_group=force_path_group)

        super(GeoCCISMv6GenioTs, self).__init__(ts_path, **kwargs)

        self.exact_index = exact_index

    def _read_gp(self, gpi, **kwargs):
        # override default args
        ts = super(GeoCCISMv6GenioTs, self)._read_gp(gpi, **kwargs)
        if self.parameters is not None:
            ts = ts[self.parameters]
        return ts.replace(self._fillval, np.nan)

if __name__ == '__main__':
    from io_utils.read.geo_ts_readers.esa_cci_sm.esa_cci_sm_v06 import GeoCCISMv6Ts
    ds = GeoCCISMv6Ts(('ESA_CCI_SM', 'v0603_tmi', 'COMBINED'), exact_index=False)
    ts6 = ds.read(45, 15)
