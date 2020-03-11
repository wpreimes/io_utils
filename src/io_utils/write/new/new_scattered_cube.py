# -*- coding: utf-8 -*-

"""
Module description
"""
# TODO:
#   (+) 
#---------
# NOTES:
#   -
from pynetcf.base import Dataset
import numpy as np
import pandas as pd
import xarray as xr
from datetime import datetime


init_ds = xr.Dataset(coords={'time': [], 'loc': []})

lons, lats = [10,11], [20,21]
other = xr.Dataset({'lon':(['loc'], lons),
                    'lat':(['loc'], lats),
                    'z':(['loc'], [1,1]),
                    'var1':(['time', 'loc'], np.random.rand(1, 2))},
                coords={'loc': [1,2],
                        'time': [datetime(2000,1,1)]})

merged = init_ds.merge(other, join='outer')

lons, lats = [10.1,11], [20.235,21]
other = xr.Dataset({'lon':(['loc'], lons),
                    'lat':(['loc'], lats),
                    'z':(['loc'], [1,1]),
                    'var1':(['time', 'loc'], np.random.rand(1, 2))},
                coords={'loc': [3,4],
                        'time':[datetime(2000,1,2)]})

merged = merged.merge(other, join='outer')

merged.to_netcdf(r"C:\Temp\scatter_time.nc")

ds = xr.open_dataset(r"C:\Temp\scatter_time.nc")
df = ds.to_dataframe()
df['time'] = df.index.get_level_values('time')
df['loc'] = df.index.get_level_values('loc')
print(df.set_index(['lat', 'lon', 'time']))

###########################################################################


init_ds = xr.Dataset(coords={'loc': []})

lons, lats = [10,11], [20,21]
other = xr.Dataset({'lon':(['loc'], lons),
                    'lat':(['loc'], lats),
                    'z':(['loc'], [1,1]),
                    'var1':(['loc'], np.random.rand(2))},
                coords={'loc': [1,2]})

merged = init_ds.merge(other, join='outer')

lons, lats = [10.1,11], [20.235,21]
other = xr.Dataset({'lon':(['loc'], lons),
                    'lat':(['loc'], lats),
                    'z':(['loc'], [1,1]),
                    'var1':(['loc'], np.random.rand(2))},
                coords={'loc': [3,4]})

merged = merged.merge(other, join='outer')

merged.to_netcdf(r"C:\Temp\scatter_notime.nc")

ds = xr.open_dataset(r"C:\Temp\scatter_notime.nc")
df = ds.to_dataframe()
df['loc'] = df.index.get_level_values('loc')
print(df.set_index(['lat', 'lon']))

# if False:
#     init_ds = xr.Dataset(coords={'loc': []})
#
#     lons, lats = [10,11], [20,21]
#     other = xr.Dataset({'lon':(['loc'], lons),
#                         'lat':(['loc'], lats),
#                         'z':(['loc'], [1,1]),
#                         'time':(['loc'], [datetime(2000,1,1),datetime(2000,1,1)]),
#                         'var1':(['loc'], np.random.rand(2))},
#                     coords={'loc': [1,2]})
#
#     merged = init_ds.merge(other, join='outer')
#
#     lons, lats = [10.1,11], [20.235,21]
#     other = xr.Dataset({'lon':(['loc'], lons),
#                         'lat':(['loc'], lats),
#                         'z':(['loc'], [1,1]),
#                         'time':(['loc'], [datetime(2000,1,2),datetime(2000,1,2)]),
#                         'var1':(['loc'], np.random.rand(2))},
#                     coords={'loc': [3,4]})
#
#     merged = merged.merge(other, join='outer')
#
#     merged.to_netcdf(r"C:\Temp\tex.nc")



