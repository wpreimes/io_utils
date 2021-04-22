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
        ('ESA_CCI_SM', 'v052', 'COMBINED'):
        # paths will be tried in this order
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'CCI_52_D_TS',
                                         'combined'),
                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'CCI_52_D_TS',
                                         'combined'),
                 }),
                ('radar',
                 {
                     'win': os.path.join(root_path.r,
                                         'Datapool',
                                         'ESA_CCI_SM',
                                         '02_processed',
                                         'ESA_CCI_SM_v05.2',
                                         'timeseries',
                                         'combined'),
                     'lin': os.path.join(root_path.r,
                                         'Datapool',
                                         'ESA_CCI_SM',
                                         '02_processed',
                                         'ESA_CCI_SM_v05.2',
                                         'timeseries',
                                         'combined'),
                 }),
                ('__test',
                 {
                     'win': os.path.join(root_path.test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v052', 'combined'),
                     'lin': os.path.join(root_path.test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v052', 'combined')
                 } if root_path.test_root is not None else {'win' : None, 'lin' : None})
            ]),

        ('ESA_CCI_SM', 'v052', 'ACTIVE'):
        # paths will be tried in this order
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'CCI_52_D_TS',
                                         'active'),
                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'CCI_52_D_TS',
                                         'active'),
                 }),
                ('radar',
                 {
                     'win': os.path.join(root_path.r,
                                         'Datapool',
                                         'ESA_CCI_SM',
                                         '02_processed',
                                         'ESA_CCI_SM_v05.2',
                                         'timeseries',
                                         'active'),
                     'lin': os.path.join(root_path.r,
                                         'Datapool',
                                         'ESA_CCI_SM',
                                         '02_processed',
                                         'ESA_CCI_SM_v05.2',
                                         'timeseries',
                                         'active'),
                 }),
                ('__test',
                 {
                     'win': os.path.join(root_path.test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v052', 'active'),
                     'lin': os.path.join(root_path.test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v052', 'active')
                 } if root_path.test_root is not None else {'win' : None, 'lin' : None})
            ]),

        ('ESA_CCI_SM', 'v052', 'PASSIVE'):
        # paths will be tried in this order
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'CCI_52_D_TS',
                                         'passive'),
                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'CCI_52_D_TS',
                                         'passive'),
                 }),
                ('radar',
                 {
                     'win': os.path.join(root_path.r,
                                         'Datapool',
                                         'ESA_CCI_SM',
                                         '02_processed',
                                         'ESA_CCI_SM_v05.2',
                                         'timeseries',
                                         'passive'),
                     'lin': os.path.join(root_path.r,
                                         'Datapool',
                                         'ESA_CCI_SM',
                                         '02_processed',
                                         'ESA_CCI_SM_v05.2',
                                         'timeseries',
                                         'passive'),
                 }),
                ('__test',
                 {
                     'win': os.path.join(root_path.test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v052', 'passive'),
                     'lin': os.path.join(root_path.test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v052', 'passive')
                 } if root_path.test_root is not None else {'win' : None, 'lin' : None})
            ]),
    }