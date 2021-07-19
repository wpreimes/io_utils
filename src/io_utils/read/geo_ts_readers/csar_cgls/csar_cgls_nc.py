from io_utils.read.path_config import PathConfig
from io_utils.read.geo_ts_readers.csar_cgls.base_reader_nc import S1CglsTs
import warnings
import os
try:
    from io_utils.path_configs.cgls_sm.paths_ssm_swi import path_settings
except ImportError:
    warnings.warn(f"Not paths imported for {os.path.basename(__file__)}")
    path_settings = {}


class GeoCglsNcReader(S1CglsTs):

    _ds_implemented = [('CSAR', 'CGLS', 'SSM', '1km', 'V1.1'),
                       ('CSAR', 'CGLS', 'SWI', '1km', 'V1.0'),
                       ]

    def __init__(self, dataset_or_path, force_path_group=None, **kwargs):

        if isinstance(dataset_or_path, list):
            dataset_or_path = tuple(dataset_or_path)

        self.dataset = dataset_or_path
        path_config = path_settings[self.dataset] if self.dataset in path_settings.keys() else None
        self.path_config = PathConfig(self.dataset, path_config)
        path = self.path_config.load_path(force_path_group=force_path_group)

        super(GeoCglsNcReader, self).__init__(path, **kwargs)

# check if each dataset in reader has a match in paths
assert all([p in path_settings.keys() for p in GeoCglsNcReader._ds_implemented])

if __name__ == '__main__':
    ds = GeoCglsNcReader('/home/wpreimes/shares/home/code/io_utils/tests/00_testdata/read/cgls/CGLS_SWI_TS_synthetic_hawaii')
    ts = ds.read(19.1222, 47.201232)