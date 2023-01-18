# -*- coding: utf-8 -*-

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
        ('SCATSAR', 'SWI', 'Drypan', 'Anoms'):
            # paths will be tried in this order
            OrderedDict([
                ('local',
                    {
                        'win': os.path.join(root_path.d,
                                            'data-read',
                                            'SCATSAR',
                                            '02_processed',
                                            'SCATSAR_SWI_anomalies'),
                        'lin': os.path.join(root_path.dr,
                                            'USERS',
                                            'wpreimes',
                                            'SCATSAR',
                                            '02_processed',
                                            'SCATSAR_SWI_anomalies'),
                    }),
                ('climers',
                    {
                        'win': os.path.join(root_path.m,
                                            'Projects',
                                            'DryPan',
                                            '07_data',
                                            'SCATSAR_SWI_anomalies'),
                        'lin': os.path.join(root_path.m,
                                            'Projects',
                                            'DryPan',
                                            '07_data',
                                            'SCATSAR_SWI_anomalies'),
                    }),
            ]),

        ('SCATSAR', 'SWI', 'Drypan', 'Abs'):
        # paths will be tried in this order
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'SCATSAR',
                                         '02_processed',
                                         'DryPan',
                                         'SCATSAR_reprojected'),
                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                         'wpreimes',
                                         'SCATSAR',
                                         '02_processed',
                                         'DryPan',
                                         'SCATSAR_reprojected'),
                 }),
                ('climers',
                 {
                     'win': os.path.join(root_path.m,
                                         'Projects',
                                         'DryPan',
                                         '07_data',
                                         'SCATSAR_reprojected'),
                     'lin': os.path.join(root_path.m,
                                         'Projects',
                                         'DryPan',
                                         '07_data',
                                         'SCATSAR_reprojected'),
                 }),
            ]),
    }
