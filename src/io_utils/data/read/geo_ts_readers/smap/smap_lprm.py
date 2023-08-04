# -*- coding: utf-8 -*-
from io_utils.data.read.geo_ts_readers.lprm.base_reader import LPRMTs
from io_utils.data.read.path_config import PathConfig
path_settings = {}

class GeoSMAPLPRMv6Ts(LPRMTs):
    # Reader implementation that uses the PATH configuration from above

    # implememted subversion that have a set path configuration
    _ds_implemented = []

    _t0 = 'SCANTIME_MJD'

    def __init__(self, dataset_or_path, force_path_group=None,
                 **kwargs):

        if isinstance(dataset_or_path, list):
            dataset_or_path = tuple(dataset_or_path)

        self.dataset = dataset_or_path

        path_config = path_settings[self.dataset] if self.dataset in path_settings.keys() else None
        self.path_config = PathConfig(self.dataset, path_config)
        ts_path = self.path_config.load_path(force_path_group=force_path_group)

        super(GeoSMAPLPRMv6Ts, self).__init__(ts_path, **kwargs)


# check if datasets in reader and in dict match
assert sorted(list(path_settings.keys())) == sorted(GeoSMAPLPRMv6Ts._ds_implemented)
