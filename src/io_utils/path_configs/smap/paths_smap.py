# -*- coding: utf-8 -*-

"""
Paths for different subversions / paramter combinations of SMAP Time Series.
"""

import os
from collections import OrderedDict
import io_utils.root_path as root_path


path_settings = \
    {
        ('SMAP', 'SP3SMPv5', 'ASC'):
            # paths will be tried in this order
            OrderedDict([
                ('local',
                    {
                        'win': os.path.join(root_path.d,
                                            'data-read',
                                            'SMAP_TS',
                                            'SPL3SMP.005',
                                            'PM_ascending'),
                        'lin': os.path.join(root_path.dr,
                                            'USERS',
                                            'wpreimes',
                                            'SMAP_TS',
                                            'SPL3SMP.005',
                                            'PM_ascending'),
                    }),
                ('radar',
                    {
                        'win': os.path.join(root_path.r,
                                            'Datapool_processed',
                                            'SMAP',
                                            'SPL3SMP_v5',
                                            'PM_ascending',
                                            'netcdf'),
                        'lin': os.path.join(root_path.r,
                                            'Datapool_processed',
                                            'SMAP',
                                            'SPL3SMP_v5',
                                            'PM_ascending',
                                            'netcdf'),
                    }),
                ('__test',
                    {
                        'win': os.path.join(root_path.test_root, '00_testdata', 'read',
                                            'SMAP', 'smap_spl3smpv5_asc'),
                        'lin': os.path.join(root_path.test_root, '00_testdata', 'read',
                                            'SMAP', 'smap_spl3smpv5_asc'),
                    } if root_path.test_root is not None else None),
            ]),
        ('SMAP', 'SP3SMPv5', 'DES'):
        # paths will be tried in this order
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'SMAP_TS',
                                         'SPL3SMP.005',
                                         'AM_descending',
                                         'netcdf'),
                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'SMAP_TS',
                                         'SPL3SMP.005',
                                         'AM_descending',
                                         'netcdf'),
                 }),
                ('radar',
                 {
                     'win': os.path.join(root_path.r,
                                         'Datapool_processed',
                                         'SMAP',
                                         'SPL3SMP_v5',
                                         'AM_descending',
                                         'netcdf'),
                     'lin': os.path.join(root_path.r,
                                         'Datapool_processed',
                                         'SMAP',
                                         'SPL3SMP_v5',
                                         'AM_descending',
                                         'netcdf'),
                 }),
                ('__test',
                 {
                     'win': os.path.join(root_path.test_root, '00_testdata', 'read',
                                         'SMAP', 'smap_spl3smpv5_asc'),
                     'lin': os.path.join(root_path.test_root, '00_testdata', 'read',
                                         'SMAP', 'smap_spl3smpv5_asc'),
                 } if root_path.test_root is not None else None),
            ]),

        ('SMAP', 'SP3SMPv6', 'ASC'):
            # paths will be tried in this order
            OrderedDict([
                ('local',
                    {
                        'win': os.path.join(root_path.d,
                                            'data-read',
                                            'SMAP_TS',
                                            'SPL3SMP.006',
                                            'PM_ascending'),
                        'lin': os.path.join(root_path.dr,
                                            'USERS',
                                            'wpreimes',
                                            'SMAP_TS',
                                            'SPL3SMP.006',
                                            'PM_ascending'),
                    }),
                ('radar',
                    {
                        'win': os.path.join(root_path.r,
                                            'Datapool_processed',
                                            'SMAP',
                                            'SPL3SMP_v6',
                                            'PM_ascending',
                                            'netcdf'),
                        'lin': os.path.join(root_path.r,
                                            'Datapool_processed',
                                            'SMAP',
                                            'SPL3SMP_v6',
                                            'PM_ascending',
                                            'netcdf'),
                    }),
                ('__test',
                    {
                        'win': os.path.join(root_path.test_root, '00_testdata', 'read',
                                            'SMAP', 'smap_spl3smpv5_asc'),
                        'lin': os.path.join(root_path.test_root, '00_testdata', 'read',
                                            'SMAP', 'smap_spl3smpv5_asc'),
                    } if root_path.test_root is not None else None),
            ]),
        ('SMAP', 'SP3SMPv6', 'DES'):
        # paths will be tried in this order
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'SMAP_TS',
                                         'SPL3SMP.006',
                                         'AM_descending',
                                         'netcdf'),
                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'SMAP_TS',
                                         'SPL3SMP.006',
                                         'AM_descending',
                                         'netcdf'),
                 }),
                ('radar',
                 {
                     'win': os.path.join(root_path.r,
                                         'Datapool_processed',
                                         'SMAP',
                                         'SPL3SMP_v6',
                                         'AM_descending',
                                         'netcdf'),
                     'lin': os.path.join(root_path.r,
                                         'Datapool_processed',
                                         'SMAP',
                                         'SPL3SMP_v6',
                                         'AM_descending',
                                         'netcdf'),
                 }),
                ('__test',
                 {
                     'win': os.path.join(root_path.test_root, '00_testdata', 'read',
                                         'SMAP', 'smap_spl3smpv5_asc'),
                     'lin': os.path.join(root_path.test_root, '00_testdata', 'read',
                                         'SMAP', 'smap_spl3smpv5_asc'),
                 } if root_path.test_root is not None else None),
            ]),
    }