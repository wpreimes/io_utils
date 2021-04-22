# -*- coding: utf-8 -*-

from collections import OrderedDict
import os
import io_utils.root_path as root_path


if root_path.test_root is not None:
    test_data_path = os.path.join(root_path.test_root, '00_testdata', 'read', 'c3s', 'v201912')
else:
    test_data_path = None

path_settings = \
    {
        ('C3S', 'v201912', 'COMBINED', 'DAILY', 'TCDR'):
        # paths will be tried in this order, there is no limit to the potential pathes here
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'C3S',
                                         'v201912',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'combined-daily'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'C3S',
                                         'v201912',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'combined-daily')
                 }),
                ('radar',
                 {
                     'win': os.path.join(root_path.r,
                                         'Datapool',
                                         'C3S',
                                         '02_processed',
                                         'v201912',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'combined-daily'),
                     'lin': os.path.join(root_path.r,
                                         'Datapool',
                                         'C3S',
                                         '02_processed',
                                         'v201912',
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


        ('C3S', 'v201912', 'ACTIVE', 'DAILY', 'TCDR'):
        # paths will be tried in this order
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'C3S',
                                         'v201912',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'active-daily'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'C3S',
                                         'v201912',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'active-daily')
                 }),
                ('radar',
                 {
                     'win': os.path.join(root_path.r,
                                         'Datapool',
                                         'C3S',
                                         '02_processed',
                                         'v201912',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'active-daily'),
                     'lin': os.path.join(root_path.r,
                                         'Datapool',
                                         'C3S',
                                         '02_processed',
                                         'v201912',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'active-daily'),
                 }),
            ]),


        ('C3S', 'v201912', 'PASSIVE', 'DAILY', 'TCDR'):
        # paths will be tried in this order
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'C3S',
                                         'v201912',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'passive-daily'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'C3S',
                                         'v201912',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'passive-daily')
                 }),
                ('radar',
                 {
                     'win': os.path.join(root_path.r,
                                         'Datapool',
                                         'C3S',
                                         '02_processed',
                                         'v201912',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'passive-daily'),
                     'lin': os.path.join(root_path.r,
                                         'Datapool',
                                         'C3S',
                                         '02_processed',
                                         'v201912',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'passive-daily'),
                 }),
            ]),

        ('C3S', 'v201912', 'COMBINED', 'MONTHLY', 'TCDR'):
        # paths will be tried in this order, there is no limit to the potential pathes here
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'C3S',
                                         'v201912',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'combined-monthly'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'C3S',
                                         'v201912',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'combined-monthly')
                 }),
                ('radar',
                 {
                     'win': os.path.join(root_path.r,
                                         'Datapool',
                                         'C3S',
                                         '02_processed',
                                         'v201912',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'combined-monthly'),
                     'lin': os.path.join(root_path.r,
                                         'Datapool',
                                         'C3S',
                                         '02_processed',
                                         'v201912',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'combined-monthly'),
                 }),
            ]),
        ('C3S', 'v201912', 'ACTIVE', 'MONTHLY', 'TCDR'):
        # paths will be tried in this order, there is no limit to the potential pathes here
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'C3S',
                                         'v201912',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'active-monthly'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'C3S',
                                         'v201912',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'active-monthly')
                 }),
                ('radar',
                 {
                     'win': os.path.join(root_path.r,
                                         'Datapool',
                                         'C3S',
                                         '02_processed',
                                         'v201912',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'active-monthly'),
                     'lin': os.path.join(root_path.r,
                                         'Datapool',
                                         'C3S',
                                         '02_processed',
                                         'v201912',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'active-monthly'),
                 }),
            ]),
        ('C3S', 'v201912', 'PASSIVE', 'MONTHLY', 'TCDR'):
        # paths will be tried in this order, there is no limit to the potential pathes here
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'C3S',
                                         'v201912',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'passive-monthly'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'C3S',
                                         'v201912',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'passive-monthly')
                 }),
                ('radar',
                 {
                     'win': os.path.join(root_path.r,
                                         'Datapool',
                                         'C3S',
                                         '02_processed',
                                         'v201912',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'passive-monthly'),
                     'lin': os.path.join(root_path.r,
                                         'Datapool',
                                         'C3S',
                                         '02_processed',
                                         'v201912',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'passive-monthly'),
                 }),
            ]),
        ('C3S', 'v201912', 'COMBINED', 'DEKADAL', 'TCDR'):
        # paths will be tried in this order, there is no limit to the potential pathes here
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'C3S',
                                         'v201912',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'combined-dekadal'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'C3S',
                                         'v201912',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'combined-dekadal')
                 }),
                ('radar',
                 {
                     'win': os.path.join(root_path.r,
                                         'Datapool',
                                         'C3S',
                                         '02_processed',
                                         'v201912',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'combined-dekadal'),
                     'lin': os.path.join(root_path.r,
                                         'Datapool',
                                         'C3S',
                                         '02_processed',
                                         'v201912',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'combined-dekadal'),
                 }),
            ]),
        ('C3S', 'v201912', 'ACTIVE', 'DEKADAL', 'TCDR'):
        # paths will be tried in this order, there is no limit to the potential pathes here
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'C3S',
                                         'v201912',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'active-dekadal'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'C3S',
                                         'v201912',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'active-dekadal')
                 }),
                ('radar',
                 {
                     'win': os.path.join(root_path.r,
                                         'Datapool',
                                         'C3S',
                                         '02_processed',
                                         'v201912',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'active-dekadal'),
                     'lin': os.path.join(root_path.r,
                                         'Datapool',
                                         'C3S',
                                         '02_processed',
                                         'v201912',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'active-dekadal'),
                 }),
            ]),
        ('C3S', 'v201912', 'PASSIVE', 'DEKADAL', 'TCDR'):
        # paths will be tried in this order, there is no limit to the potential pathes here
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'C3S',
                                         'v201912',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'passive-dekadal'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'C3S',
                                         'v201912',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'passive-dekadal')
                 }),
                ('radar',
                 {
                     'win': os.path.join(root_path.r,
                                         'Datapool',
                                         'C3S',
                                         '02_processed',
                                         'v201912',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'passive-dekadal'),
                     'lin': os.path.join(root_path.r,
                                         'Datapool',
                                         'C3S',
                                         '02_processed',
                                         'v201912',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'passive-dekadal'),
                 }),
            ]),
    }
