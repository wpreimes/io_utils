# -*- coding: utf-8 -*-

"""
Reader for SWI data from esa cci sm v4 sm data.
"""
from io_utils.read.path_config import PathConfig
from io_utils.read.geo_ts_readers.esa_cci_swi.base_reader import GeoCCISWITs
path_settings = {}

class GeoCCISWIv4Ts(GeoCCISWITs):
    # Reader implementation that uses the PATH configuration from above

    # fill values in the data columns
    _col_fillvalues = {}

    # implememted subversion that have a set path configuration
    _ds_implemented = []

    def __init__(self, dataset_or_path, force_path_group=None, **kwargs):
        """
        Parameters
        ----------
        dataset_or_path : tuple or str
            e.g. ('C3S', 'v201812', 'COMBINED', 'TCDR')
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

        super(GeoCCISWIv4Ts, self).__init__(ts_path, **kwargs)

# check if datasets in reader and in dict match
assert sorted(list(path_settings.keys())) == sorted(GeoCCISWIv4Ts._ds_implemented)