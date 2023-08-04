# -*- coding: utf-8 -*-

"""
Module description
"""
# TODO:
#   (+) 
#---------
# NOTES:
#   -

import os
from collections import OrderedDict
import io_utils.root_path as root_path

path_settings = \
    {
        ('ESA_CCI_SM', 'v033', 'COMBINED'):
            # paths will be tried in this order
            OrderedDict([
                ('local',
                    {
                        'win': os.path.join(root_path.d,
                                            'data-read',
                                            'CCI_33_D_TS',
                                            'combined'),
                        'lin': os.path.join(root_path.dr,
                                            'USERS',
                                            'wpreimes',
                                            'CCI_33_D_TS',
                                            'combined'),
                    }),
                ('climers',
                    {
                        'win': os.path.join(root_path.m,
                                            'Datapool',
                                            'ESA_CCI_SM',
                                            '02_processed',
                                            'ESA_CCI_SM_v03.3',
                                            'timeseries',
                                            'combined'),
                        'lin': os.path.join(root_path.m,
                                            'Datapool',
                                            'ESA_CCI_SM',
                                            '02_processed',
                                            'ESA_CCI_SM_v03.3',
                                            'timeseries',
                                            'combined'),
                    }),
                ('__test',
                    {
                        'win': os.path.join(root_path.test_root,  '00_testdata', 'read',
                                            'esa_cci_sm', 'v033', 'combined'),
                        'lin': os.path.join(root_path.test_root, '00_testdata', 'read',
                                            'esa_cci_sm', 'v033', 'combined')
                    } if root_path.test_root is not None else {'win' : None, 'lin' : None})
        ]),

        ('ESA_CCI_SM', 'v033', 'ACTIVE'):
        # paths will be tried in this order
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'CCI_33_D_TS',
                                         'active'),
                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'CCI_33_D_TS',
                                         'active'),
                 }),
                ('climers',
                 {
                     'win': os.path.join(root_path.m,
                                         'Archive_Projects',
                                         'CCI_Soil_Moisture',
                                         '07_data',
                                         'ESA_CCI_SM_v03.3',
                                         '073_images_to_ts',
                                         'active'),
                     'lin': os.path.join(root_path.m,
                                         'Archive_Projects',
                                         'CCI_Soil_Moisture',
                                         '07_data',
                                         'ESA_CCI_SM_v03.3',
                                         '073_images_to_ts',
                                         'active'),
                 }),
                ('__test',
                 {
                     'win': os.path.join(root_path.test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v033', 'active'),
                     'lin': os.path.join(root_path.test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v033', 'active')
                 } if root_path.test_root is not None else {'win' : None, 'lin' : None})
            ]),

        ('ESA_CCI_SM', 'v033', 'PASSIVE'):
        # paths will be tried in this order
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'CCI_33_D_TS',
                                         'passive'),
                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'CCI_33_D_TS',
                                         'passive'),
                 }),
                ('climers',
                 {
                     'win': os.path.join(root_path.m,
                                         'Datapool',
                                         'ESA_CCI_SM',
                                         '02_processed',
                                         'ESA_CCI_SM_v03.3',
                                         'timeseries',
                                         'passive'),
                     'lin': os.path.join(root_path.m,
                                         'Datapool',
                                         'ESA_CCI_SM',
                                         '02_processed',
                                         'ESA_CCI_SM_v03.3',
                                         'timeseries',
                                         'passive'),
                 }),
                ('__test',
                 {
                     'win': os.path.join(root_path.test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v033', 'passive'),
                     'lin': os.path.join(root_path.test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v033', 'passive')
                 } if root_path.test_root is not None else {'win' : None, 'lin' : None})
            ]),
    }
