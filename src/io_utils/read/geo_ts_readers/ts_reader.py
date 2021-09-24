# -*- coding: utf-8 -*-

"""
Combines dataset config readers, adapters and some more features for all readers.
"""

# TODO: pass multiple selfmasking adapters that are applied sequentially?

import pandas as pd
import numpy as np
from io_utils.utils import filter_months, ddek
import warnings
from collections.abc import Iterable
import io_utils.read.geo_ts_readers.adapters as adapters

def load_settings(setts_file):
    s = open(setts_file, 'r').read()
    settings = eval(s)
    return settings


class GeoTsReader(object):

    def __init__(self,
                 cls,
                 reader_kwargs=None,
                 read_func_name='read',
                 adapters=None,
                 resample=None,
                 filter_months=None,
                 params_rename=None,
                 remove_nans=None):

        """
        Collects geopath-readers and calls them based on the dataset name,
        adds masking and climatology and allow resampling

        Parameters
        ----------
        cls : Object
            A dataset reader with a path implementation
            e.g. readers.GeoCCISMv4Ts
        reader_kwargs: dict, optional (default: None)
            Kwargs that are used to initialise the base reader.
        read_func_name: str, optional (default: 'read')
            Name of the read function to use. At the moment it is not possible
            give additional parameters to the read function.
            e.g. parameters, io_kwargs etc.
        adapters : dict(str, dict), optional (default: None)
            The names of adapters that are implemented. Either in
            adapters.py or in pytesmo.validation_framework.adapters as keys.
            Will be applied in the passed order.
            e.g.
                {'01-SelfMaskingAdapter': {'op' : '<=', 'threshold' : 50,
                                           'column_name' : 'sm'},
                 '02-AnomalyClimAdapter': {'columns': ['sm'],
                                           'wraparound': True,
                                           'timespan': ['1900-01-01', '2099-12-31']}
                }
        resample : tuple, optional (default: None)
            A frequency and method to resample the read, masked, transformed, data
            e.g. ('M', 'mean'), calls resample('M').mean(), other predefined methods
            are mean, median, min, max etc. Can also be a generic method, then
            resample('M').apply(method) is called, but this might be slower!!
        filter_months : list, optional (default: None)
            List of months (1-12) that are kept, data for other months is replaced
            by nan. We select month via index.month.
        params_rename : dict, optional (default: None)
            A lookup table for renaming parameters. This is done at the very end.
            e.g. {'sm' : 'ESA CCI SM Soil Moisture'}
        remove_nans : float or int or dict, optional (default: None)
            Replace fill values in time series. Either
                - dict of form {parameter: {val_to_replace: replacement_val}, ... }
                - dict of form {parameter : val_to_set_NaN ...}
                - A number to replace this number with nan anywhere
                - None to do nothing
        """

        if reader_kwargs is None:
            reader_kwargs = {}

        if 'network' in reader_kwargs.keys():
            if isinstance(reader_kwargs['network'], str) and \
                reader_kwargs['network'].lower() in ['all', 'none']:
                reader_kwargs['network'] = None

        self.reader_kwargs = reader_kwargs
        self.read_func_name = read_func_name
        self.params_rename = params_rename
        self.filter_months = filter_months
        self.resample = resample

        if isinstance(remove_nans, dict):
            for var, is_should in remove_nans.copy().items():
                if not isinstance(is_should, dict):
                    remove_nans[var] = {is_should: np.nan}
        self.remove_nans = remove_nans

        self.adapters = adapters

        cls = cls(**self.reader_kwargs)

        self.grid = cls.grid if hasattr(cls, 'grid') else None

        self.base_reader = cls # the unadaptered input reader
        self._adapt(self.base_reader) # the adapted reader to use
        setattr(self, read_func_name, self._read)


    def __str__(self):
        reader_class_str = self.reader.__class__.__name__

        adapters = list(self.adapters.keys()) \
            if self.adapters is not None else ['no Adapters']

        adapters_str = ', '.join(adapters)

        return '{} with {}'.format(reader_class_str, adapters_str)


    def _adapt(self, reader):
        """ Apply adapters to reader, e.g. anomaly adapter, mask adapter, ... """
        reader = adapters.BasicAdapter(reader, read_name=self.read_func_name)
        if self.adapters is not None:
            id = -1
            for adapter_name, adapter_kwargs in self.adapters.items():
                assert '-' in adapter_name, "Adapter must be of form 'id-AdapterName'"
                i, adapter_name = adapter_name.split('-')
                i = int(i)
                assert i > id, "Wrong order of passed adapters"
                id = i
                Adapter = getattr(adapters, adapter_name)
                reader = Adapter(reader, read_name=self.read_func_name,
                                 **adapter_kwargs)

        self.reader = reader

    def _read(self, *args, **kwargs):
        """ Read data for a location, by gpi or by lonlat """

        df: pd.DataFrame = getattr(self.reader,
                                   self.read_func_name)(*args, **kwargs)

        if self.remove_nans:
            if isinstance(self.remove_nans, (int, float)):
                df = df.replace(self.remove_nans, np.nan)
            else:
                df = df.replace(self.remove_nans)

        # filtering is done after adapting
        if self.filter_months is not None:
            df = filter_months(df, months=self.filter_months, dropna=False)

        # Resampling is done AFTER reading the original data, masking, climadapt.etc
        if self.resample is not None:
            df = self._resample(df)

        # Renaming is done last.
        if self.params_rename is not None:
            df.rename(columns=self.params_rename, inplace=True)

        return df

    def _resample(self, df):
        method = self.resample[1]

        if self.resample[0].lower() == 'ddekad':
            groups = df.groupby(ddek)
        else:
            groups = None

        df = df.select_dtypes(np.number)
        if isinstance(method, str):
            a = groups if groups is not None else df.resample(self.resample[0])
            df = eval('a.{}()'.format(method)) # todo: ?? better solution?
        else:
            warnings.warn('Appling a resampling method is slow, use a string that pandas can use, e.g. mean!')
            if groups is None:
                groups = df.resample(self.resample[0])
            df = groups.apply(method, axis=0)

        df.freq = self.resample[0]

        return df

    def read_multiple(self, locs, var='sm', dtype='float32'):
        """
        Read a list of locations, either from gpis, from lonlats or from a grid.
        Applies all the filtering and conversion from the reader generation.
        This simply orders the locs by cells for bulk reading and take the selected
        column received from the read() function for each location.

        Parameters
        ----------
        locs : list
            Either a set of locations [gpi,...] or [(lon, lat), ...]
        var : str, optional (default: 'sm')
            Variable to take from the dataframe that the read() function returns.

        Returns
        -------
        df : pd.DataFrame
            Dataframe of time series for the var of all locs, named by gpi.
        """

        if self.grid is None:
            raise ValueError("No grid found for the current reader.")

        gpis = {}

        for loc in locs:
            if isinstance(loc, Iterable):
                gpi = self.grid.find_nearest_gpi(*loc)[0]
            else:
                gpi = loc

            cell = self.grid.gpi2cell(gpi)
            if cell not in gpis.keys():
                gpis[cell] = []
            else:
                gpis[cell].append(gpi)

        print(f'Read {len(locs)} locations in {len(list(gpis.keys()))} cells')

        data = []

        i = 0
        for cell, cell_gpis in gpis.items():
            for gpi in cell_gpis:
                print(f'Reading loc {i} of {len(locs)}')
                try:
                    df = self._read(gpi)[[var]].rename(columns={var: gpi})
                except:
                    warnings.warn(f'Reading TS for GPI {gpi} failed. Continue.')
                    continue
                if not df.empty: data.append(df.astype(dtype))
                i += 1

        data = pd.concat(data, axis=1, sort=True)
        return data

