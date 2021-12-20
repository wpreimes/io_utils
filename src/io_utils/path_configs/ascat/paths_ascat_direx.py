# -*- coding: utf-8 -*-

from collections import OrderedDict
import os
import getpass
import io_utils.root_path as root_path

path_settings = \
    {
        ('ASCAT', 'DIREX', 'v2', 'Senegal'):
        # paths will be tried in this order, there is no limit to the potential pathes here
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'ASCAT_DIREX',
                                         'v2'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         getpass.getuser(),
                                         'ASCAT_DIREX',
                                         'v2'),
                 }),
                ('radar',
                 {
                     'win': os.path.join(root_path.r,
                                         'Projects',
                                         'SMART-DRI',
                                         '07_data',
                                         'Senegal_ASCAT_DIREX_SWI_500m_v2.0',
                                         'preprocessed',
                                         '05_time_series'),
                     'lin': os.path.join(root_path.r,
                                         'Projects',
                                         'SMART-DRI',
                                         '07_data',
                                         'Senegal_ASCAT_DIREX_SWI_500m_v2.0',
                                         'preprocessed',
                                         '05_time_series'),
                 }),
            ]),
}