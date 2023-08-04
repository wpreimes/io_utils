from io_utils.data.read.path_config import PathConfig
from io_utils.data.read.geo_ts_readers.csar_cgls.base_reader_nc import S1CglsTs
import warnings
import os
try:
    from io_utils.data.path_configs.cgls_sm.paths_ssm_swi import path_settings
except ImportError:
    warnings.warn(f"Not paths imported for {os.path.basename(__file__)}")
    path_settings = {}


class GeoCglsNcTs(S1CglsTs):

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

        super().__init__(path, **kwargs)


# check if each dataset in reader has a match in paths
assert all([p in path_settings.keys() for p in GeoCglsNcTs._ds_implemented])
