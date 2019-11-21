# -*- coding: utf-8 -*-

"""
Module description
"""
# TODO:
#   (+) 
#---------
# NOTES:
#   -

import src.io_utils.read.time_series as readers
import pandas as pd
from pytesmo.validation_framework.adapters import AnomalyClimAdapter, SelfMaskingAdapter
import os
from pprint import pprint
from collections import OrderedDict


class GeoDsTsReader(object):
    # Implements Adapters for the
    # todo: Implement an Adaptor for the full, loaded DF, e.g. to filter for certain temperature thresholds?
    # todo: instead of temporal resampling, do temporal matching!
    # for all the used readers

    _readers = [readers.GeoCCISMv4Ts,
                readers.GeoC3Sv201812Ts,
                readers.GeoC3Sv201706Ts,
                readers.GeoC3Sv201706FullCDRTs,
                readers.GeoEra5Ts,
                readers.GeoEra5LandTs,
                readers.GeoEraIntGBG4Ts,
                readers.GeoGLDAS21Ts,
                readers.GeoGLDAS20Ts,
                readers.GeoMerra2Ts]

    def __init__(self, ds_params, ds_reader_kwargs=None, ds_params_names=None,
                 ds_maskadapter_kwargs=None, ds_climadapter_kwargs=None,
                 resample=('D', pd.DataFrame.mean)):
        """
        Create multiple readers of the passed data sets and read nearest location
        for them all.

        Parameters
        ----------
        ds_params : dict
            Dictionary of dataset names and variables from the respective dataset
            that are combined in the final data frame.
            e.g. {('ESA_CCI_SM', 'v045', 'COMBINED')' : ['sm', 'sm_uncertainty']}
        ds_reader_kwargs : dict, optional (default: None)
            Keywords arguments that are passed to the resp. readers.
            e.g. {('ESA_CCI_SM', 'v045', 'COMBINED') : {'dropna': True}}
        ds_params_names : dict
            Dictionary that provides names for dataset-parameter combinations
            that are used instead of the generated column name
            form: {(dataset, parameter) : new_name}
            e.g. {(('ESA_CCI_SM', 'v045', 'COMBINED'), 'sm') : 'CCI Soil Moisture'}
        ds_maskadapter_kwargs : dict
            Dictionary that provides options to create a SelfMaskingAdapter
            for a dataset, that is applied when reading the data.
            {('ESA_CCI_SM', 'v045', 'COMBINED'): dict(op='==', threshold=0, column_name='flag')}
        ds_climadapter_kwargs : dict
            Dictionary that provides options to create a AnomalyClimAdapter
            for a dataset, that is applied when reading the data.
            {('ESA_CCI_SM', 'v045', 'COMBINED'): dict(columns=['sm'],
                timespan=[datetime(1991,1,1), datetime(2010,12,31)])}
        resample : tuple or None, optional (default: ('D', pd.DataFrame.mean))
            First argument is the target temporal resolution of all time series.
            Second argument is a function that is applied to the data to resample
            it to the target resolution (pd.DataFrame.apply)
        """
        if ds_reader_kwargs is None:
            ds_reader_kwargs = {}

        self.ds_params = ds_params
        self.ds_reader_kwargs = ds_reader_kwargs
        self.resample = resample
        self.ds_param_names = ds_params_names

        if ds_maskadapter_kwargs is None:
            self.ds_maskadapter_kwargs = {}
        else:
            self.ds_maskadapter_kwargs = ds_maskadapter_kwargs

        if ds_climadapter_kwargs is None:
            self.ds_climadapter_kwargs = {}
        else:
            self.ds_climadapter_kwargs = ds_climadapter_kwargs

        self.datasets = self._extract_datasets()
        self.readers = self._collect_readers()

    def _collect_readers(self):
        """ Go through the readers and check if the dataset is implemented """
        readers = {}
        for ds in self.datasets:
            for reader in self._readers:
                if ds in reader._ds_implemented:
                    kwargs = {}
                    if ds in self.ds_reader_kwargs.keys():
                        kwargs.update(self.ds_reader_kwargs[ds])
                    if ds in self.ds_params:
                        if 'parameters' in kwargs.keys():
                            raise IOError('Parametes must be passed in the ds_params field.')
                        kwargs['parameters'] = self.ds_params[ds]

                    reader = reader(ds, **kwargs)
                    if ds in self.ds_maskadapter_kwargs:
                        reader = SelfMaskingAdapter(cls=reader, **self.ds_maskadapter_kwargs[ds])
                    if ds in self.ds_climadapter_kwargs:
                        reader = AnomalyClimAdapter(cls=reader, **self.ds_climadapter_kwargs[ds])
                    readers[ds] = reader

                    break

        if not sorted(list(readers.keys())) == sorted(self.datasets):
            missing_readers = []
            for ds in self.datasets:
                if ds not in list(readers.keys()):
                    missing_readers.append(ds)
            raise IOError("Missing readers for the following datasets: {}".format(missing_readers))

        return readers

    def _extract_datasets(self):
        """ Get the dataset names and do some input checks """
        datasets = list(self.ds_params.keys())
        for k in self.ds_reader_kwargs.keys():
            try:
                assert k in datasets
            except AssertionError:
                raise IOError('{}: Dataset was passed in the ds_reader_kwargs '
                              'but is not in list of dataset'.format(k))
        for k, c in self.ds_param_names.keys():
            try:
                assert k in datasets
            except AssertionError:
                raise IOError('{}: Dataset was passed in the ds_param_names '
                              'but is not in list of dataset'.format(k))
        for k in self.ds_maskadapter_kwargs.keys():
            try:
                assert k in datasets
            except AssertionError:
                raise IOError('{}: Dataset was passed in the ds_maskadapter_kwargs '
                              'but is not in list of dataset'.format(k))
        for k in self.ds_climadapter_kwargs.keys():
            try:
                assert k in datasets
            except AssertionError:
                raise IOError('{}: Dataset was passed in the ds_climadapter_kwargs '
                              'but is not in list of dataset'.format(k))
        return datasets

    def print_settings(self, todir=None):
        """
        Print all settings in a nice overview.

        Parameters
        ---------
        todir : str, optional (default: None)
            Write the settings to a text file in the passed path.
        """
        if todir:
            f = open(os.path.join(todir, "multi_reader_settings.txt"), 'w')
        else:
            f = None
        settings = OrderedDict([
            ('ds_params', OrderedDict(sorted(self.ds_params.items(), key=lambda t: t[0]))),
            ('ds_reader_kwargs', OrderedDict(sorted(self.ds_reader_kwargs.items(), key=lambda t: t[0]))),
            ('ds_param_names', OrderedDict(sorted(self.ds_param_names.items(), key=lambda t: t[0]))),
            ('ds_maskadapter_kwargs', OrderedDict(sorted(self.ds_maskadapter_kwargs.items(), key=lambda t: t[0]))),
            ('ds_climadapter_kwargs', OrderedDict(sorted(self.ds_climadapter_kwargs.items(), key=lambda t: t[0]))),
            ('resample', self.resample)])
        if f:
            f.write(str(settings))
        else:
            pprint(settings)

    def read_all(self, lon, lat):
        dfs = []
        for dataset, reader in self.readers.items():
            df = reader.read(*(lon, lat))
            if self.resample is not None:
                df = df.resample(self.resample[0]).apply(self.resample[1])

            rename = {}
            for c in df.columns.values:
                if (dataset, c) in self.ds_param_names.keys():
                    name = self.ds_param_names[(dataset, c)]
                else:
                    name = '{}__{}__{}'.format(c, 'from', '|'.join(dataset))
                rename[c] = name

            df = df.rename(columns=rename)
            dfs.append(df)
        return pd.concat(dfs, axis=1)
