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
        ('ESA_CCI_SM', 'v0603_tmi', 'COMBINED'):
        # paths will be tried in this order
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'CCI_v06.0.3_tmi',
                                         '063_images_to_ts',
                                         'combined'),
                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'CCI_v06.0.3_tmi',
                                         '063_images_to_ts',
                                         'combined'),
                 }),
                ('radar',
                 {
                     'win': os.path.join(r'\\project10',
                                         'data-read',
                                         'USERS',
                                         'wpreimes',
                                         'CCI_v06.0.3_tmi',
                                         '063_images_to_ts',
                                         'combined'),
                     'lin': None,
                 }),
            ]),
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
                ('radar',
                 {
                     'win': os.path.join(root_path.r,
                                         'Projects',
                                         'CCIplus_Soil_Moisture',
                                         '07_data',
                                         'ESA_CCI_SM_v06.1',
                                         '063_images_to_ts',
                                         'combined'),
                     'lin': os.path.join(root_path.r,
                                         'Projects',
                                         'CCIplus_Soil_Moisture',
                                         '07_data',
                                         'ESA_CCI_SM_v06.1',
                                         '063_images_to_ts',
                                         'combined'),
                 }),
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
                ('radar',
                 {
                     'win': os.path.join(root_path.r,
                                         'Projects',
                                         'CCIplus_Soil_Moisture',
                                         '07_data',
                                         'ESA_CCI_SM_v06.1',
                                         '063_images_to_ts',
                                         'active'),
                     'lin': os.path.join(root_path.r,
                                         'Projects',
                                         'CCIplus_Soil_Moisture',
                                         '07_data',
                                         'ESA_CCI_SM_v06.1',
                                         '063_images_to_ts',
                                         'active'),
                 }),
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
                ('radar',
                 {
                     'win': os.path.join(root_path.r,
                                         'Projects',
                                         'CCIplus_Soil_Moisture',
                                         '07_data',
                                         'ESA_CCI_SM_v06.1',
                                         '063_images_to_ts',
                                         'passive'),
                     'lin': os.path.join(root_path.r,
                                         'Projects',
                                         'CCIplus_Soil_Moisture',
                                         '07_data',
                                         'ESA_CCI_SM_v06.1',
                                         '063_images_to_ts',
                                         'passive'),
                 }),
            ]),
    }