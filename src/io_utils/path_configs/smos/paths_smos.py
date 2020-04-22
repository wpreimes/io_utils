# -*- coding: utf-8 -*-

"""
Paths for different subversions / paramter combinations of SMOS Time Series.
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
        ('SMOS', 'IC', 'ASC'):
            # paths will be tried in this order
            OrderedDict([
                ('local',
                    {
                        'win': os.path.join(root_path.d,
                                            'data-read',
                                            'SMOS_IC_TS',
                                            'ASC'),
                        'lin': os.path.join(root_path.dr,
                                            'USERS',
                                            'wpreimes',
                                            'SMOS_IC_TS',
                                            'ASC'),
                    }),
                ('radar',
                    {
                        'win': os.path.join(root_path.r,
                                            'Datapool',
                                            'SMOS',
                                            '02_processed',
                                            'L3_SMOS_IC_Soil_Moisture',
                                            'timeseries',
                                            'ASC'),
                        'lin': os.path.join(root_path.r,
                                            'Datapool',
                                            'SMOS',
                                            '02_processed',
                                            'L3_SMOS_IC_Soil_Moisture',
                                            'timeseries',
                                            'ASC'),
                    }),
                ('__test',
                    {
                        'win': os.path.join(root_path.test_root, '00_testdata', 'read',
                                            'SMOS', 'smos_ic_asc'),
                        'lin': os.path.join(root_path.test_root, '00_testdata', 'read',
                                            'SMOS', 'smos_ic_asc'),
                    } if root_path.test_root is not None else {'win' : None, 'lin' : None}),
            ]),
        ('SMOS', 'IC', 'DES'):
        # paths will be tried in this order
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'SMOS_IC_TS',
                                         'DES'),
                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'SMOS_IC_TS',
                                         'DES'),
                 }),
                ('radar',
                 {
                     'win': os.path.join(root_path.r,
                                         'Datapool',
                                         'SMOS',
                                         '02_processed',
                                         'L3_SMOS_IC_Soil_Moisture',
                                         'timeseries',
                                         'DES'),
                     'lin': os.path.join(root_path.r,
                                         'Datapool',
                                         'SMOS',
                                         '02_processed',
                                         'L3_SMOS_IC_Soil_Moisture',
                                         'timeseries',
                                         'DES'),
                 }),
            ]),
    }