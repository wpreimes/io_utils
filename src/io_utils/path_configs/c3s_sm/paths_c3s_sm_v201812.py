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
    test_data_path = os.path.join(root_path.test_root, '00_testdata', 'read', 'c3s', 'v201812')
else:
    test_data_path = None

path_settings = \
    {
        ('C3S', 'v201812', 'COMBINED', 'DAILY', 'TCDR'):
        # paths will be tried in this order, there is no limit to the potential pathes here
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'C3S',
                                         'v201812',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'combined-daily'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'C3S',
                                         'v201812',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'combined-daily')
                 }),
                ('climers',
                 {
                     'win': os.path.join(root_path.m,
                                         'Datapool',
                                         'C3S',
                                         '02_processed',
                                         'v201812',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'combined-daily'),
                     'lin': os.path.join(root_path.m,
                                         'Datapool',
                                         'C3S',
                                         '02_processed',
                                         'v201812',
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


        ('C3S', 'v201812', 'ACTIVE', 'DAILY', 'TCDR'):
        # paths will be tried in this order
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'C3S',
                                         'v201812',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'active-daily'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'C3S',
                                         'v201812',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'active-daily')
                 }),
                ('climers',
                 {
                     'win': os.path.join(root_path.m,
                                         'Datapool',
                                         'C3S',
                                         '02_processed',
                                         'v201812',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'active-daily'),
                     'lin': os.path.join(root_path.m,
                                         'Datapool',
                                         'C3S',
                                         '02_processed',
                                         'v201812',
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


        ('C3S', 'v201812', 'PASSIVE', 'DAILY', 'TCDR'):
        # paths will be tried in this order
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'C3S',
                                         'v201812',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'passive-daily'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'C3S',
                                         'v201812',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'passive-daily')
                 }),
                ('climers',
                 {
                     'win': os.path.join(root_path.m,
                                         'Datapool',
                                         'C3S',
                                         '02_processed',
                                         'v201812',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'passive-daily'),
                     'lin': os.path.join(root_path.m,
                                         'Datapool',
                                         'C3S',
                                         '02_processed',
                                         'v201812',
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
        ('C3S', 'v201812', 'COMBINED', 'MONTHLY', 'TCDR'):
        # paths will be tried in this order, there is no limit to the potential pathes here
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'C3S',
                                         'v201812',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'combined-monthly'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'C3S',
                                         'v201812',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'combined-monthly')
                 }),
                ('climers',
                 {
                     'win': os.path.join(root_path.m,
                                         'Datapool',
                                         'C3S',
                                         '02_processed',
                                         'v201812',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'combined-monthly'),
                     'lin': os.path.join(root_path.m,
                                         'Datapool',
                                         'C3S',
                                         '02_processed',
                                         'v201812',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'combined-monthly'),
                 }),
            ]),
        ('C3S', 'v201812', 'ACTIVE', 'MONTHLY', 'TCDR'):
        # paths will be tried in this order, there is no limit to the potential pathes here
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'C3S',
                                         'v201812',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'active-monthly'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'C3S',
                                         'v201812',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'active-monthly')
                 }),
                ('climers',
                 {
                     'win': os.path.join(root_path.m,
                                         'Datapool',
                                         'C3S',
                                         '02_processed',
                                         'v201812',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'active-monthly'),
                     'lin': os.path.join(root_path.m,
                                         'Datapool',
                                         'C3S',
                                         '02_processed',
                                         'v201812',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'active-monthly'),
                 }),
            ]),
        ('C3S', 'v201812', 'PASSIVE', 'MONTHLY', 'TCDR'):
        # paths will be tried in this order, there is no limit to the potential pathes here
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'C3S',
                                         'v201812',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'passive-monthly'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'C3S',
                                         'v201812',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'passive-monthly')
                 }),
                ('climers',
                 {
                     'win': os.path.join(root_path.m,
                                         'Datapool',
                                         'C3S',
                                         '02_processed',
                                         'v201812',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'passive-monthly'),
                     'lin': os.path.join(root_path.m,
                                         'Datapool',
                                         'C3S',
                                         '02_processed',
                                         'v201812',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'passive-monthly'),
                 }),
            ]),
        ('C3S', 'v201812', 'COMBINED', 'DEKADAL', 'TCDR'):
        # paths will be tried in this order, there is no limit to the potential pathes here
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'C3S',
                                         'v201812',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'combined-dekadal'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'C3S',
                                         'v201812',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'combined-dekadal')
                 }),
                ('climers',
                 {
                     'win': os.path.join(root_path.m,
                                         'Datapool',
                                         'C3S',
                                         '02_processed',
                                         'v201812',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'combined-dekadal'),
                     'lin': os.path.join(root_path.m,
                                         'Datapool',
                                         'C3S',
                                         '02_processed',
                                         'v201812',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'combined-dekadal'),
                 }),
            ]),
        ('C3S', 'v201812', 'ACTIVE', 'DEKADAL', 'TCDR'):
        # paths will be tried in this order, there is no limit to the potential pathes here
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'C3S',
                                         'v201812',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'active-dekadal'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'C3S',
                                         'v201812',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'active-dekadal')
                 }),
                ('climers',
                 {
                     'win': os.path.join(root_path.m,
                                         'Datapool',
                                         'C3S',
                                         '02_processed',
                                         'v201812',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'active-dekadal'),
                     'lin': os.path.join(root_path.m,
                                         'Datapool',
                                         'C3S',
                                         '02_processed',
                                         'v201812',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'active-dekadal'),
                 }),
            ]),

        ('C3S', 'v201812', 'PASSIVE', 'DEKADAL', 'TCDR'):
        # paths will be tried in this order, there is no limit to the potential pathes here
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'C3S',
                                         'v201812',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'passive-dekadal'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'C3S',
                                         'v201812',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'passive-dekadal')
                 }),
                ('climers',
                 {
                     'win': os.path.join(root_path.m,
                                         'Datapool',
                                         'C3S',
                                         '02_processed',
                                         'v201812',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'passive-dekadal'),
                     'lin': os.path.join(root_path.m,
                                         'Datapool',
                                         'C3S',
                                         '02_processed',
                                         'v201812',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'passive-dekadal'),
                 }),
            ]),

        ('C3S', 'v201812', 'COMBINED', 'DAILY', 'ICDR'):
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'C3S',
                                         'v201812',
                                         'ICDR',
                                         '064_images_to_ts',
                                         'combined-daily'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'C3S',
                                         'v201812',
                                         'ICDR',
                                         '064_images_to_ts',
                                         'combined-daily')
                 }),
                ('climers',
                 {
                     'win': os.path.join(root_path.m,
                                         'Datapool',
                                         'C3S',
                                         '02_processed',
                                         'v201812',
                                         'ICDR',
                                         '064_images_to_ts',
                                         'combined-daily'),
                     'lin': os.path.join(root_path.m,
                                         'Datapool',
                                         'C3S',
                                         '02_processed',
                                         'v201812',
                                         'TCDR',
                                         '064_images_to_ts',
                                         'combined-daily'),
                 }),
            ]),

        ('C3S', 'v201812', 'ACTIVE', 'DAILY', 'ICDR'):
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'C3S',
                                         'v201812',
                                         'ICDR',
                                         '064_images_to_ts',
                                         'active-daily'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'C3S',
                                         'v201812',
                                         'ICDR',
                                         '064_images_to_ts',
                                         'active-daily')
                 }),
                ('climers',
                 {
                     'win': os.path.join(root_path.m,
                                         'Datapool',
                                         'C3S',
                                         '02_processed',
                                         'v201812',
                                         'ICDR',
                                         '064_images_to_ts',
                                         'active-daily'),
                     'lin': os.path.join(root_path.m,
                                         'Datapool',
                                         'C3S',
                                         '02_processed',
                                         'v201812',
                                         'TCDR',
                                         '064_images_to_ts',
                                         'active-daily'),
                 }),
            ]),

        ('C3S', 'v201812', 'PASSIVE', 'DAILY', 'ICDR'):
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'C3S',
                                         'v201812',
                                         'ICDR',
                                         '064_images_to_ts',
                                         'passive-daily'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'C3S',
                                         'v201812',
                                         'ICDR',
                                         '064_images_to_ts',
                                         'passive-daily')
                 }),
                ('climers',
                 {
                     'win': os.path.join(root_path.m,
                                         'Datapool',
                                         'C3S',
                                         '02_processed',
                                         'v201812',
                                         'ICDR',
                                         '064_images_to_ts',
                                         'passive-daily'),
                     'lin': os.path.join(root_path.m,
                                         'Datapool',
                                         'C3S',
                                         '02_processed',
                                         'v201812',
                                         'TCDR',
                                         '064_images_to_ts',
                                         'passive-daily'),
                 }),
            ]),
    }
