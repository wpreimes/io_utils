from io_utils.read.path_config import PathConfig
from io_utils.read.geo_ts_readers.scatsar_swi.base_reader import ScatSarCglsSwiReader
import os
import warnings
try:
    from io_utils.path_configs.scatsar.paths_scatsar_cgls import path_settings
except ImportError:
    warnings.warn(f"Not paths imported for {os.path.basename(__file__)}")
    path_settings = {}

class GeoScatSarCglsSwiReader(ScatSarCglsSwiReader):

    _ds_implemented = [('SCATSAR', 'CGLS', 'C0418', 'E7')]

    def __init__(self, dataset_or_path, force_path_group=None, grid_sampling=500,
                 tval=5):

        if isinstance(dataset_or_path, list):
            dataset_or_path = tuple(dataset_or_path)

        self.dataset = dataset_or_path
        path_config = path_settings[self.dataset] if self.dataset in path_settings.keys() else None
        self.path_config = PathConfig(self.dataset, path_config)
        path = self.path_config.load_path(force_path_group=force_path_group)

        super(GeoScatSarCglsSwiReader, self).__init__(path, grid_sampling=grid_sampling,
                                                      tval=tval)
