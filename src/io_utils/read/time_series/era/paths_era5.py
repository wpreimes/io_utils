# -*- coding: utf-8 -*-

"""
Module description
"""
# TODO:
#   (+) 
#---------
# NOTES:
#   -
from collections import OrderedDict
import os
from rsroot import root_path

path_settings = \
    {
        ('ERA5', 'core'):
        # paths will be tried in this order
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'ERA5',
                                         'timeseries',
                                         'netcdf'),
                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'ERA5',
                                         'timeseries',
                                         'netcdf'),
                 }),
                ('radar',
                 {
                     'win': os.path.join(root_path.r,
                                         'Datapool_processed',
                                         'ECMWF_reanalysis',
                                         'ERA5',
                                         'datasets',
                                         'netcdf'),
                     'lin': os.path.join(root_path.r,
                                         'Datapool_processed',
                                         'ECMWF_reanalysis',
                                         'ERA5',
                                         'datasets',
                                         'netcdf'),
                 }),
                ('fallback',
                 {
                     'win': None,
                     'lin': None,
                 })
            ]),
    }
