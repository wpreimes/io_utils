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
from io_utils.globals import test_root


path_settings = \
    {
        ('ESA_CCI_SM', 'v047', 'COMBINED'):
        # paths will be tried in this order
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'CCI_47_D_TS',
                                         'combined'),
                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'CCI_47_D_TS',
                                         'combined'),
                 }),
                ('radar',
                 {
                     'win': os.path.join(root_path.r,
                                         'Datapool_processed',
                                         'ESA_CCI_SM',
                                         'ESA_CCI_SM_v04.7',
                                         '063_images_to_ts',
                                         'combined'),
                     'lin': os.path.join(root_path.r,
                                         'Datapool_processed',
                                         'ESA_CCI_SM',
                                         'ESA_CCI_SM_v04.7',
                                         '063_images_to_ts',
                                         'combined'),
                 }),
                ('__test',
                 {
                     'win': os.path.join(test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v047', 'combined'),
                     'lin': os.path.join(test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v047', 'combined')
                 } if test_root is not None else None)
            ]),

        ('ESA_CCI_SM', 'v047', 'ACTIVE'):
        # paths will be tried in this order
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'CCI_47_D_TS',
                                         'active'),
                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'CCI_47_D_TS',
                                         'active'),
                 }),
                ('radar',
                 {
                     'win': os.path.join(root_path.r,
                                         'Datapool_processed',
                                         'ESA_CCI_SM',
                                         'ESA_CCI_SM_v04.7',
                                         '063_images_to_ts',
                                         'active'),
                     'lin': os.path.join(root_path.r,
                                         'Datapool_processed',
                                         'ESA_CCI_SM',
                                         'ESA_CCI_SM_v04.7',
                                         '063_images_to_ts',
                                         'active'),
                 }),
                ('__test',
                 {
                     'win': os.path.join(test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v047', 'active'),
                     'lin': os.path.join(test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v047', 'active')
                 } if test_root is not None else None)
            ]),

        ('ESA_CCI_SM', 'v047', 'PASSIVE'):
        # paths will be tried in this order
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'CCI_47_D_TS',
                                         'passive'),
                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'CCI_47_D_TS',
                                         'passive'),
                 }),
                ('radar',
                 {
                     'win': os.path.join(root_path.r,
                                         'Datapool_processed',
                                         'ESA_CCI_SM',
                                         'ESA_CCI_SM_v04.7',
                                         '063_images_to_ts',
                                         'passive'),
                     'lin': os.path.join(root_path.r,
                                         'Datapool_processed',
                                         'ESA_CCI_SM',
                                         'ESA_CCI_SM_v04.7',
                                         '063_images_to_ts',
                                         'passive'),
                 }),
                ('__test',
                 {
                     'win': os.path.join(test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v047', 'passive'),
                     'lin': os.path.join(test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v047', 'passive')
                 } if test_root is not None else None)
            ]),

        ('ESA_CCI_SM', 'v045', 'COMBINED'):
            # paths will be tried in this order
            OrderedDict([
                ('local',
                    {
                        'win': os.path.join(root_path.d,
                                            'data-read',
                                            'CCI_45_D_TS',
                                            'combined'),
                        'lin': os.path.join(root_path.dr,
                                            'USERS',
                                            'wpreimes',
                                            'CCI_45_D_TS',
                                            'combined'),
                    }),
                ('radar',
                    {
                        'win': os.path.join(root_path.r,
                                            'Datapool_processed',
                                            'ESA_CCI_SM',
                                            'ESA_CCI_SM_v04.5',
                                            '063_images_to_ts',
                                            'combined'),
                        'lin': os.path.join(root_path.r,
                                            'Datapool_processed',
                                            'ESA_CCI_SM',
                                            'ESA_CCI_SM_v04.5',
                                            '063_images_to_ts',
                                            'combined'),
                    }),
                ('__test',
                    {
                        'win': os.path.join(test_root, '00_testdata', 'read',
                                            'esa_cci_sm', 'v045', 'combined'),
                        'lin': os.path.join(test_root, '00_testdata', 'read',
                                            'esa_cci_sm', 'v045', 'combined')
                    } if test_root is not None else None)
        ]),

        ('ESA_CCI_SM', 'v045', 'ACTIVE'):
        # paths will be tried in this order
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'CCI_45_D_TS',
                                         'active'),
                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'CCI_45_D_TS',
                                         'active'),
                 }),
                ('radar',
                 {
                     'win': os.path.join(root_path.r,
                                         'Datapool_processed',
                                         'ESA_CCI_SM',
                                         'ESA_CCI_SM_v04.5',
                                         '063_images_to_ts',
                                         'active'),
                     'lin': os.path.join(root_path.r,
                                         'Datapool_processed',
                                         'ESA_CCI_SM',
                                         'ESA_CCI_SM_v04.5',
                                         '063_images_to_ts',
                                         'active'),
                 }),
                ('__test',
                 {
                     'win': os.path.join(test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v045', 'active'),
                     'lin': os.path.join(test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v045', 'active')
                 } if test_root is not None else None)
            ]),

        ('ESA_CCI_SM', 'v045', 'PASSIVE'):
        # paths will be tried in this order
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'CCI_45_D_TS',
                                         'passive'),
                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'CCI_45_D_TS',
                                         'passive'),
                 }),
                ('radar',
                 {
                     'win': os.path.join(root_path.r,
                                         'Datapool_processed',
                                         'ESA_CCI_SM',
                                         'ESA_CCI_SM_v04.5',
                                         '063_images_to_ts',
                                         'passive'),
                     'lin': os.path.join(root_path.r,
                                         'Datapool_processed',
                                         'ESA_CCI_SM',
                                         'ESA_CCI_SM_v04.5',
                                         '063_images_to_ts',
                                         'passive'),
                 }),
                ('__test',
                 {
                     'win': os.path.join(test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v045', 'passive'),
                     'lin': os.path.join(test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v045', 'passive')
                 } if test_root is not None else None)
            ]),

        ('ESA_CCI_SM', 'v044', 'COMBINED'):
        # paths will be tried in this order
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'CCI_44_D_TS',
                                         'combined'),
                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'CCI_44_D_TS',
                                         'combined'),
                 }),
                ('radar',
                 {
                     'win': os.path.join(root_path.r,
                                         'Datapool_processed',
                                         'ESA_CCI_SM',
                                         'ESA_CCI_SM_v04.4',
                                         '073_images_to_ts',
                                         'combined'),
                     'lin': os.path.join(root_path.r,
                                         'Datapool_processed',
                                         'ESA_CCI_SM',
                                         'ESA_CCI_SM_v04.4',
                                         '073_images_to_ts',
                                         'combined'),
                 }),
                ('__test',
                 {
                     'win': os.path.join(test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v044', 'combined'),
                     'lin': os.path.join(test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v044', 'combined')
                 } if test_root is not None else None)
            ]),

        ('ESA_CCI_SM', 'v044', 'ACTIVE'):
        # paths will be tried in this order
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'CCI_44_D_TS',
                                         'active'),
                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'CCI_44_D_TS',
                                         'active'),
                 }),
                ('radar',
                 {
                     'win': os.path.join(root_path.r,
                                         'Datapool_processed',
                                         'ESA_CCI_SM',
                                         'ESA_CCI_SM_v04.4',
                                         '073_images_to_ts',
                                         'active'),
                     'lin': os.path.join(root_path.r,
                                         'Datapool_processed',
                                         'ESA_CCI_SM',
                                         'ESA_CCI_SM_v04.4',
                                         '073_images_to_ts',
                                         'active'),
                 }),
                ('__test',
                 {
                     'win': os.path.join(test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v044', 'active'),
                     'lin': os.path.join(test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v044', 'active')
                 } if test_root is not None else None)
            ]),

        ('ESA_CCI_SM', 'v044', 'PASSIVE'):
        # paths will be tried in this order
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'CCI_44_D_TS',
                                         'passive'),
                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'CCI_44_D_TS',
                                         'passive'),
                 }),
                ('radar',
                 {
                     'win': os.path.join(root_path.r,
                                         'Datapool_processed',
                                         'ESA_CCI_SM',
                                         'ESA_CCI_SM_v04.4',
                                         '073_images_to_ts',
                                         'passive'),
                     'lin': os.path.join(root_path.r,
                                         'Datapool_processed',
                                         'ESA_CCI_SM',
                                         'ESA_CCI_SM_v04.4',
                                         '073_images_to_ts',
                                         'passive'),
                 }),
                ('__test',
                 {
                     'win': os.path.join(test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v044', 'passive'),
                     'lin': os.path.join(test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v044', 'passive')
                 } if test_root is not None else None)
            ]),
    }