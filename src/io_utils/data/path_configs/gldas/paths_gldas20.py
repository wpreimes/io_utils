# -*- coding: utf-8 -*-
from collections import OrderedDict
import os
import io_utils.root_path as root_path

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
                ('climers',
                    {
                        'win': os.path.join(root_path.m,
                                            'Datapool',
                                            'GLDAS',
                                            '02_processed',
                                            'GLDAS_NOAH025_3H.020',
                                            'datasets',
                                            'netcdf_reprocessed'),
                        'lin': os.path.join(root_path.m,
                                            'Datapool',
                                            'GLDAS',
                                            '02_processed',
                                            'GLDAS_NOAH025_3H.020',
                                            'datasets',
                                            'netcdf_reprocessed'),
                    }),
        ]),
    }
