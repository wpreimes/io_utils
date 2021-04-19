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
import io_utils.root_path as root_path

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
                                            'Datapool',
                                            'ECMWF_reanalysis',
                                            '02_processed',
                                            'ERA5-Land',
                                            'datasets',
                                            'sm_precip_lai'),
                        'lin': os.path.join(root_path.r,
                                            'Datapool',
                                            'ECMWF_reanalysis',
                                            '02_processed',
                                            'ERA5-Land',
                                            'datasets',
                                            'sm_precip_lai'),
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
                                         'Datapool',
                                         'ECMWF_reanalysis',
                                         '02_processed',
                                         'ERA5-Land',
                                         'datasets',
                                         'snow'),
                     'lin': os.path.join(root_path.r,
                                         'Datapool',
                                         'ECMWF_reanalysis',
                                         '02_processed',
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
                                         'Datapool',
                                         'ECMWF_reanalysis',
                                         '02_processed',
                                         'ERA5-Land',
                                         'datasets',
                                         'temperature'),
                     'lin': os.path.join(root_path.r,
                                         'Datapool',
                                         'ECMWF_reanalysis',
                                         '02_processed',
                                         'ERA5-Land',
                                         'datasets',
                                         'temperature'),
                 }),
            ]),

        ('ERA5-Land', 'testdata'):
        # paths will be tried in this order
            OrderedDict([
                ('__test',
                 {
                     'win': os.path.join(root_path.test_root, '00_testdata', 'read',
                                         'era5_land', 'sm_tmp'),
                     'lin': os.path.join(root_path.test_root, '00_testdata', 'read',
                                         'era5_land', 'sm_tmp')
                 } if root_path.test_root is not None else {'win' : None, 'lin' : None}),
            ]),
    }
