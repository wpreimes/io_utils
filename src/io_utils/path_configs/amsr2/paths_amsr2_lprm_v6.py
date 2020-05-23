# -*- coding: utf-8 -*-


from collections import OrderedDict
import os
import getpass
import io_utils.root_path as root_path

path_settings = \
    {
        ('AMSR2', 'LPRM', 'v6', 'ASC'):
        # paths will be tried in this order, there is no limit to the potential pathes here
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'AMSR2',
                                         '02_processed',
                                         'AMSR2_S3_VEGC_LPRMv6',
                                         'timeseries',
                                         'v202001',
                                         'a'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         getpass.getuser(),
                                         'AMSR2',
                                         '02_processed',
                                         'AMSR2_S3_VEGC_LPRMv6',
                                         'timeseries',
                                         'v202001',
                                         'a'),
                 }),
                ('radar',
                 {
                     'win': os.path.join(root_path.r,
                                         'Datapool',
                                         'AMSR2',
                                         '02_processed',
                                         'AMSR2_S3_VEGC_LPRMv6',
                                         'timeseries',
                                         'v202001',
                                         'a'),
                     'lin': os.path.join(root_path.r,
                                         'Datapool',
                                         'AMSR2',
                                         '02_processed',
                                         'AMSR2_S3_VEGC_LPRMv6',
                                         'timeseries',
                                         'v202001',
                                         'a'),
                 }),
            ]),
        ('AMSR2', 'LPRM', 'v6', 'DESC'):
        # paths will be tried in this order, there is no limit to the potential pathes here
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'AMSR2',
                                         '02_processed',
                                         'AMSR2_S3_VEGC_LPRMv6',
                                         'timeseries',
                                         'v202001',
                                         'd'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         getpass.getuser(),
                                         'AMSR2',
                                         '02_processed',
                                         'AMSR2_S3_VEGC_LPRMv6',
                                         'timeseries',
                                         'v202001',
                                         'd'),
                 }),
                ('radar',
                 {
                     'win': os.path.join(root_path.r,
                                         'Datapool',
                                         'AMSR2',
                                         '02_processed',
                                         'AMSR2_S3_VEGC_LPRMv6',
                                         'timeseries',
                                         'v202001',
                                         'd'),
                     'lin': os.path.join(root_path.r,
                                         'Datapool',
                                         'AMSR2',
                                         '02_processed',
                                         'AMSR2_S3_VEGC_LPRMv6',
                                         'timeseries',
                                         'v202001',
                                         'd'),
                 }),
            ]),
    }
