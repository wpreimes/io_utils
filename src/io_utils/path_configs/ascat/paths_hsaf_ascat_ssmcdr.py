# -*- coding: utf-8 -*-

from collections import OrderedDict
import os
import getpass
import io_utils.root_path as root_path

path_settings = \
    {
        ('HSAF_ASCAT', 'SSM', 'H115+H116'):
        # paths will be tried in this order, there is no limit to the potential pathes here
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'HSAF_ASCAT_SSMCDR',
                                         'H115+H116r8'),

                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         getpass.getuser(),
                                         'HSAF_ASCAT_SSMCDR',
                                         'H115+H116r8'),
                 }),
                ('radar',
                 {
                     'win': os.path.join(root_path.r,
                                         'Projects',
                                         'H_SAF_CDOP3',
                                         '05_deliverables_products',
                                         'H116',
                                         'H115+H116r8'),
                     'lin': os.path.join(root_path.r,
                                         'Projects',
                                         'H_SAF_CDOP3',
                                         '05_deliverables_products',
                                         'H116',
                                         'H115+H116r8'),
                 }),
            ]),
}