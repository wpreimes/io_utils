from io_utils.read.path_config import PathConfig
from io_utils.read.geo_ts_readers.csar_cgls.base_reader import CSarTiffReader
import os
import warnings
try:
    from io_utils.path_configs.csar.paths_csar_cgls_swi import path_settings
except ImportError:
    warnings.warn(f"Not paths imported for {os.path.basename(__file__)}")
    path_settings = {}

class GeoCSarSwiTiffReader(CSarTiffReader):

    _ds_implemented = [('CSAR', 'CGLS', 'SWI', '1km', 'V1.0', 'geotiff')]

    def __init__(self, dataset_or_path, force_path_group=None, grid_sampling=500):

        if isinstance(dataset_or_path, list):
            dataset_or_path = tuple(dataset_or_path)

        self.dataset = dataset_or_path
        path_config = path_settings[self.dataset] if self.dataset in path_settings.keys() else None
        self.path_config = PathConfig(self.dataset, path_config)
        path = self.path_config.load_path(force_path_group=force_path_group)

        super(GeoCSarSwiTiffReader, self).__init__(path, grid_sampling=grid_sampling,
                                                   param_rename='swi')


# check if datasets in reader and in dict match
assert sorted(list(path_settings.keys())) == sorted(GeoCSarSwiTiffReader._ds_implemented)

if __name__ == '__main__':
    ds = GeoCSarSwiTiffReader(('CSAR', 'CGLS', 'SWI', '1km', 'V1.0', 'geotiff'))
    ts = ds.read(15.,45)
    print(ts.loc['2010-08-17':'2020-08-30'])