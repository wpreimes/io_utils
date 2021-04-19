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
                                         'Datapool',
                                         'ESA_CCI_SM',
                                         '02_processed',
                                         'ESA_CCI_SM_v04.7',
                                         'timeseries',
                                         'combined'),
                     'lin': os.path.join(root_path.r,
                                         'Datapool',
                                         'ESA_CCI_SM',
                                         '02_processed',
                                         'ESA_CCI_SM_v04.7',
                                         'timeseries',
                                         'combined'),
                 }),
                ('__test',
                 {
                     'win': os.path.join(root_path.test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v047', 'combined'),
                     'lin': os.path.join(root_path.test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v047', 'combined')
                 } if root_path.test_root is not None else {'win' : None, 'lin' : None})
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
                                         'Datapool',
                                         'ESA_CCI_SM',
                                         '02_processed',
                                         'ESA_CCI_SM_v04.7',
                                         'timeseries',
                                         'active'),
                     'lin': os.path.join(root_path.r,
                                         'Datapool',
                                         'ESA_CCI_SM',
                                         '02_processed',
                                         'ESA_CCI_SM_v04.7',
                                         'timeseries',
                                         'active'),
                 }),
                ('__test',
                 {
                     'win': os.path.join(root_path.test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v047', 'active'),
                     'lin': os.path.join(root_path.test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v047', 'active')
                 } if root_path.test_root is not None else {'win' : None, 'lin' : None})
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
                                         'Datapool',
                                         'ESA_CCI_SM',
                                         '02_processed',
                                         'ESA_CCI_SM_v04.7',
                                         'timeseries',
                                         'passive'),
                     'lin': os.path.join(root_path.r,
                                         'Datapool',
                                         'ESA_CCI_SM',
                                         '02_processed',
                                         'ESA_CCI_SM_v04.7',
                                         'timeseries',
                                         'passive'),
                 }),
                ('__test',
                 {
                     'win': os.path.join(root_path.test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v047', 'passive'),
                     'lin': os.path.join(root_path.test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v047', 'passive')
                 } if root_path.test_root is not None else {'win' : None, 'lin' : None})
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
                                            'Projects',
                                            'CCI_Soil_Moisture_Phase_2',
                                            '07_data',
                                            'ESA_CCI_SM_v04.5',
                                            '063_images_to_ts',
                                            'combined'),
                        'lin': os.path.join(root_path.r,
                                            'Projects',
                                            'CCI_Soil_Moisture_Phase_2',
                                            '07_data',
                                            'ESA_CCI_SM_v04.5',
                                            '063_images_to_ts',
                                            'combined'),
                    }),
                ('__test',
                    {
                        'win': os.path.join(root_path.test_root, '00_testdata', 'read',
                                            'esa_cci_sm', 'v045', 'combined'),
                        'lin': os.path.join(root_path.test_root, '00_testdata', 'read',
                                            'esa_cci_sm', 'v045', 'combined')
                    } if root_path.test_root is not None else {'win' : None, 'lin' : None})
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
                                         'Projects',
                                         'CCI_Soil_Moisture_Phase_2',
                                         '07_data',
                                         'ESA_CCI_SM_v04.5',
                                         '063_images_to_ts',
                                         'active'),
                     'lin': os.path.join(root_path.r,
                                         'Projects',
                                         'CCI_Soil_Moisture_Phase_2',
                                         '07_data',
                                         'ESA_CCI_SM_v04.5',
                                         '063_images_to_ts',
                                         'active'),
                 }),
                ('__test',
                 {
                     'win': os.path.join(root_path.test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v045', 'active'),
                     'lin': os.path.join(root_path.test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v045', 'active')
                 } if root_path.test_root is not None else {'win' : None, 'lin' : None})
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
                                         'Projects',
                                         'CCI_Soil_Moisture_Phase_2',
                                         '07_data',
                                         'ESA_CCI_SM_v04.5',
                                         '063_images_to_ts',
                                         'passive'),
                     'lin': os.path.join(root_path.r,
                                         'Projects',
                                         'CCI_Soil_Moisture_Phase_2',
                                         '07_data',
                                         'ESA_CCI_SM_v04.5',
                                         '063_images_to_ts',
                                         'passive'),
                 }),
                ('__test',
                 {
                     'win': os.path.join(root_path.test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v045', 'passive'),
                     'lin': os.path.join(root_path.test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v045', 'passive')
                 } if root_path.test_root is not None else {'win' : None, 'lin' : None})
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
                                         'Projects',
                                         'CCI_Soil_Moisture_Phase_2',
                                         '07_data',
                                         'ESA_CCI_SM_v04.4',
                                         '073_images_to_ts',
                                         'combined'),
                     'lin': os.path.join(root_path.r,
                                         'Projects',
                                         'CCI_Soil_Moisture_Phase_2',
                                         '07_data',
                                         'ESA_CCI_SM_v04.4',
                                         '073_images_to_ts',
                                         'combined'),
                 }),
                ('__test',
                 {
                     'win': os.path.join(root_path.test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v044', 'combined'),
                     'lin': os.path.join(root_path.test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v044', 'combined')
                 } if root_path.test_root is not None else {'win' : None, 'lin' : None})
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
                                         'Projects',
                                         'CCI_Soil_Moisture_Phase_2',
                                         '07_data',
                                         'ESA_CCI_SM_v04.4',
                                         '073_images_to_ts',
                                         'active'),
                     'lin': os.path.join(root_path.r,
                                         'Projects',
                                         'CCI_Soil_Moisture_Phase_2',
                                         '07_data',
                                         'ESA_CCI_SM_v04.4',
                                         '073_images_to_ts',
                                         'active'),
                 }),
                ('__test',
                 {
                     'win': os.path.join(root_path.test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v044', 'active'),
                     'lin': os.path.join(root_path.test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v044', 'active')
                 } if root_path.test_root is not None else {'win' : None, 'lin' : None})
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
                                         'Projects',
                                         'CCI_Soil_Moisture_Phase_2',
                                         '07_data',
                                         'ESA_CCI_SM_v04.4',
                                         '073_images_to_ts',
                                         'passive'),
                     'lin': os.path.join(root_path.r,
                                         'Projects',
                                         'CCI_Soil_Moisture_Phase_2',
                                         '07_data',
                                         'ESA_CCI_SM_v04.4',
                                         '073_images_to_ts',
                                         'passive'),
                 }),
                ('__test',
                 {
                     'win': os.path.join(root_path.test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v044', 'passive'),
                     'lin': os.path.join(root_path.test_root, '00_testdata', 'read',
                                         'esa_cci_sm', 'v044', 'passive')
                 } if root_path.test_root is not None else {'win' : None, 'lin' : None})
            ]),
    }