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


path_settings = \
    {
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
                ('fallback',
                    {
                        'win': None,
                        'lin': None,
                    })
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
                ('fallback',
                 {
                     'win': None,
                     'lin': None,
                 })
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
                ('fallback',
                 {
                     'win': None,
                     'lin': None,
                 })
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
                ('fallback',
                 {
                     'win': None,
                     'lin': None,
                 })
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
                ('fallback',
                 {
                     'win': None,
                     'lin': None,
                 })
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
                ('fallback',
                 {
                     'win': None,
                     'lin': None,
                 })
            ]),
    }