# -*- coding: utf-8 -*-

"""
Adapter that
"""
# TODO:
#   (+) 
#---------
# NOTES:
#   -

import pandas as pd
from pytesmo.validation_framework.adapters import SelfMaskingAdapter
from pytesmo.validation_framework.adapters import AnomalyClimAdapter
from datetime import datetime

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
            Dictionary that provides options to create a SelfMaskingAdapter
            for the dataset. Thas is applied after reading the params.
            e.g. dict(op='==', threshold=0, column_name='flag')}
        climadapter_kwargs : dict, optional (default: None)
            Dictionary that provides options to create a AnomalyClimAdapter
            for the dataset. That is applied after reading and masking the params.
            e.g. dict(columns=['sm'], timespan=[datetime(1991,1,1), datetime(2010,12,31)])
        resample : tuple, optional (default: None)
            A frequency and method to resample the read, masked, transformed, data
            e.g. ('M', pd.DataFrame.mean)
        params_rename : dict, optional (default: None)
            A lookup table for renaming parameters. This is done at the very end.
            e.g. {'sm' : 'ESA CCI SM Soil Moisture'}
        """

        if reader_kwargs is None:
            reader_kwargs = {}

        self.reader_kwargs = reader_kwargs
        self.params_rename = params_rename
        self.resample=resample

        cls = cls(**self.reader_kwargs)

        self.grid = cls.grid


        if selfmaskingadapter_kwargs is not None:
            cls = SelfMaskingAdapter(cls, **selfmaskingadapter_kwargs)

        if climadapter_kwargs is not None:
            cls = AnomalyClimAdapter(cls, **climadapter_kwargs)

        self.reader = cls

    def read(self, *args, **kwargs):
        df = self.reader.read(*args, **kwargs) # type: pd.DataFrame

        if self.resample is not None:
            df = df.resample(self.resample[0]).apply(self.resample[1])

        if self.params_rename is not None:
            df = df.rename(columns=self.params_rename)

        return df

if __name__ == '__main__':
    from io_utils.read.time_series.era.era5_land import GeoEra5LandTs
    cls = GeoEra5LandTs

    reader = GeoTsReader(cls,
                reader_kwargs={'var_groups': ['sm_precip_lai', 'temperature'],
                               'parameters': ['stl1', 'swvl1'],
                               'ioclass_kws': {'read_bulk': True}},
                selfmaskingadapter_kwargs={'op':'>=', 'threshold':277.15, 'column_name':'stl1'},
                climadapter_kwargs={'columns':['swvl1'], 'timespan':[datetime(1991,1,1), datetime(2010,12,31)]},
                resample=None, params_rename={'swvl1': 'ERA5LandSM'})
    ts = reader.read(15,45)


