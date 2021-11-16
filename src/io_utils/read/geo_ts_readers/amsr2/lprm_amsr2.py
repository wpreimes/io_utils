# -*- coding: utf-8 -*-
from io_utils.read.geo_ts_readers.lprm.base_reader import LPRMTs
from io_utils.read.path_config import PathConfig
try:
    from io_utils.path_configs.amsr2.paths_amsr2_lprm_v6 import path_settings
except ImportError:
    path_settings = {}

class GeoAmsr2LPRMv6Ts(LPRMTs):
    # Reader implementation that uses the PATH configuration from above

    # implememted subversion that have a set path configuration
    _ds_implemented = [('AMSR2', 'LPRM', 'v6', 'ASC'),
                       ('AMSR2', 'LPRM', 'v6', 'DES')]

    _t0 = 'SCANTIME_MJD'

    def __init__(self, dataset_or_path, force_path_group=None,
                 **kwargs):

        if isinstance(dataset_or_path, list):
            dataset_or_path = tuple(dataset_or_path)

        self.dataset = dataset_or_path

        path_config = path_settings[self.dataset] if self.dataset in path_settings.keys() else None
        self.path_config = PathConfig(self.dataset, path_config)
        ts_path = self.path_config.load_path(force_path_group=force_path_group)

        super(GeoAmsr2LPRMv6Ts, self).__init__(ts_path, **kwargs)



# check if datasets in reader and in dict match
assert sorted(list(path_settings.keys())) == sorted(GeoAmsr2LPRMv6Ts._ds_implemented)

if __name__ == '__main__':
    ds = GeoAmsr2LPRMv6Ts(('AMSR2', 'LPRM', 'v6', 'ASC'),
                          exact_index=True,
                         ioclass_kws={'read_bulk': True})
    ts = ds.read(15,45)