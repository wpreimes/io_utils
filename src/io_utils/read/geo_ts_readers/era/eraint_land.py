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
from io_utils.read.geo_ts_readers.path_config import PathConfig
from path_configs.era.paths_eraint_land import path_settings

class GeoEraIntGBG4Ts(ERATs):
    # Reader implementation that uses the PATH configuration from above
    _ds_implemented = [('ERAINT-Land', 'GBG4', 'core')]

    def __init__(self, dataset, **kwargs):
        self.dataset = dataset
        self.path_config = PathConfig(self.dataset, path_settings[self.dataset])
        ts_path = self.path_config.load_path()
        super(GeoEraIntGBG4Ts, self).__init__(ts_path, **kwargs)

# check if datasets in reader and in dict match
assert sorted(list(path_settings.keys())) == sorted(GeoEraIntGBG4Ts._ds_implemented)

if __name__ == '__main__':
    reader = GeoEraIntGBG4Ts(dataset=('ERAINT-Land', 'GBG4', 'core'),
                           resample='D', ioclass_kws={'read_bulk': True},
                           parameters=['39'], scale_factors={'39': 100.})
    ts = reader.read(15,48)
    print(ts)