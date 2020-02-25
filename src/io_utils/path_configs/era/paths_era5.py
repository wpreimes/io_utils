# -*- coding: utf-8 -*-

from collections import OrderedDict
import os
import io_utils.root_path as root_path


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
                ('__test',
                 {
                     'win': os.path.join(root_path.test_root, '00_testdata', 'read',
                                         'era5', 'sm_tmp'),
                     'lin': os.path.join(root_path.test_root, '00_testdata', 'read',
                                         'era5', 'sm_tmp')
                 } if root_path.test_root is not None else None),
            ]),
    }
