# -*- coding: utf-8 -*-

"""
Time series reader for CCI SM v05 data
"""

from smecv_grid.grid import SMECV_Grid_v052
from io_utils.data.read.path_config import PathConfig
import numpy as np
from io_utils.data.read.geo_ts_readers.esa_cci_sm.base_reader import GriddedNcContiguousRaggedTsCompatible
from io_utils.data.read.geo_ts_readers.mixins import ContiguousRaggedTsCellReaderMixin
try:
    from io_utils.data.path_configs.esa_cci_sm.paths_esa_cci_sm_v07 import path_settings
except ImportError:
    path_settings = {}

# todo integrate exact index
class GeoCCISMv7IntermedNcTs(GriddedNcContiguousRaggedTsCompatible,
                             ContiguousRaggedTsCellReaderMixin):
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

        if 'grid' not in kwargs:
            kwargs['grid'] = SMECV_Grid_v052()

        super(GeoCCISMv7IntermedNcTs, self).__init__(ts_path, **kwargs)

        self.exact_index = exact_index

    def _read_gp(self, gpi, **kwargs):
        # override default args
        ts = super(GeoCCISMv7IntermedNcTs, self)._read_gp(gpi, **kwargs)
        if self.parameters is not None:
            ts = ts[self.parameters]
        if ts is not None:
            ts = ts.replace(self._fillval, np.nan)
        return ts

