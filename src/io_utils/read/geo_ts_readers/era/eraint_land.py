# -*- coding: utf-8 -*-

"""
Time series reader for ERA Interim Land data
"""
# TODO:
#   (+)
#---------
# NOTES:
#   -

from io_utils.read.geo_ts_readers.era.base_reader import ERATs
from io_utils.read.path_config import PathConfig
try:
    from io_utils.path_configs.era.paths_eraint_land import path_settings
except ImportError:
    path_settings = {}

class GeoEraIntGBG4Ts(ERATs):
    # Reader implementation that uses the PATH configuration from above
    _ds_implemented = [('ERAINT-Land', 'GBG4', 'core')]

    def __init__(self, dataset_or_path, force_path_group=None, **kwargs):

        if isinstance(dataset_or_path, list):
            dataset_or_path = tuple(dataset_or_path)

        self.dataset = dataset_or_path

        path_config = path_settings[self.dataset] if self.dataset in path_settings.keys() else None
        self.path_config = PathConfig(self.dataset, path_config)
        ts_path = self.path_config.load_path(force_path_group=force_path_group)

        super(GeoEraIntGBG4Ts, self).__init__(ts_path, **kwargs)

# check if datasets in reader and in dict match
assert sorted(list(path_settings.keys())) == sorted(GeoEraIntGBG4Ts._ds_implemented)

if __name__ == '__main__':
    reader = GeoEraIntGBG4Ts(dataset_or_path=('ERAINT-Land', 'GBG4', 'core'),
                           resample='D', ioclass_kws={'read_bulk': True},
                           parameters=['39'], scale_factors={'39': 100.})
    ts = reader.read(15,48)
    print(ts)