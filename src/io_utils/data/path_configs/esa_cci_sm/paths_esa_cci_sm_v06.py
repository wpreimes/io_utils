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
        ('ESA_CCI_SM', 'v061', 'COMBINED'):
        # paths will be tried in this order
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'CCI_61_D_TS',
                                         'combined'),
                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'CCI_61_D_TS',
                                         'combined'),
                 }),
                ('climers',
                 {
                     'win': os.path.join(root_path.m,
                                         'Datapool',
                                         'ESA_CCI_SM',
                                         '02_processed',
                                         'ESA_CCI_SM_v06.1',
                                         'timeseries',
                                         'combined'),
                     'lin': os.path.join(root_path.m,
                                         'Datapool',
                                         'ESA_CCI_SM',
                                         '02_processed',
                                         'ESA_CCI_SM_v06.1',
                                         'timeseries',
                                         'combined'),
                 }),
                ('__test',
                 {
                     'win': os.path.join(root_path.test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v061', 'combined'),
                     'lin': os.path.join(root_path.test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v061', 'combined')
                 } if root_path.test_root is not None else {'win' : None, 'lin' : None})
            ]),
        ('ESA_CCI_SM', 'v061', 'ACTIVE'):
        # paths will be tried in this order
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'CCI_61_D_TS',
                                         'active'),
                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'CCI_61_D_TS',
                                         'active'),
                 }),
                ('climers',
                 {
                     'win': os.path.join(root_path.m,
                                         'Datapool',
                                         'ESA_CCI_SM',
                                         '02_processed',
                                         'ESA_CCI_SM_v06.1',
                                         'timeseries',
                                         'active'),
                     'lin': os.path.join(root_path.m,
                                         'Datapool',
                                         'ESA_CCI_SM',
                                         '02_processed',
                                         'ESA_CCI_SM_v06.1',
                                         'timeseries',
                                         'active'),
                 }),
                ('__test',
                 {
                     'win': os.path.join(root_path.test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v061', 'active'),
                     'lin': os.path.join(root_path.test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v061', 'active')
                 } if root_path.test_root is not None else {'win' : None, 'lin' : None})
            ]),
        ('ESA_CCI_SM', 'v061', 'PASSIVE'):
        # paths will be tried in this order
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'CCI_61_D_TS',
                                         'passive'),
                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'CCI_61_D_TS',
                                         'passive'),
                 }),
                ('climers',
                 {
                     'win': os.path.join(root_path.m,
                                         'Datapool',
                                         'ESA_CCI_SM',
                                         '02_processed',
                                         'ESA_CCI_SM_v06.1',
                                         'timeseries',
                                         'passive'),
                     'lin': os.path.join(root_path.m,
                                         'Datapool',
                                         'ESA_CCI_SM',
                                         '02_processed',
                                         'ESA_CCI_SM_v06.1',
                                         'timeseries',
                                         'passive'),
                 }),
                ('__test',
                 {
                     'win': os.path.join(root_path.test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v061', 'passive'),
                     'lin': os.path.join(root_path.test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v061', 'passive')
                 } if root_path.test_root is not None else {'win' : None, 'lin' : None})
            ]),
    }
