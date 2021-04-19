# -*- coding: utf-8 -*-
from collections import OrderedDict
import os
import io_utils.root_path as root_path


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
                                            'Datapool',
                                            'GLDAS',
                                            '02_processed',
                                            'GLDAS_NOAH025_3H.2.1',
                                            'datasets',
                                            'netcdf'),
                        'lin': os.path.join(root_path.r,
                                            'Datapool',
                                            'GLDAS',
                                            '02_processed',
                                            'GLDAS_NOAH025_3H.2.1',
                                            'datasets',
                                            'netcdf'),
                    }),
                ('__test',
                  {
                      'win': os.path.join(root_path.test_root, '00_testdata', 'read',
                                          'gldas', 'gldas21_ts'),
                      'lin': os.path.join(root_path.test_root, '00_testdata', 'read',
                                          'gldas', 'gldas21_ts'),
                  } if root_path.test_root is not None else {'win' : None, 'lin' : None})
        ]),
    }
