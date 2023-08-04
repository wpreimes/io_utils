# -*- coding: utf-8 -*-

from collections import OrderedDict
import os
import getpass
import io_utils.root_path as root_path

path_settings = \
    {
        ('HSAF_ASCAT', 'SMDAS2', 'H14'):
        # paths will be tried in this order, there is no limit to the potential pathes here
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'HSAF_SWI_SMDAS2',
                                         '03_reshuffled_timeseries'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         getpass.getuser(),
                                         'HSAF_SWI_SMDAS2',
                                         '03_reshuffled_timeseries'),
                 }),
                ('radar',
                 {
                     'win': os.path.join(root_path.r,
                                         'Projects',
                                         'SMART-DRI',
                                         '07_Data',
                                         'SMDAS2_H14',
                                         '03_reshuffled_timeseries'),
                     'lin': os.path.join(root_path.r,
                                         'Projects',
                                         'SMART-DRI',
                                         '07_Data',
                                         'SMDAS2_H14',
                                         '03_reshuffled_timeseries'),
                 }),
            ]),
}