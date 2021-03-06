from io_utils.read.path_config import PathConfig
from io_utils.read.geo_ts_readers.scatsar_swi.base_reader import ScatSarCGLSReader
try:
    from io_utils.path_configs.scatsar.paths_scatsar_cgls import path_settings
except ImportError:
    path_settings = {}

class GeoScatSarCGLSReader(ScatSarCGLSReader):

    _ds_implemented = [('SCATSAR', 'CGLS', 'C0418', 'E7')]

    def __init__(self, dataset_or_path, force_path_group=None, grid_sampling=500,
                 **kwargs):

        if isinstance(dataset_or_path, list):
            dataset_or_path = tuple(dataset_or_path)

        self.dataset = dataset_or_path
        path_config = path_settings[self.dataset] if self.dataset in path_settings.keys() else None
        self.path_config = PathConfig(self.dataset, path_config)
        path = self.path_config.load_path(force_path_group=force_path_group)

        super(GeoScatSarCGLSReader, self).__init__(path, grid_sampling=grid_sampling,
                                                   **kwargs)


if __name__ == '__main__':
    import pandas as pd
    import os

    cgls_path = r"C:\Temp\delete_me\cgls"

    ds = GeoScatSarCGLSReader(cgls_path, grid_sampling=1000)
    ts = ds.read(19.1222, 47.201232) # type: pd.DataFrame
    ts.to_csv(os.path.join(r'C:\Temp\laura', 'abs_cgls.csv'))
    #print(ts.index)
    #print(ts['1'])
    #ts = pd.read_csv(r'C:\Temp\scatsarts.csv', index_col=0, parse_dates=True)