# -*- coding: utf-8 -*-

"""
Combines dataset config readers, adapters and some more features for all readers.
"""

# TODO: pass multiple selfmasking adapters that are applied sequentially?

import pandas as pd
from pytesmo.validation_framework.adapters import AnomalyClimAdapter, AnomalyAdapter, SelfMaskingAdapter
import numpy as np
from io_utils.utils import filter_months
import warnings
from collections.abc import Iterable
from pytesmo.validation_framework.adapters import BasicAdapter


def load_settings(setts_file):
    s = open(setts_file, 'r').read()
    settings = eval(s)
    return settings

class GeoTsReader(object):

    def __init__(self, cls, reader_kwargs=None, selfmaskingadapter_kwargs=None,
                 climadapter_kwargs=None, resample=None, filter_months=None,
                 params_rename=None, remove_nans=None):

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
        selfmaskingadapter_kwargs : list, optional (default: None)
            Dictionary that provides options to create ONE SelfMaskingAdapter
            for the dataset. Thas is applied after reading the params.
            e.g. dict(op='==', threshold=0, column_name='flag')}
        climadapter_kwargs : dict, optional (default: None)
            Dictionary that provides options to create a AnomalyClimAdapter
            for the dataset. That is applied after reading and masking the params.
            e.g. dict(columns=['sm'], timespan=[datetime(1991,1,1), datetime(2010,12,31)])
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
        self.params_rename = params_rename
        self.filter_months = filter_months
        self.resample = resample

        if isinstance(remove_nans, dict):
            for var, is_should in remove_nans.copy().items():
                if not isinstance(is_should, dict):
                    remove_nans[var] = {is_should: np.nan}
        self.remove_nans = remove_nans

        self.selfmaskingadapter_kwargs = selfmaskingadapter_kwargs
        self.climadapter_kwargs = climadapter_kwargs

        cls = cls(**self.reader_kwargs)

        self.grid = cls.grid if hasattr(cls, 'grid') else None

        self.base_reader = cls # the unadaptered input reader
        self._adapt(self.base_reader) # the adapted reader to use


    def __str__(self):
        reader_class_str = self.reader.__class__.__name__

        adapters = []
        if self.selfmaskingadapter_kwargs is not None:
            adapters.append('SelfMaskingAdapter')
        if self.climadapter_kwargs is not None:
            adapters.append('AnomalyAdapter')
        if len(adapters) == 0:
            adapters.append('no Adapters')

        adapters_str = ', '.join(adapters)

        return '{} with {}'.format(reader_class_str, adapters_str)


    def _adapt(self, reader):
        """ Apply adapters to reader, e.g. anomaly adapter, mask adapter, ... """

        if self.selfmaskingadapter_kwargs is None and self.climadapter_kwargs is None:
            reader = BasicAdapter(reader)
        else:
            if self.selfmaskingadapter_kwargs is not None:
                # Multiple self masking adapters are possible
                if isinstance(self.selfmaskingadapter_kwargs, dict):
                    self.selfmaskingadapter_kwargs = [self.selfmaskingadapter_kwargs]
                for kwargs in self.selfmaskingadapter_kwargs:
                    reader = SelfMaskingAdapter(reader, **kwargs)

            if self.climadapter_kwargs is not None:
                if 'timespan' in self.climadapter_kwargs.keys():
                    anom_adapter = AnomalyClimAdapter
                else:
                    anom_adapter = AnomalyAdapter

                reader = anom_adapter(reader, **self.climadapter_kwargs)

        self.reader = reader

    def read(self, *args, **kwargs):
        """ Read data for a location, by gpi or by lonlat """
        df = self.reader.read(*args, **kwargs) # type: pd.DataFrame

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
            method = self.resample[1]
            df = df.select_dtypes(np.number)
            if isinstance(method, str):
                df = eval('df.resample(self.resample[0]).{}()'.format(method)) # todo: ?? better solution?
            else:
                warnings.warn('Appling a resampling method is slow, use a string that pandas can use, e.g. mean!')
                df = df.resample(self.resample[0]).apply(method, axis=0)
            df.freq = self.resample[0]

        # Renaming is done last.
        if self.params_rename is not None:
            df.rename(columns=self.params_rename, inplace=True)

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
                    df = self.read(gpi)[[var]].rename(columns={var: gpi})
                except:
                    warnings.warn(f'Reading TS for GPI {gpi} failed. Continue.')
                    continue
                if not df.empty: data.append(df.astype(dtype))
                i += 1

        data = pd.concat(data, axis=1, sort=True)
        return data

if __name__ == '__main__':
    from io_utils.read.geo_ts_readers import GeoC3Sv202012Ts
    from io_utils.read.geo_ts_readers import GeoTsReader

    reader = GeoTsReader(GeoC3Sv202012Ts,
                         reader_kwargs={'dataset_or_path':
                                            ['C3S', 'v202012', 'PASSIVE', 'MONTHLY', 'TCDR']})
    ds = reader.read(15,45)


    # reader = GeoTsReader(GeoHsafAscatSsmTs,
    #             reader_kwargs={'dataset_or_path': ('HSAF_ASCAT', 'SSM', 'H115+H116'),
    #                            'parameters': ['sm', 'proc_flag'],
    #                            'exact_index': True,
    #                            'ioclass_kws': {'read_bulk': True}},
    #             selfmaskingadapter_kwargs={'op': '==', 'threshold': 0,
    #                              'column_name': 'flag'},
    #             climadapter_kwargs={'columns': ['sm'],
    #                                 'wraparound': True,
    #                                 'timespan': [datetime(1991, 1, 1), datetime(2018, 12, 31)],
    #                                 'moving_avg_clim': 30},
    #             resample=None, params_rename={'sm': 'ascatsm'})
    # from io_utils.grid.grid_shp_adapter import GridShpAdapter
    # from smecv_grid.grid import SMECV_Grid_v052
    # adapter = GridShpAdapter(SMECV_Grid_v052('land'))
    # subgrid = adapter.create_subgrid(['Senegal']) # type: CellGrid
    # df = reader.read_multiple(var='ascatsm', locs=list(zip(subgrid.activearrlon,
    #                                                          subgrid.activearrlat)))
    # print(df)


    # ccireader.read_multiple(var='sm', *zip(subgrid.activearrlon, subgrid.activearrlat))
    # merrareader = GeoTsReader(GeoMerra2Ts,
    #             reader_kwargs={'dataset': ('MERRA2', 'core'),
    #                            'parameters': ['SFMC'],
    #                            'ioclass_kws': {'read_bulk': True}},
    #             resample=('1D', pd.DataFrame.mean),
    #             params_rename={'SFMC': 'MERRA2 SFMC'})
    #
    # ts_merra = merrareader.read(46.375, 18.625)
    # ts_cci = ccireader.read(46.375, 18.625)
    #
    # df = pd.concat([ts_merra, ts_cci], axis=1)
    # df_mean = df.rolling(30, min_periods=10).mean().dropna()
    #
    # from pytesmo.scaling import scale
    # df_mean= scale(df_mean, 'mean_std', reference_index=1)
    #
    # df_mean['$\Delta$(CAN,REF)'] = df_mean['ESA CCI SM'] - df_mean['MERRA2 SFMC']
    #
    # df_mean = df_mean.loc['2007-01-01': '2018-12-31']
    # ax = df_mean.plot()
    # ax.hlines(0, df_mean.index[0], df_mean.index[-1])
    # ax.vlines('2012-07-01', -0.05, 0.17, color='red', linewidth=5)
    # from matplotlib.legend import _get_legend_handles
    # plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
    #            ncol=3, mode="expand", borderaxespad=0.)
