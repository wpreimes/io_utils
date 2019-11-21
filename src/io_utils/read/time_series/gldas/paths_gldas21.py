# -*- coding: utf-8 -*-
from collections import OrderedDict
import os
from rsroot import root_path

path_settings = \
    {
        ('GLDAS21', 'core'):
            # paths will be tried in this order
            OrderedDict([
                ('local',
                    {
                        'win': os.path.join(root_path.d,
                                            'data-read',
                                            'GLDAS_v21',
                                            'netcdf'),
                        'lin': os.path.join(root_path.dr,
                                              'USERS',
                                              'wpreimes',
                                              'GLDAS_v21',
                                              'netcdf'),
                    }),
                ('radar',
                    {
                        'win': os.path.join(root_path.r,
                                            'Datapool_processed',
                                            'GLDAS',
                                            'GLDAS_NOAH025_3H.2.1',
                                            'datasets',
                                            'netcdf'),
                        'lin': os.path.join(root_path.r,
                                            'Datapool_processed',
                                            'GLDAS',
                                            'GLDAS_NOAH025_3H.2.1',
                                            'datasets',
                                            'netcdf'),
                    }),
                ('fallback',
                    {
                        'win': None,
                        'lin': None,
                    })
        ]),
    }
