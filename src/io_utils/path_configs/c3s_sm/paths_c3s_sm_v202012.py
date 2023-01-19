# -*- coding: utf-8 -*-

from collections import OrderedDict
import os
import io_utils.root_path as root_path


if root_path.test_root is not None:
    test_data_path = os.path.join(root_path.test_root, '00_testdata', 'read',
                                  'c3s', 'v202012')
else:
    test_data_path = None

path_settings = \
    {
        ('C3S', 'v202012', 'COMBINED', 'DAILY', 'TCDR'):
        # paths will be tried in this order, there is no limit to the potential pathes here
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'C3S',
                                         'v202012',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'combined-daily'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'C3S',
                                         'v202012',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'combined-daily')
                 }),
                ('climers',
                 {
                     'win': os.path.join(root_path.m,
                                         'Projects',
                                         'C3S_312b',
                                         '07_data',
                                         'v202012_TCDR',
                                         '063_images_to_ts',
                                         'combined-daily'),
                     'lin': os.path.join(root_path.m,
                                         'Projects',
                                         'C3S_312b',
                                         '07_data',
                                         'v202012_TCDR',
                                         '063_images_to_ts',
                                         'combined-daily'),
                 }),
                ('__test',
                 {
                     'win': os.path.join(test_data_path, 'tcdr', 'combined'),
                     'lin': os.path.join(test_data_path, 'tcdr', 'combined')
                 } if root_path.test_root is not None else {'win' : None, 'lin' : None}),

            ]),


        ('C3S', 'v202012', 'ACTIVE', 'DAILY', 'TCDR'):
        # paths will be tried in this order
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'C3S',
                                         'v202012',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'active-daily'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'C3S',
                                         'v202012',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'active-daily')
                 }),
                ('climers',
                 {
                     'win': os.path.join(root_path.m,
                                         'Projects',
                                         'C3S_312b',
                                         '07_data',
                                         'v202012_TCDR',
                                         '063_images_to_ts',
                                         'active-daily'),
                     'lin': os.path.join(root_path.m,
                                         'Projects',
                                         'C3S_312b',
                                         '07_data',
                                         'v202012_TCDR',
                                         '063_images_to_ts',
                                         'active-daily'),
                 }),
            ]),


        ('C3S', 'v202012', 'PASSIVE', 'DAILY', 'TCDR'):
        # paths will be tried in this order
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'C3S',
                                         'v202012',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'passive-daily'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'C3S',
                                         'v202012',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'passive-daily')
                 }),
                ('climers',
                 {
                     'win': os.path.join(root_path.m,
                                         'Projects',
                                         'C3S_312b',
                                         '07_data',
                                         'v202012_TCDR',
                                         '063_images_to_ts',
                                         'passive-daily'),
                     'lin': os.path.join(root_path.m,
                                         'Projects',
                                         'C3S_312b',
                                         '07_data',
                                         'v202012_TCDR',
                                         '063_images_to_ts',
                                         'passive-daily'),
                 }),
            ]),

        ('C3S', 'v202012', 'COMBINED', 'MONTHLY', 'TCDR'):
        # paths will be tried in this order, there is no limit to the potential pathes here
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'C3S',
                                         'v202012',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'combined-monthly'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'C3S',
                                         'v202012',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'combined-monthly')
                 }),
                ('climers',
                 {
                     'win': os.path.join(root_path.m,
                                         'Projects',
                                         'C3S_312b',
                                         '07_data',
                                         'v202012_TCDR',
                                         '063_images_to_ts',
                                         'combined-monthly'),
                     'lin': os.path.join(root_path.m,
                                         'Projects',
                                         'C3S_312b',
                                         '07_data',
                                         'v202012_TCDR',
                                         '063_images_to_ts',
                                         'combined-monthly'),
                 }),
            ]),
        ('C3S', 'v202012', 'ACTIVE', 'MONTHLY', 'TCDR'):
        # paths will be tried in this order, there is no limit to the potential pathes here
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'C3S',
                                         'v202012',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'active-monthly'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'C3S',
                                         'v202012',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'active-monthly')
                 }),
                ('climers',
                 {
                     'win': os.path.join(root_path.m,
                                         'Projects',
                                         'C3S_312b',
                                         '07_data',
                                         'v202012_TCDR',
                                         '063_images_to_ts',
                                         'active-monthly'),
                     'lin': os.path.join(root_path.m,
                                         'Projects',
                                         'C3S_312b',
                                         '07_data',
                                         'v202012_TCDR',
                                         '063_images_to_ts',
                                         'active-monthly'),
                 }),
            ]),
        ('C3S', 'v202012', 'PASSIVE', 'MONTHLY', 'TCDR'):
        # paths will be tried in this order, there is no limit to the potential pathes here
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'C3S',
                                         'v202012',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'passive-monthly'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'C3S',
                                         'v202012',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'passive-monthly')
                 }),
                ('climers',
                 {
                     'win': os.path.join(root_path.m,
                                         'Projects',
                                         'C3S_312b',
                                         '07_data',
                                         'v202012_TCDR',
                                         '063_images_to_ts',
                                         'passive-monthly'),
                     'lin': os.path.join(root_path.m,
                                         'Projects',
                                         'C3S_312b',
                                         '07_data',
                                         'v202012_TCDR',
                                         '063_images_to_ts',
                                         'passive-monthly'),
                 }),
            ]),
        ('C3S', 'v202012', 'COMBINED', 'DEKADAL', 'TCDR'):
        # paths will be tried in this order, there is no limit to the potential pathes here
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'C3S',
                                         'v202012',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'combined-dekadal'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'C3S',
                                         'v202012',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'combined-dekadal')
                 }),
                ('climers',
                 {
                     'win': os.path.join(root_path.m,
                                         'Projects',
                                         'C3S_312b',
                                         '07_data',
                                         'v202012_TCDR',
                                         '063_images_to_ts',
                                         'combined-dekadal'),
                     'lin': os.path.join(root_path.m,
                                         'Projects',
                                         'C3S_312b',
                                         '07_data',
                                         'v202012_TCDR',
                                         '063_images_to_ts',
                                         'combined-dekadal'),
                 }),
            ]),
        ('C3S', 'v202012', 'ACTIVE', 'DEKADAL', 'TCDR'):
        # paths will be tried in this order, there is no limit to the potential pathes here
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'C3S',
                                         'v202012',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'active-dekadal'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'C3S',
                                         'v202012',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'active-dekadal')
                 }),
                ('climers',
                 {
                     'win': os.path.join(root_path.m,
                                         'Projects',
                                         'C3S_312b',
                                         '07_data',
                                         'v202012_TCDR',
                                         '063_images_to_ts',
                                         'active-dekadal'),
                     'lin': os.path.join(root_path.m,
                                         'Projects',
                                         'C3S_312b',
                                         '07_data',
                                         'v202012_TCDR',
                                         '063_images_to_ts',
                                         'active-dekadal'),
                 }),
            ]),
        ('C3S', 'v202012', 'PASSIVE', 'DEKADAL', 'TCDR'):
        # paths will be tried in this order, there is no limit to the potential pathes here
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'C3S',
                                         'v202012',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'passive-dekadal'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'C3S',
                                         'v202012',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'passive-dekadal')
                 }),
                ('climers',
                 {
                     'win': os.path.join(root_path.m,
                                         'Projects',
                                         'C3S_312b',
                                         '07_data',
                                         'v202012_TCDR',
                                         '063_images_to_ts',
                                         'passive-dekadal'),
                     'lin': os.path.join(root_path.m,
                                         'Projects',
                                         'C3S_312b',
                                         '07_data',
                                         'v202012_TCDR',
                                         '063_images_to_ts',
                                         'passive-dekadal'),
                 }),
            ]),
##############################################################################

        ('C3S', 'v202012', 'COMBINED', 'DAILY', 'TCDR'):
        # paths will be tried in this order, there is no limit to the potential pathes here
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'C3S',
                                         'v202012',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'combined-daily'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'C3S',
                                         'v202012',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'combined-daily')
                 }),
                ('climers',
                 {
                     'win': os.path.join(root_path.m,
                                         'Projects',
                                         'C3S_312b',
                                         '07_data',
                                         'v202012_TCDR',
                                         '063_images_to_ts',
                                         'combined-daily'),
                     'lin': os.path.join(root_path.m,
                                         'Projects',
                                         'C3S_312b',
                                         '07_data',
                                         'v202012_TCDR',
                                         '063_images_to_ts',
                                         'combined-daily'),
                 }),
                ('__test',
                 {
                     'win': os.path.join(test_data_path, 'tcdr', 'combined'),
                     'lin': os.path.join(test_data_path, 'tcdr', 'combined')
                 } if root_path.test_root is not None else {'win' : None, 'lin' : None}),

            ]),


        ('C3S', 'v202012', 'ACTIVE', 'DAILY', 'TCDR'):
        # paths will be tried in this order
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'C3S',
                                         'v202012',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'active-daily'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'C3S',
                                         'v202012',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'active-daily')
                 }),
                ('climers',
                 {
                     'win': os.path.join(root_path.m,
                                         'Projects',
                                         'C3S_312b',
                                         '07_data',
                                         'v202012_TCDR',
                                         '063_images_to_ts',
                                         'active-daily'),
                     'lin': os.path.join(root_path.m,
                                         'Projects',
                                         'C3S_312b',
                                         '07_data',
                                         'v202012_TCDR',
                                         '063_images_to_ts',
                                         'active-daily'),
                 }),
            ]),


        ('C3S', 'v202012', 'PASSIVE', 'DAILY', 'TCDR'):
        # paths will be tried in this order
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'C3S',
                                         'v202012',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'passive-daily'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'C3S',
                                         'v202012',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'passive-daily')
                 }),
                ('climers',
                 {
                     'win': os.path.join(root_path.m,
                                         'Projects',
                                         'C3S_312b',
                                         '07_data',
                                         'v202012_TCDR',
                                         '063_images_to_ts',
                                         'passive-daily'),
                     'lin': os.path.join(root_path.m,
                                         'Projects',
                                         'C3S_312b',
                                         '07_data',
                                         'v202012_TCDR',
                                         '063_images_to_ts',
                                         'passive-daily'),
                 }),
            ]),

        ('C3S', 'v202012', 'COMBINED', 'MONTHLY', 'TCDR'):
        # paths will be tried in this order, there is no limit to the potential pathes here
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'C3S',
                                         'v202012',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'combined-monthly'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'C3S',
                                         'v202012',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'combined-monthly')
                 }),
                ('climers',
                 {
                     'win': os.path.join(root_path.m,
                                         'Projects',
                                         'C3S_312b',
                                         '07_data',
                                         'v202012_TCDR',
                                         '063_images_to_ts',
                                         'combined-monthly'),
                     'lin': os.path.join(root_path.m,
                                         'Projects',
                                         'C3S_312b',
                                         '07_data',
                                         'v202012_TCDR',
                                         '063_images_to_ts',
                                         'combined-monthly'),
                 }),
            ]),
        ('C3S', 'v202012', 'ACTIVE', 'MONTHLY', 'TCDR'):
        # paths will be tried in this order, there is no limit to the potential pathes here
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'C3S',
                                         'v202012',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'active-monthly'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'C3S',
                                         'v202012',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'active-monthly')
                 }),
                ('climers',
                 {
                     'win': os.path.join(root_path.m,
                                         'Projects',
                                         'C3S_312b',
                                         '07_data',
                                         'v202012_TCDR',
                                         '063_images_to_ts',
                                         'active-monthly'),
                     'lin': os.path.join(root_path.m,
                                         'Projects',
                                         'C3S_312b',
                                         '07_data',
                                         'v202012_TCDR',
                                         '063_images_to_ts',
                                         'active-monthly'),
                 }),
            ]),
        ('C3S', 'v202012', 'PASSIVE', 'MONTHLY', 'TCDR'):
        # paths will be tried in this order, there is no limit to the potential pathes here
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'C3S',
                                         'v202012',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'passive-monthly'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'C3S',
                                         'v202012',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'passive-monthly')
                 }),
                ('climers',
                 {
                     'win': os.path.join(root_path.m,
                                         'Projects',
                                         'C3S_312b',
                                         '07_data',
                                         'v202012_TCDR',
                                         '063_images_to_ts',
                                         'passive-monthly'),
                     'lin': os.path.join(root_path.m,
                                         'Projects',
                                         'C3S_312b',
                                         '07_data',
                                         'v202012_TCDR',
                                         '063_images_to_ts',
                                         'passive-monthly'),
                 }),
            ]),
        ('C3S', 'v202012', 'COMBINED', 'DEKADAL', 'TCDR'):
        # paths will be tried in this order, there is no limit to the potential pathes here
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'C3S',
                                         'v202012',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'combined-dekadal'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'C3S',
                                         'v202012',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'combined-dekadal')
                 }),
                ('climers',
                 {
                     'win': os.path.join(root_path.m,
                                         'Projects',
                                         'C3S_312b',
                                         '07_data',
                                         'v202012_TCDR',
                                         '063_images_to_ts',
                                         'combined-dekadal'),
                     'lin': os.path.join(root_path.m,
                                         'Projects',
                                         'C3S_312b',
                                         '07_data',
                                         'v202012_TCDR',
                                         '063_images_to_ts',
                                         'combined-dekadal'),
                 }),
            ]),
        ('C3S', 'v202012', 'ACTIVE', 'DEKADAL', 'TCDR'):
        # paths will be tried in this order, there is no limit to the potential pathes here
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'C3S',
                                         'v202012',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'active-dekadal'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'C3S',
                                         'v202012',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'active-dekadal')
                 }),
                ('climers',
                 {
                     'win': os.path.join(root_path.m,
                                         'Projects',
                                         'C3S_312b',
                                         '07_data',
                                         'v202012_TCDR',
                                         '063_images_to_ts',
                                         'active-dekadal'),
                     'lin': os.path.join(root_path.m,
                                         'Projects',
                                         'C3S_312b',
                                         '07_data',
                                         'v202012_TCDR',
                                         '063_images_to_ts',
                                         'active-dekadal'),
                 }),
            ]),
        ('C3S', 'v202012', 'PASSIVE', 'DEKADAL', 'TCDR'):
        # paths will be tried in this order, there is no limit to the potential pathes here
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'C3S',
                                         'v202012',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'passive-dekadal'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'C3S',
                                         'v202012',
                                         'TCDR',
                                         '063_images_to_ts',
                                         'passive-dekadal')
                 }),
                ('climers',
                 {
                     'win': os.path.join(root_path.m,
                                         'Projects',
                                         'C3S_312b',
                                         '07_data',
                                         'v202012_TCDR',
                                         '063_images_to_ts',
                                         'passive-dekadal'),
                     'lin': os.path.join(root_path.m,
                                         'Projects',
                                         'C3S_312b',
                                         '07_data',
                                         'v202012_TCDR',
                                         '063_images_to_ts',
                                         'passive-dekadal'),
                 }),
            ]),
    }
