# -*- coding: utf-8 -*-
from collections import OrderedDict
import os
from rsroot import root_path

from src.globals import get_test_root

path_settings = \
    {
        ('GLDAS20', 'core'):
            # paths will be tried in this order
            OrderedDict([
                ('local',
                    {
                        'win': os.path.join(root_path.d,
                                            'data-read',
                                            'GLDAS_v2',
                                            'netcdf'),
                        'lin': os.path.join(root_path.dr,
                                            'USERS',
                                            'wpreimes',
                                            'GLDAS_v2',
                                            'netcdf'),
                    }),
                ('radar',
                    {
                        'win': os.path.join(root_path.r,
                                            'Datapool_processed',
                                            'GLDAS',
                                            'GLDAS_NOAH025_3H.020',
                                            'datasets',
                                            'netcdf_reprocessed'),
                        'lin': os.path.join(root_path.r,
                                            'Datapool_processed',
                                            'GLDAS',
                                            'GLDAS_NOAH025_3H.020',
                                            'datasets',
                                            'netcdf_reprocessed'),
                    }),
        ]),
    }