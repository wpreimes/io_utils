from io_utils.read.path_config import PathConfig
from pynetcf.time_series import GriddedNcOrthoMultiTs
from pygeogrids.netcdf import load_grid
import os
from io_utils.path_configs.ascat.paths_ascat_direx import path_settings
from io_utils.read.geo_ts_readers.mixins import OrthoMultiTsCellReaderMixin

class DirexTs(GriddedNcOrthoMultiTs, OrthoMultiTsCellReaderMixin):
    def __init__(self, ts_path, grid_path=None, **kwargs):
        if grid_path is None:
            grid_path = os.path.join(ts_path, "grid.nc")

        grid = load_grid(grid_path)
        super().__init__(ts_path, grid, **kwargs)


class GeoDirexTs(DirexTs):

    _ds_implemented = [('ASCAT', 'DIREX', 'v2', 'Senegal')]

    def __init__(self, dataset_or_path, force_path_group=None, **kwargs):

        if isinstance(dataset_or_path, list):
            dataset_or_path = tuple(dataset_or_path)

        self.dataset = dataset_or_path
        path_config = path_settings[self.dataset] if self.dataset in path_settings.keys() else None
        self.path_config = PathConfig(self.dataset, path_config)
        path = self.path_config.load_path(force_path_group=force_path_group)

        super().__init__(path, **kwargs)