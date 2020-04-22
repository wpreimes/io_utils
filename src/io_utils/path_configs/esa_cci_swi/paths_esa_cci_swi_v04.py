# -*- coding: utf-8 -*-

"""
Module description
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
        ('ESA_CCI_SWI', 'v047'):
        # paths will be tried in this order
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'CCISWI_47_D_TS'),
                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'CCISWI_47_D_TS'),
                 }),
                ('radar',
                 {
                     'win': os.path.join(root_path.r,
                                         'Projects',
                                         'G3P',
                                         '07_data',
                                         'SWI_CCI_v04.7_contUSA_TS'),
                     'lin': os.path.join(root_path.r,
                                         'Projects',
                                         'G3P',
                                         '07_data',
                                         'SWI_CCI_v04.7_contUSA_TS'),
                 }),
            ]),
    }