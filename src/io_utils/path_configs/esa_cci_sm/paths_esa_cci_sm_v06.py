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
        ('ESA_CCI_SM', 'v0603_tmi', 'COMBINED'):
        # paths will be tried in this order
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'CCI_v06.0.3_tmi',
                                         '063_images_to_ts',
                                         'combined'),
                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'CCI_v06.0.3_tmi',
                                         '063_images_to_ts',
                                         'combined'),
                 }),
                ('radar',
                 {
                     'win': os.path.join(r'\\project10',
                                         'data-read',
                                         'USERS',
                                         'wpreimes',
                                         'CCI_v06.0.3_tmi',
                                         '063_images_to_ts',
                                         'combined'),
                     'lin': None,
                 }),
            ]),

    }