from io_utils.read.path_config import PathConfig
from io_utils.read.geo_ts_readers.csar_cgls.base_reader_nc import S1CglsTs
import warnings
import os
try:
    from io_utils.path_configs.cgls_sm.paths_ssm_swi import path_settings
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

if __name__ == '__main__':
    ds = S1CglsTs("/home/wpreimes/shares/radar/Projects/QA4SM_HR/07_data/SERVICE_DATA/CGLS_SCATSAR_SWI1km/CGLS_SCATSAR_SWI1km_V1_0/")

    ds_new = GeoCglsNcTs('/home/wpreimes/shares/radar/Projects/QA4SM_HR/07_data/CGLS_TS_1_DEG/swi/')
    ts_new = ds_new.read(2.5, 47.)

    ds_old = GeoCglsNcTs('/home/wpreimes/shares/radar/Projects/QA4SM_HR/07_data/CGLS_TS_025_DEG/CGLS_SWI1km_V1.0_ts/')
    ts_old = ds_old.read(2.5, 47.)