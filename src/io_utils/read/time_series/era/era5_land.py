# -*- coding: utf-8 -*-

"""
Time series reader for ERA5 and ERA5 Land data
"""
# TODO:
#   (+)
#---------
# NOTES:
#   -

from src.io_utils.read.time_series.era.base_reader import ERATs
from src.io_utils.read.time_series.path_config import PathConfig
import pandas as pd
from src.io_utils.read.time_series.era.paths_era5_land import path_settings

class GeoPathEra5LandTs(ERATs):
    # Reader implementation that uses the PATH configuration from above
    _ds_implemented = [('ERA5-Land', 'sm_precip_lai'),
                       ('ERA5-Land', 'snow'),
                       ('ERA5-Land', 'temperature')]

    def __init__(self, dataset, **kwargs):
        self.dataset = dataset
        self.path_config = PathConfig(self.dataset, path_settings[self.dataset])
        ts_path = self.path_config.load_path()
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
            A dictionary with a variable group name as the index and a list
            of variables from that group as the value.
        kwargs :
            Keyword arguements that are passed to the reader. Are the same for
            ALL variable groups!!
        """
        if 'parameters' in kwargs.keys():
            raise ValueError("Pass the params together with the var groups.")
        self.readers = []
        for group, vars in group_vars.items():
            if isinstance(vars, str):
                vars = [vars]
            kwargs['parameters'] = vars
            ds = ('ERA5-Land', group)
            self.readers.append(GeoPathEra5LandTs(ds, **kwargs))

        self.grid = self.readers[0].grid
        assert all([self.grid == reader.grid for reader in self.readers])

    def read(self, *args, **kwargs):
        return pd.concat([r.read(*args, **kwargs) for r in self.readers],
                         axis=1)


if __name__ == '__main__':
    reader = GeoEra5LandTs(group_vars={'temperature': ['stl1'],
                                       'sm_precip_lai': ['swvl1']})
    ts = reader.read(15,45)