# -*- coding: utf-8 -*-

# TODO:
#   (+) 
#---------
# NOTES:
#   -

import os
from collections import OrderedDict
import io_utils.root_path as root_path
import getpass


if root_path.test_root is not None:
    test_data_path = os.path.join(root_path.test_root, '00_testdata', 'read', 'cgls')
else:
    test_data_path = None

path_settings = \
    {
        ('CSAR', 'CGLS', 'SSM', '1km', 'V1.1'):
        # paths will be tried in this order
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'CGLS_SSM1km_V1.1',
                                         '02_processed',
                                         'time_series'),
                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         getpass.getuser(),
                                         'CGLS_SSM1km_V1.1',
                                         '02_processed',
                                         'time_series')
                 }),
                ('climers',
                 {
                     'win': os.path.join(root_path.m,
                                         'Projects',
                                         'QA4SM_HR',
                                         '07_data',
                                         'CGLS_SSM1km_V1.1_ts'),
                     'lin': os.path.join(root_path.m,
                                         'Projects',
                                         'QA4SM_HR',
                                         '07_data',
                                         'CGLS_SSM1km_V1.1_ts'),
                 }),
                ('__test',
                 {
                     'win': os.path.join(test_data_path, 'CGLS_SSM_TS_synthetic_hawaii'),
                     'lin': os.path.join(test_data_path, 'CGLS_SSM_TS_synthetic_hawaii')
                 } if root_path.test_root is not None else {'win' : None, 'lin' : None}),

            ]),

        ('CSAR', 'CGLS', 'SWI', '1km', 'V1.0'):
        # paths will be tried in this order
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'CGLS_SWI1km_V1.0',
                                         '02_processed',
                                         'time_series'),
                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         getpass.getuser(),
                                         'CGLS_SWI1km_V1.0',
                                         '02_processed',
                                         'time_series')
                 }),
                ('climers',
                 {
                     'win': os.path.join(root_path.m,
                                         'Projects',
                                         'QA4SM_HR',
                                         '07_data',
                                         'CGLS_SWI1km_V1.0_ts'),
                     'lin': os.path.join(root_path.m,
                                         'Projects',
                                         'QA4SM_HR',
                                         '07_data',
                                         'CGLS_SWI1km_V1.0_ts'),
                 }),
                ('__test',
                 {
                     'win': os.path.join(test_data_path, 'CGLS_SWI_TS_synthetic_hawaii'),
                     'lin': os.path.join(test_data_path, 'CGLS_SWI_TS_synthetic_hawaii')
                 } if root_path.test_root is not None else {'win' : None, 'lin' : None}),
            ]),

    }
