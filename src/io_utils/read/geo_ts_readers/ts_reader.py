# -*- coding: utf-8 -*-

"""
Combines dataset config readers, adapters and some more features for all readers.
"""

# TODO: pass multiple selfmasking adapters that are applied sequentially?

import pandas as pd
from pytesmo.validation_framework.adapters import SelfMaskingAdapter
from pytesmo.validation_framework.adapters import AnomalyClimAdapter
import matplotlib.pyplot as plt

resample_method_lut = {'mean' : pd.DataFrame.mean,
                       'max': pd.DataFrame.max,
                       'min': pd.DataFrame.min,
                       'median': pd.DataFrame.median}

def load_settings(setts_file):
    s = open(setts_file, 'r').read()
    settings = eval(s)
    return settings

class GeoTsReader(object):

    def __init__(self, cls, reader_kwargs=None, selfmaskingadapter_kwargs=None,
                 climadapter_kwargs=None, resample=None, params_rename=None):

        """
        Collects geopath-readers and calls them based on the dataset name,
        adds masking and climatology and allow resampling

        Parameters
        ----------
        cls : Object
            A dataset reader with a path implementation
            e.g. readers.GeoCCISMv4Ts
        parameters : list
            A list of parameters that are read for the dataset
            e.g. ['sm', 'swvl1', 'flag']
        selfmaskingadapter_kwargs : dict, optional (default: None)
            Dictionary that provides options to create ONE SelfMaskingAdapter
            for the dataset. Thas is applied after reading the params.
            e.g. dict(op='==', threshold=0, column_name='flag')}
        climadapter_kwargs : dict, optional (default: None)
            Dictionary that provides options to create a AnomalyClimAdapter
            for the dataset. That is applied after reading and masking the params.
            e.g. dict(columns=['sm'], timespan=[datetime(1991,1,1), datetime(2010,12,31)])
        resample : tuple, optional (default: None)
            A frequency and method to resample the read, masked, transformed, data
            e.g. ('M', pd.DataFrame.mean), method can also be a string then it will
            be looked up.
        params_rename : dict, optional (default: None)
            A lookup table for renaming parameters. This is done at the very end.
            e.g. {'sm' : 'ESA CCI SM Soil Moisture'}
        """

        if reader_kwargs is None:
            reader_kwargs = {}

        if 'network' in reader_kwargs.keys():
            if isinstance(reader_kwargs['network'], str) and \
                reader_kwargs['network'].lower() in ['all', 'none']:
                reader_kwargs['network'] = None

        self.reader_kwargs = reader_kwargs
        self.params_rename = params_rename
        self.resample=resample

        self.selfmaskingadapter_kwargs = selfmaskingadapter_kwargs
        self.climadapter_kwargs = climadapter_kwargs

        cls = cls(**self.reader_kwargs)

        self.grid = cls.grid

        self.reader = cls


    def __str__(self):
        reader_class_str = self.reader.__class__.__name__

        adapters = []
        if self.selfmaskingadapter_kwargs is not None:
            adapters.append('SelfMaskingAdapter')
        if self.climadapter_kwargs is not None:
            adapters.append('AnomalyClimAdapter')
        if len(adapters) == 0:
            adapters.append('no Adapters')

        adapters_str = ', '.join(adapters)

        return '{} with {}'.format(reader_class_str, adapters_str)


    @staticmethod
    def _method_from_lut(name):
        if name not in resample_method_lut.keys():
            raise ValueError('Method {} not implemented in GeoTsReaders')
        else:
            return resample_method_lut[name]

    def _adapt(self):
        """ Apply adapters to reader, e.g. anomaly adapter, mask adapter, ... """
        reader = self.reader

        if self.selfmaskingadapter_kwargs is not None:
            reader = SelfMaskingAdapter(reader, **self.selfmaskingadapter_kwargs)

        if self.climadapter_kwargs is not None:
            reader = AnomalyClimAdapter(reader, **self.climadapter_kwargs)

        return reader

    def read(self, *args, **kwargs):

        reader = self._adapt()

        df = reader.read(*args, **kwargs) # type: pd.DataFrame

        # Resampling is done AFTER reading the original data, masking, climadapt. etc
        if self.resample is not None:
            method = self.resample[1]
            if isinstance(method, str):
                method = self._method_from_lut(method)
            df = df.resample(self.resample[0]).apply(method)

        # Renaming is done last.
        if self.params_rename is not None:
            df = df.rename(columns=self.params_rename)

        return df

if __name__ == '__main__':
    from io_utils.read.geo_ts_readers import GeoMerra2Ts
    from io_utils.read.geo_ts_readers import GeoCCISMv4Ts
    merrareader = GeoTsReader(GeoMerra2Ts,
                reader_kwargs={'dataset': ('MERRA2', 'core'),
                               'parameters': ['SFMC'],
                               'ioclass_kws': {'read_bulk': True}},
                resample=('1D', pd.DataFrame.mean), params_rename={'SFMC': 'MERRA2 SFMC'})

    ccireader = GeoTsReader(GeoCCISMv4Ts,
                reader_kwargs={'dataset': ('ESA_CCI_SM', 'v045', 'COMBINED'),
                               'parameters': ['sm'],
                               'ioclass_kws': {'read_bulk': True}},
                resample=('1D', pd.DataFrame.mean), params_rename={'sm': 'ESA CCI SM'})

    ts_merra = merrareader.read(46.375, 18.625)
    ts_cci = ccireader.read(46.375, 18.625)

    df = pd.concat([ts_merra, ts_cci], axis=1)
    df_mean = df.rolling(30, min_periods=10).mean().dropna()

    from pytesmo.scaling import scale
    df_mean= scale(df_mean, 'mean_std', reference_index=1)

    df_mean['$\Delta$(CAN,REF)'] = df_mean['ESA CCI SM'] - df_mean['MERRA2 SFMC']

    df_mean = df_mean.loc['2007-01-01': '2018-12-31']
    ax = df_mean.plot()
    ax.hlines(0, df_mean.index[0], df_mean.index[-1])
    ax.vlines('2012-07-01', -0.05, 0.17, color='red', linewidth=5)
    from matplotlib.legend import _get_legend_handles
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
               ncol=3, mode="expand", borderaxespad=0.)
