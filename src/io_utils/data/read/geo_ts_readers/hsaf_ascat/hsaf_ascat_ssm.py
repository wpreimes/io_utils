# -*- coding: utf-8 -*-
from io_utils.data.read.path_config import PathConfig
from io_utils.data.read.geo_ts_readers.hsaf_ascat import base_reader
try:
    from io_utils.data.path_configs.ascat.paths_hsaf_ascat_ssmcdr import path_settings
except ImportError:
    path_settings = {}

# Ascat index is always exact

class GeoHsafAscatSsmTs(base_reader.HSAFAscatSSMTs):

    _ds_implemented = [('HSAF_ASCAT', 'SSM', 'H115+H116')]

    def __init__(self, dataset_or_path, force_path_group=None,
                 **kwargs):
        """
        Parameters
        ----------
        dataset_or_path : tuple or str
            e.g. ('HSAF_ASCAT', 'SSM', 'H115+H116')
        force_path_group : str, optional (default: None)
            Select a specific path group from the path config to read.
        kwargs :
            kwargs that are passed to load_path and to initialise the reader.
        """
        if isinstance(dataset_or_path, list):
            dataset_or_path = tuple(dataset_or_path)

        self.dataset = dataset_or_path
        path_config = path_settings[self.dataset] if self.dataset in path_settings.keys() else None
        self.path_config = PathConfig(self.dataset, path_config)
        ts_path = self.path_config.load_path(force_path_group=force_path_group)

        super().__init__(ts_path, **kwargs)

    def read(self, *args, **kwargs):
        ts = super().read(*args, **kwargs)
        if self.parameters is not None:
            ts = ts[self.parameters]

        return ts


# check if datasets in reader and in dict match
assert sorted(list(path_settings.keys())) == sorted(GeoHsafAscatSsmTs._ds_implemented)

if __name__ == '__main__':
    ds = GeoHsafAscatSsmTs(('HSAF_ASCAT', 'SSM', 'H115+H116'),
            grid_path="/home/wpreimes/shares/radar/projects/H_SAF_CDOP3/05_deliverables_products/auxiliary/warp5_grid/TUW_WARP5_grid_info_2_3.nc")
    ts = ds.read(	-100.650 , 40)
    print(ts)
