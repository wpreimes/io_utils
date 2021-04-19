# -*- coding: utf-8 -*-

"""
Time series reader for CCI SM v05 data
"""

from io_utils.read.path_config import PathConfig
import os
import numpy as np
import pandas as pd
import netCDF4 as nc
from datetime import timedelta
from io_utils.read.geo_ts_readers.esa_cci_sm.base_reader import CCITs
try:
    from io_utils.path_configs.esa_cci_sm.paths_esa_cci_sm_v05 import path_settings
except ImportError:
    path_settings = {}

class GeoCCISMv5Ts(CCITs):
    # Reader implementation that uses the PATH configuration from above

    # implememted subversion that have a set path configuration
    _ds_implemented = [('ESA_CCI_SM', 'v052', 'COMBINED'),
                       ('ESA_CCI_SM', 'v052', 'ACTIVE'),
                       ('ESA_CCI_SM', 'v052', 'PASSIVE')]

    _t0 = 't0'

    def __init__(self, dataset_or_path, exact_index=False, force_path_group=None,
                 **kwargs):

        if isinstance(dataset_or_path, list):
            dataset_or_path = tuple(dataset_or_path)

        self.dataset = dataset_or_path

        path_config = path_settings[self.dataset] if self.dataset in path_settings.keys() else None
        self.path_config = PathConfig(self.dataset, path_config)
        ts_path = self.path_config.load_path(force_path_group=force_path_group)

        super(GeoCCISMv5Ts, self).__init__(ts_path, **kwargs)

        self.exact_index = exact_index
        if exact_index and (self.parameters is not None):
            self.parameters.append(self._t0)

    def read_cell_file(self, cell, var):
        """
        Read a whole cell file

        Parameters
        ----------
        cell : int
            Cell / filename to read.
        var : str
            Name of the variable to extract from the cellfile.

        Returns
        -------
        data : np.array
            Data for var in cell
        """

        file_path = os.path.join(self.path, '{}.nc'.format("%04d" % (cell,)))
        with nc.Dataset(file_path) as ncfile:
            loc_id = ncfile.variables['location_id'][:]
            time = ncfile.variables['time'][:]
            unit_time = ncfile.variables['time'].units
            delta = lambda t: timedelta(t)
            vfunc = np.vectorize(delta)
            since = pd.Timestamp(unit_time.split('since ')[1])
            time = since + vfunc(time)
            variable = ncfile.variables[var][:]
            variable = np.transpose(variable)
            data = pd.DataFrame(variable, columns=loc_id, index=time)

            return data

# check if datasets in reader and in dict match
assert sorted(list(path_settings.keys())) == sorted(GeoCCISMv5Ts._ds_implemented)

if __name__ == '__main__':
    ds = GeoCCISMv5Ts(('ESA_CCI_SM', 'v052', 'COMBINED'), exact_index=True)
    ts52 = ds.read(45, 15)

