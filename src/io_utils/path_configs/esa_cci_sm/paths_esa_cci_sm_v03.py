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
                ('__test',
                 {
                     'win': os.path.join(root_path.test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v033', 'passive'),
                     'lin': os.path.join(root_path.test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v033', 'passive')
                 } if root_path.test_root is not None else {'win' : None, 'lin' : None})
            ]),
    }