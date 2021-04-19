# -*- coding: utf-8 -*-

"""
Paths for different subversions / paramter combinations of MERRA2 Time Series.
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
        ('MERRA2', 'core'):
            # paths will be tried in this order
            OrderedDict([
                ('local',
                    {
                        'win': os.path.join(root_path.d,
                                            'data-read',
                                            'MERRA2_D_TS',
                                            'M2T1NXLND.5.12.4_6hourly'),
                        'lin': os.path.join(root_path.dr,
                                            'USERS',
                                            'wpreimes',
                                            'MERRA2_D_TS',
                                            'M2T1NXLND.5.12.4_6hourly'),
                    }),
                ('radar',
                    {
                        'win': os.path.join(root_path.r,
                                            'Datapool',
                                            'MERRA2',
                                            '02_processed',
                                            'datasets',
                                            'M2T1NXLND.5.12.4_6hourly'),
                        'lin': os.path.join(root_path.r,
                                            'Datapool',
                                            'MERRA2',
                                            '02_processed',
                                            'datasets',
                                            'M2T1NXLND.5.12.4_6hourly'),
                    }),
                ('__test',
                    {
                        'win': os.path.join(root_path.test_root, '00_testdata', 'read',
                                            'merra2', 'core'),
                        'lin': os.path.join(root_path.test_root, '00_testdata', 'read',
                                            'merra2', 'core'),
                    } if root_path.test_root is not None else {'win' : None, 'lin' : None}),
            ]),
    }