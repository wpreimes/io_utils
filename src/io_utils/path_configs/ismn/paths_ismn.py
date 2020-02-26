# -*- coding: utf-8 -*-

from collections import OrderedDict
import os
import io_utils.root_path as root_path

path_settings = \
    {
    ('ISMN', 'v20191211'):
        # paths will be tried in this order
        OrderedDict([
            ('local',
                {
                    'win': os.path.join(root_path.d,
                                        'data-read',
                                        'ISMN',
                                        'global_20191211'),
                    'lin': os.path.join(root_path.dr,
                                          'USERS',
                                          'wpreimes',
                                          'ISMN',
                                          'global_20191211'),
                }),
            ('radar',
                {
                    'win': os.path.join(root_path.r,
                                        'Projects',
                                        'QA4SM',
                                        '07_data',
                                        'ISMN',
                                        'global_20191211'),
                    'lin': os.path.join(root_path.r,
                                        'Projects',
                                        'QA4SM',
                                        '07_data',
                                        'ISMN',
                                        'global_20191211'),
                }),
            ('__test',
                 {
                     'win': os.path.join(root_path.test_root, '00_testdata', 'read',
                                         'ismn', 'ISMN_TESTDATA_HAWAII'),
                     'lin': os.path.join(root_path.test_root, '00_testdata', 'read',
                                         'ismn', 'ISMN_TESTDATA_HAWAII'),
                 } if root_path.test_root is not None else {'win' : None, 'lin' : None}),
    ]),
    }
