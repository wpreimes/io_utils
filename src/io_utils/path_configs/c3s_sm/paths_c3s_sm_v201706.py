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
import io_utils.root_path as root_path

if root_path.test_root is not None:
    test_data_path = os.path.join(root_path.test_root, '00_testdata', 'read', 'c3s', 'v201706')
else:
    test_data_path = None

path_settings = \
    {
        ('C3S', 'v201706', 'COMBINED', 'DAILY', 'TCDR'):
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
                ('__test',
                 {
                     'win': os.path.join(test_data_path, 'tcdr', 'combined'),
                     'lin': os.path.join(test_data_path, 'tcdr', 'combined')
                 } if root_path.test_root is not None else {'win' : None, 'lin' : None}),
            ]),

        ('C3S', 'v201706', 'COMBINED', 'DAILY', 'ICDR'):
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
                ('__test',
                 {
                     'win': os.path.join(test_data_path, 'icdr', 'combined'),
                     'lin': os.path.join(test_data_path, 'icdr', 'combined')
                 } if root_path.test_root is not None else {'win' : None, 'lin' : None}),
            ]),

        ('C3S', 'v201706', 'ACTIVE', 'DAILY', 'TCDR'):
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
                ('__test',
                 {
                     'win': os.path.join(test_data_path, 'tcdr', 'active'),
                     'lin': os.path.join(test_data_path, 'tcdr', 'active')
                 } if root_path.test_root is not None else {'win' : None, 'lin' : None}),
            ]),

        ('C3S', 'v201706', 'ACTIVE', 'DAILY', 'ICDR'):
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
                ('__test',
                 {
                     'win': os.path.join(test_data_path, 'icdr', 'active'),
                     'lin': os.path.join(test_data_path, 'icdr', 'active')
                 } if root_path.test_root is not None else {'win' : None, 'lin' : None}),
            ]),


        ('C3S', 'v201706', 'PASSIVE', 'DAILY', 'TCDR'):
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
                ('__test',
                 {
                     'win': os.path.join(test_data_path, 'tcdr', 'passive'),
                     'lin': os.path.join(test_data_path, 'tcdr', 'passive')
                 } if root_path.test_root is not None else {'win' : None, 'lin' : None}),
            ]),

        ('C3S', 'v201706', 'PASSIVE', 'DAILY', 'ICDR'):
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
                ('__test',
                 {
                     'win': os.path.join(test_data_path, 'icdr', 'passive'),
                     'lin': os.path.join(test_data_path, 'icdr', 'passive')
                 } if root_path.test_root is not None else {'win' : None, 'lin' : None}),
            ]),
    }
