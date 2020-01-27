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
from rsroot import root_path

from src.globals import get_test_root

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
                                            'Datapool_processed',
                                            'SMOS',
                                            'L3_SMOS_IC_Soil_Moisture',
                                            'timeseries',
                                            'ASC'),
                        'lin': os.path.join(root_path.r,
                                            'Datapool_processed',
                                            'SMOS',
                                            'L3_SMOS_IC_Soil_Moisture',
                                            'timeseries',
                                            'ASC'),
                    }),
                ('_test',
                    {
                        'win': os.path.join(get_test_root(), 'test_data', 'read',
                                            'SMOS', 'smos_ic_asc'),
                        'lin': os.path.join(get_test_root(), 'test_data', 'read',
                                            'SMOS', 'smos_ic_asc'),
                    }),
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
                                         'Datapool_processed',
                                         'SMOS',
                                         'L3_SMOS_IC_Soil_Moisture',
                                         'timeseries',
                                         'DES'),
                     'lin': os.path.join(root_path.r,
                                         'Datapool_processed',
                                         'SMOS',
                                         'L3_SMOS_IC_Soil_Moisture',
                                         'timeseries',
                                         'DES'),
                 }),
            ]),
    }