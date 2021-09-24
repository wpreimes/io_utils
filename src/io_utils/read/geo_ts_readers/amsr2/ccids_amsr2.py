# -*- coding: utf-8 -*-

"""
Read AMSR2 time series in cci format (merged freq bands)

TODO:
    - masking: Mask missing values by default?
    - clean up data more as returned by base reader or do it in the val frmwk?
"""
from io_utils.read.geo_ts_readers.other_base_readers.cci_genio_base_reader import CCIDs
from io_utils.read.path_config import PathConfig
from cadati.jd_date import jd2dt
try:
    from io_utils.path_configs.cci_comm_format.paths_cci_amsr2 import path_settings
except ImportError:
    path_settings = {}

class GeoCCIDsAmsr2Ts(CCIDs):
    _ds_implemented = [('CCIDs', 'v052', 'AMSR2', 'DES')]

    _t0 = 'jd0'

    def __init__(self, dataset_or_path, exact_index=False,
                 force_path_group=None, **kwargs):

        # TODO:
            # freqband 0=invalid, 16=C_band_1, 32=C_band_2, 32=C_band_
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

        if 'parameters' in kwargs.keys():
            self.parameters = kwargs.pop('parameters')
        else:
            self.parameters = None

        self.dataset = dataset_or_path
        path_config = path_settings[self.dataset] if self.dataset in path_settings.keys() else None
        self.path_config = PathConfig(self.dataset, path_config)
        ts_path = self.path_config.load_path(force_path_group=force_path_group)

        super(GeoCCIDsAmsr2Ts, self).__init__(ts_path, custom_dtype=None, **kwargs)

        self.exact_index = exact_index
        if self.exact_index and (self.parameters is not None):
            self.parameters.append(self._t0)

    def read(self, *args, **kwargs):
        data =  super(GeoCCIDsAmsr2Ts, self).read(*args, **kwargs,
                                                  only_valid=True)

        if self.parameters is not None:
            data = data[self.parameters]

        if self.exact_index:
            data[self._t0] = jd2dt(data[self._t0])
            data.set_index(self._t0, inplace=True)

        return  data
    # check if datasets in reader and in dict match

assert sorted(list(path_settings.keys())) == sorted(GeoCCIDsAmsr2Ts._ds_implemented)

if __name__ == '__main__':
    ds = GeoCCIDsAmsr2Ts(('CCIDs', 'v052', 'AMSR2', 'DES'),
                         exact_index=True,
                         parameters=['sm', 'flag', 'freqband'],
                         ioclass_kws={'read_bulk': True})
    ts = ds.read(0,20)