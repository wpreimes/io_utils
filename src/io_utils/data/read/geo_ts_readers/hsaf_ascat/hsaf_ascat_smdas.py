# -*- coding: utf-8 -*-
from io_utils.data.read.path_config import PathConfig
from io_utils.data.read.geo_ts_readers.hsaf_ascat import base_reader
try:
    from io_utils.data.path_configs.ascat.paths_hsaf_ascat_smdas import path_settings
except ImportError:
    path_settings = {}

# Ascat index is always exact
class GeoHsafAscatSMDASTs(base_reader.HSAFAscatSMDASTs):

    _ds_implemented = [('HSAF_ASCAT', 'SMDAS2', 'H14')]

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

        super(GeoHsafAscatSMDASTs, self).__init__(ts_path, **kwargs)


# check if datasets in reader and in dict match
assert sorted(list(path_settings.keys())) == sorted(GeoHsafAscatSMDASTs._ds_implemented)

if __name__ == '__main__':
    ds = GeoHsafAscatSMDASTs(('HSAF_ASCAT', 'SMDAS2', 'H14'), parameters=['swi2'])
    ts = ds.read(-14,14)
    print(ts)
