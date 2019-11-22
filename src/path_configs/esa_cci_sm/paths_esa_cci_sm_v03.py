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
from rsroot import root_path

from src.globals import get_test_root

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
                ('radar',
                    {
                        'win': os.path.join(root_path.r,
                                            'Datapool_processed',
                                            'ESA_CCI_SM',
                                            'ESA_CCI_SM_v03.3',
                                            '073_images_to_ts',
                                            'combined'),
                        'lin': os.path.join(root_path.r,
                                            'Datapool_processed',
                                            'ESA_CCI_SM',
                                            'ESA_CCI_SM_v03.3',
                                            '073_images_to_ts',
                                            'combined'),
                    }),
                ('_test',
                    {
                        'win': os.path.join(get_test_root(), 'test_data', 'read', 'esa_cci_sm', 'v033', 'combined'),
                        'lin': os.path.join(get_test_root(), 'test_data', 'read', 'esa_cci_sm', 'v033', 'combined')
                    })
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
                ('radar',
                 {
                     'win': os.path.join(root_path.r,
                                         'Datapool_processed',
                                         'ESA_CCI_SM',
                                         'ESA_CCI_SM_v03.3',
                                         '073_images_to_ts',
                                         'active'),
                     'lin': os.path.join(root_path.r,
                                         'Datapool_processed',
                                         'ESA_CCI_SM',
                                         'ESA_CCI_SM_v03.3',
                                         '073_images_to_ts',
                                         'active'),
                 }),
                ('_test',
                 {
                     'win': os.path.join(get_test_root(), 'test_data', 'read', 'esa_cci_sm', 'v033', 'active'),
                     'lin': os.path.join(get_test_root(), 'test_data', 'read', 'esa_cci_sm', 'v033', 'active')
                 })
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
                ('radar',
                 {
                     'win': os.path.join(root_path.r,
                                         'Datapool_processed',
                                         'ESA_CCI_SM',
                                         'ESA_CCI_SM_v03.3',
                                         '073_images_to_ts',
                                         'passive'),
                     'lin': os.path.join(root_path.r,
                                         'Datapool_processed',
                                         'ESA_CCI_SM',
                                         'ESA_CCI_SM_v03.3',
                                         '073_images_to_ts',
                                         'passive'),
                 }),
                ('_test',
                 {
                     'win': os.path.join(get_test_root(), 'test_data', 'read', 'esa_cci_sm', 'v033', 'passive'),
                     'lin': os.path.join(get_test_root(), 'test_data', 'read', 'esa_cci_sm', 'v033', 'passive')
                 })
            ]),
    }