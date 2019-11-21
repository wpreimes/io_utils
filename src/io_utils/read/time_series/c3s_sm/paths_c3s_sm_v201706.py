# -*- coding: utf-8 -*-

"""
Module description
"""
# TODO:
#   (+) 
#---------
# NOTES:
#   -

from collections import OrderedDict
import os
from rsroot import root_path

path_settings = \
    {
        ('C3S', 'v201706', 'COMBINED', 'TCDR'):
        # paths will be tried in this order, there is no limit to the potential pathes here
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'C3S',
                                         'v201706',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'combined-daily'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'C3S',
                                         'v201706',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'combined-daily')
                 }),
                ('radar',
                 {
                     'win': os.path.join(root_path.r,
                                         'Datapool_processed',
                                         'C3S',
                                         'v201706',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'combined-daily'),
                     'lin': os.path.join(root_path.r,
                                         'Datapool_processed',
                                         'C3S',
                                         'v201706',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'combined-daily'),
                 }),
            ]),

        ('C3S', 'v201706', 'COMBINED', 'ICDR'):
        # paths will be tried in this order
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'C3S',
                                         'v201706',
                                         'ICDR',
                                         '063_images_to_ts',
                                         'combined-daily'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'C3S',
                                         'v201706',
                                         'ICDR',
                                         '063_images_to_ts',
                                         'combined-daily')
                 }),
                ('radar',
                 {
                     'win': os.path.join(root_path.r,
                                         'Datapool_processed',
                                         'C3S',
                                         'v201706',
                                         'ICDR',
                                         '063_images_to_ts',
                                         'combined-daily'),
                     'lin': os.path.join(root_path.r,
                                         'Datapool_processed',
                                         'C3S',
                                         'v201706',
                                         'ICDR',
                                         '063_images_to_ts',
                                         'combined-daily'),
                 }),
            ]),

        ('C3S', 'v201706', 'ACTIVE', 'TCDR'):
        # paths will be tried in this order
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'C3S',
                                         'v201706',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'active-daily'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'C3S',
                                         'v201706',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'active-daily')
                 }),
                ('radar',
                 {
                     'win': os.path.join(root_path.r,
                                         'Datapool_processed',
                                         'C3S',
                                         'v201706',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'active-daily'),
                     'lin': os.path.join(root_path.r,
                                         'Datapool_processed',
                                         'C3S',
                                         'v201706',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'active-daily'),
                 }),
            ]),

        ('C3S', 'v201706', 'ACTIVE', 'ICDR'):
        # paths will be tried in this order
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'C3S',
                                         'v201706',
                                         'ICDR',
                                         '063_images_to_ts',
                                         'active-daily'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'C3S',
                                         'v201706',
                                         'ICDR',
                                         '063_images_to_ts',
                                         'active-daily')
                 }),
                ('radar',
                 {
                     'win': os.path.join(root_path.r,
                                         'Datapool_processed',
                                         'C3S',
                                         'v201706',
                                         'ICDR',
                                         '063_images_to_ts',
                                         'combined-daily'),
                     'lin': os.path.join(root_path.r,
                                         'Datapool_processed',
                                         'C3S',
                                         'v201706',
                                         'ICDR',
                                         '063_images_to_ts',
                                         'combined-daily'),
                 }),
            ]),

        ('C3S', 'v201706', 'PASSIVE', 'TCDR'):
        # paths will be tried in this order
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'C3S',
                                         'v201706',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'passive-daily'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'C3S',
                                         'v201706',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'passive-daily')
                 }),
                ('radar',
                 {
                     'win': os.path.join(root_path.r,
                                         'Datapool_processed',
                                         'C3S',
                                         'v201706',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'passive-daily'),
                     'lin': os.path.join(root_path.r,
                                         'Datapool_processed',
                                         'C3S',
                                         'v201706',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'passive-daily'),
                 }),
            ]),

        ('C3S', 'v201706', 'PASSIVE', 'ICDR'):
        # paths will be tried in this order
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'C3S',
                                         'v201706',
                                         'ICDR',
                                         '063_images_to_ts',
                                         'passive-daily'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'C3S',
                                         'v201706',
                                         'ICDR',
                                         '063_images_to_ts',
                                         'passive-daily')
                 }),
                ('radar',
                 {
                     'win': os.path.join(root_path.r,
                                         'Datapool_processed',
                                         'C3S',
                                         'v201706',
                                         'ICDR',
                                         '063_images_to_ts',
                                         'passive-daily'),
                     'lin': os.path.join(root_path.r,
                                         'Datapool_processed',
                                         'C3S',
                                         'v201706',
                                         'ICDR',
                                         '063_images_to_ts',
                                         'passive-daily'),
                 }),
            ]),
    }
