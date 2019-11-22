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
from src.globals import get_test_root

test_data_root = os.path.join(get_test_root(), 'test_data', 'read', 'c3s', 'v201706')

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
                ('_test',
                 {
                     'win': os.path.join(test_data_root, 'tcdr', 'combined'),
                     'lin': os.path.join(test_data_root, 'tcdr', 'combined')
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
                ('_test',
                 {
                     'win': os.path.join(test_data_root, 'icdr', 'combined'),
                     'lin': os.path.join(test_data_root, 'icdr', 'combined')
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
                ('_test',
                 {
                     'win': os.path.join(test_data_root, 'tcdr', 'active'),
                     'lin': os.path.join(test_data_root, 'tcdr', 'active')
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
                ('_test',
                 {
                     'win': os.path.join(test_data_root, 'icdr', 'active'),
                     'lin': os.path.join(test_data_root, 'icdr', 'active')
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
                ('_test',
                 {
                     'win': os.path.join(test_data_root, 'tcdr', 'passive'),
                     'lin': os.path.join(test_data_root, 'tcdr', 'passive')
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
                ('_test',
                 {
                     'win': os.path.join(test_data_root, 'icdr', 'passive'),
                     'lin': os.path.join(test_data_root, 'icdr', 'passive')
                 }),
            ]),
    }
