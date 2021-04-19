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
        ('ESA_CCI_SM', 'v045', 'COMBINED', 'ADJUSTED', 'QCM', 'ERA5'):
            # paths will be tried in this order
            OrderedDict([
                ('local',
                    {
                        'win': os.path.join(root_path.d,
                                            'data-read',
                                            'CCI_45_D_TS',
                                            'ESA_CCI_SM_v045_COMBINED_ADJUSTED_QCM_ERA5'),
                        'lin': os.path.join(root_path.dr,
                                            'USERS',
                                            'wpreimes',
                                            'CCI_45_D_TS',
                                            'ESA_CCI_SM_v045_COMBINED_ADJUSTED_QCM_ERA5'),
                    }),
        ]),

    }