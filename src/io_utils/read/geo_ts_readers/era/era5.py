# -*- coding: utf-8 -*-

"""
Time series reader for ERA5 and ERA5 Land data
"""
# TODO:
#   (+) 
#---------
# NOTES:
#   -

from io_utils.read.geo_ts_readers.era.base_reader import ERATs
from io_utils.read.path_config import PathConfig
from io_utils.path_configs.era.paths_era5 import path_settings

class GeoEra5Ts(ERATs):
    # Reader implementation that uses the PATH configuration from above

    _ds_implemented = [('ERA5', 'core')]

    def __init__(self, dataset, force_path_group=None, **kwargs):

        if isinstance(dataset, list):
            dataset = tuple(dataset)

        self.dataset = dataset
        self.path_config = PathConfig(self.dataset, path_settings[self.dataset])
        ts_path = self.path_config.load_path(force_path_group=force_path_group)
        super(GeoEra5Ts, self).__init__(ts_path, **kwargs)


# check if datasets in reader and in dict match
assert sorted(list(path_settings.keys())) == sorted(GeoEra5Ts._ds_implemented)

if __name__ == '__main__':
    reader = GeoEra5Ts(dataset=('ERA5', 'core'),
                       ioclass_kws={'read_bulk': True},
                       parameters=['swvl1'], scale_factors={'swvl1': 100.})
    ts = reader.read(15,48)
    print(ts)