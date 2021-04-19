# -*- coding: utf-8 -*-

"""
Time series reader for SMOS data
"""

from io_utils.read.path_config import PathConfig
from io_utils.read.geo_ts_readers.smos.base_reader import SMOSTs
from collections import OrderedDict
try:
    from io_utils.path_configs.smos.paths_smos import path_settings
except ImportError:
    path_settings = {}

class GeoSMOSICTs(SMOSTs):
    # Reader implementation that uses the PATH configuration from above

    _ds_implemented = [('SMOS', 'IC', 'ASC'),
                       ('SMOS', 'IC', 'DES')]

    def __init__(self, dataset_or_path, force_path_group=None, **kwargs):

        if isinstance(dataset_or_path, list):
            dataset_or_path = tuple(dataset_or_path)

        self.dataset = dataset_or_path

        path_config = path_settings[self.dataset] if self.dataset in path_settings.keys() else None
        self.path_config = PathConfig(self.dataset, path_config)
        ts_path = self.path_config.load_path(force_path_group=force_path_group)
        super(GeoSMOSICTs, self).__init__(ts_path, **kwargs)


    def read_cells(self, cells):
        cell_data = OrderedDict()
        gpis, lons, lats = self.grid.grid_points_for_cell(list(cells))
        for gpi, lon, lat in zip(gpis, lons, lats):
            df = self.read(lon, lat)
            cell_data[gpi] = df
        return cell_data

# check if datasets in reader and in dict match
assert sorted(list(path_settings.keys())) == sorted(GeoSMOSICTs._ds_implemented)

if __name__ == '__main__':
    path_new = ('SMOS', 'IC', 'DES')
    ds = GeoSMOSICTs(path_new, exact_index=True)
    ts = ds.read(131.125, -29.875)


