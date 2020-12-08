from io_utils.read.path_config import PathConfig
from io_utils.read.geo_ts_readers.csar_ssm.base_reader import CSarSsmTiffReader
try:
    from io_utils.path_configs.csar.paths_csar_cgls import path_settings
except ImportError:
    path_settings = {}

class GeoCSarSsmTiffReader(CSarSsmTiffReader):

    _ds_implemented = [('CSAR', 'CGLS', 'SSM', '1km', 'V1.1', 'tiff')]

    def __init__(self, dataset_or_path, force_path_group=None, grid_sampling=500):

        if isinstance(dataset_or_path, list):
            dataset_or_path = tuple(dataset_or_path)

        self.dataset = dataset_or_path
        path_config = path_settings[self.dataset] if self.dataset in path_settings.keys() else None
        self.path_config = PathConfig(self.dataset, path_config)
        path = self.path_config.load_path(force_path_group=force_path_group)

        super(GeoCSarSsmTiffReader, self).__init__(path, grid_sampling=grid_sampling)

# check if datasets in reader and in dict match
assert sorted(list(path_settings.keys())) == sorted(GeoCSarSsmTiffReader._ds_implemented)

if __name__ == '__main__':
    ds = GeoCSarSsmTiffReader(('CSAR', 'CGLS', 'SSM', '1km', 'V1.1', 'tiff'))
    ts = ds.read(15.7,47)
    print(ts.loc['2020-08-17':'2020-08-30'])