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
import pandas as pd
try:
    from io_utils.path_configs.era.paths_era5_land import path_settings
except ImportError:
    path_settings = {}

class GeoPathEra5LandTs(ERATs):
    # Reader implementation that uses the PATH configuration from above
    _ds_implemented = [('ERA5-Land', 'sm_precip_lai'),
                       ('ERA5-Land', 'snow'),
                       ('ERA5-Land', 'temperature')]

    def __init__(self, dataset_or_path, force_path_group=None, **kwargs):

        if isinstance(dataset_or_path, list):
            dataset_or_path = tuple(dataset_or_path)

        self.dataset = dataset_or_path

        path_config = path_settings[self.dataset] if self.dataset in path_settings.keys() else None
        self.path_config = PathConfig(self.dataset, path_config)
        ts_path = self.path_config.load_path(force_path_group=force_path_group)

        super(GeoPathEra5LandTs, self).__init__(ts_path, **kwargs)

# check if datasets in reader and in dict match
assert sorted(list(path_settings.keys())) == sorted(GeoPathEra5LandTs._ds_implemented)

class GeoEra5LandTs(object):
    def __init__(self, group_vars, **kwargs):
        """
        Initialize the ERA5 reader(s) for multiple variable groups using their
        path configurations.

        Parameters
        ----------
        group_var : dict
            A dictionary with a variable group name as the index or a path
            and a list of variables from that group as the value.
        kwargs :
            Keyword arguements that are passed to the reader. Are the same for
            ALL variable groups!!
        """
        if 'parameters' in kwargs.keys():
            raise ValueError("Pass the params together with the var groups.")
        self.readers = []
        for group_or_path, vars in group_vars.items():
            if isinstance(vars, str):
                vars = [vars]
            kwargs['parameters'] = vars
            self.readers.append(GeoPathEra5LandTs(group_or_path, **kwargs))

        self.grid = self.readers[0].grid
        assert all([self.grid == reader.grid for reader in self.readers])

    def read(self, *args, **kwargs):
        return pd.concat([r.read(*args, **kwargs) for r in self.readers],
                         axis=1)

if __name__ == '__main__':
    force_path_group = '__test'
    reader = GeoEra5LandTs(group_vars={('ERA5-Land', 'temperature'): ['stl1'],
                                       ('ERA5-Land', 'sm_precip_lai'): ['swvl1']},
                           ioclass_kws={'read_bulk': True},
                           scale_factors={'swvl1': 1.},
                           force_path_group=force_path_group)
    ts = reader.read(15,45)