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
from src.globals import get_test_root

path_settings = \
    {
        ('ERA5-Land', 'sm_precip_lai'):
            # paths will be tried in this order
            OrderedDict([
                ('local',
                    {
                        'win': os.path.join(root_path.d,
                                            'data-read',
                                            'ERA5-Land',
                                            'sm_precip_lai'),
                        'lin': os.path.join(root_path.dr,
                                              'USERS',
                                              'wpreimes',
                                              'ERA5-Land',
                                              'sm_precip_lai'),
                    }),
                ('local_radar',
                 {
                     'win': None,
                     'lin': os.path.join(root_path.dr,
                                         'RADAR',
                                         'Datapool_processed',
                                         'ERA5-Land',
                                         'sm_precip_lai'),
                 }),
                ('radar',
                    {
                        'win': os.path.join(root_path.r,
                                            'Datapool_processed',
                                            'ECMWF_reanalysis',
                                            'ERA5-Land',
                                            'datasets',
                                            'sm_precip_lai'),
                        'lin': os.path.join(root_path.r,
                                            'Datapool_processed',
                                            'ECMWF_reanalysis',
                                            'ERA5-Land',
                                            'datasets',
                                            'sm_precip_lai'),
                    }),
                ('_test',
                     {
                         'win': os.path.join(get_test_root(), 'test_data', 'read', 'era5_land', 'sm_precip_lai'),
                         'lin': os.path.join(get_test_root(), 'test_data', 'read', 'era5_land', 'sm_precip_lai')
                     }),
        ]),

        ('ERA5-Land', 'snow'):
            # paths will be tried in this order
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'ERA5-Land',
                                         'snow'),
                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'ERA5-Land',
                                         'snow'),
                 }),
                ('local_radar',
                 {
                     'win': None,
                     'lin': os.path.join(root_path.dr,
                                         'RADAR',
                                         'Datapool_processed',
                                         'ERA5-Land',
                                         'snow'),
                 }),
                ('radar',
                 {
                     'win': os.path.join(root_path.r,
                                         'Datapool_processed',
                                         'ECMWF_reanalysis',
                                         'ERA5-Land',
                                         'datasets',
                                         'snow'),
                     'lin': os.path.join(root_path.r,
                                         'Datapool_processed',
                                         'ECMWF_reanalysis',
                                         'ERA5-Land',
                                         'datasets',
                                         'snow'),
                 }),
            ]),

        ('ERA5-Land', 'temperature'):
        # paths will be tried in this order
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'ERA5-Land',
                                         'temperature'),
                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'ERA5-Land',
                                         'temperature'),
                 }),
                ('local_radar',
                 {
                     'win': None,
                     'lin': os.path.join(root_path.dr,
                                         'RADAR',
                                         'Datapool_processed',
                                         'ERA5-Land',
                                         'temperature'),
                 }),
                ('radar',
                 {
                     'win': os.path.join(root_path.r,
                                         'Datapool_processed',
                                         'ECMWF_reanalysis',
                                         'ERA5-Land',
                                         'datasets',
                                         'temperature'),
                     'lin': os.path.join(root_path.r,
                                         'Datapool_processed',
                                         'ECMWF_reanalysis',
                                         'ERA5-Land',
                                         'datasets',
                                         'temperature'),
                 }),
            ]),
    }
