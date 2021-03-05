# -*- coding: utf-8 -*-
from pygeogrids.grids import CellGrid

import warnings
import numpy as np

from pygeobase.io_base import ImageBase, MultiTemporalImageBase
from pygeobase.object_base import Image
from pynetcf.time_series import GriddedNcOrthoMultiTs


from datetime import timedelta

from netCDF4 import Dataset
from pygeogrids.netcdf import load_grid
import pyproj

import os
import xarray as xr
from dask.diagnostics import ProgressBar
import pandas as pd



class CsarCglsNcDs:

    def __init__(self, root_path, chunks, filename_templ='*.nc', params=None):

        with ProgressBar():
            self.ds = xr.open_mfdataset(os.path.join(root_path, filename_templ),
                                        chunks=chunks, parallel=True)

        if params is None:
            self.params = [v for v in self.ds.variables.keys() if v not in self.ds.coords]
        else:
            self.params = [params] if isinstance(params, str) else params

    def read_ts(self, lon:float, lat:float) -> pd.DataFrame:
        # read time series for a specific location, NN lookup, max_dist=500m
        d = self.ds.sel({'lon':lon, 'lat':lat}, method='nearest', tolerance=500)
        return d[self.params].to_dataframe()


if __name__ == '__main__':
    from datetime import datetime
    chunks = {"lon": 50, 'lat': 50} # no time, i.e focus on reading TS
    ds = CsarCglsNcDs(r"R:\Datapool\CGLS\01_raw\SSM1km\V1.1\product", chunks=chunks,
                      filename_templ=f"*.nc", params=['ssm', 'ssm_noise'])
    lon, lat = -5, 41
    ts = ds.read_ts(lon, lat)
    print(ts, str(datetime.now()))
    lon, lat = -7, 42
    ts = ds.read_ts(lon, lat)
    print(ts,str(datetime.now()))
