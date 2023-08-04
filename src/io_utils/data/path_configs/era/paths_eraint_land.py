# -*- coding: utf-8 -*-

"""
Module description
"""
# TODO:
#   (+) 
#---------
# NOTES:
#   -

from collections import OrderedDict
import os

import io_utils.root_path as root_path


path_settings = \
    {
        ('ERAINT-Land', 'GBG4', 'core'):
        # paths will be tried in this order
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'ERALand_gbg4',
                                         'netcdf'),
                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'ERALand_gbg4',
                                         'netcdf'),
                 }),
                ('climers',
                 {
                     'win': os.path.join(root_path.m,
                                         'Datapool',
                                         'ECMWF_reanalysis',
                                         '02_processed',
                                         'ERALAND',
                                         'datasets',
                                         'netcdf_gbg4'),
                     'lin': os.path.join(root_path.m,
                                         'Datapool',
                                         'ECMWF_reanalysis',
                                         '02_processed',
                                         'ERALAND',
                                         'datasets',
                                         'netcdf_gbg4'),
                 }),
            ]),
    }
