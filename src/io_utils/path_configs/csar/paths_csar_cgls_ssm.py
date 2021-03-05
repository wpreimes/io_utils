# -*- coding: utf-8 -*-

# TODO:
#   (+) 
#---------
# NOTES:
#   -

import os
from collections import OrderedDict
import io_utils.root_path as root_path
import getpass

path_settings = \
    {
        ('CSAR', 'CGLS', 'SSM', '1km', 'V1.1', 'tiff'):
            # paths will be tried in this order
            OrderedDict([
                ('local',
                    {
                        'win': os.path.join(root_path.d,
                                            'data-read',
                                            'CSAR',
                                            '02_processed',
                                            'CGLS',
                                            'SSM1km',
                                            'V1.1',
                                            'geotiff'),
                        'lin': os.path.join(root_path.dr,
                                            'USERS',
                                             getpass.getuser(),
                                            'CGLS',
                                            '02_processed',
                                            'SSM1km',
                                            'V1.1',
                                            'geotiff')
                    }),
                ('radar',
                    {
                        'win': os.path.join(root_path.r,
                                            'Datapool',
                                            'CGLS',
                                            '01_raw',
                                            'SSM1km',
                                            'V1.1',
                                            'geotiff'),
                        'lin': os.path.join(root_path.r,
                                            'Datapool',
                                            'CGLS',
                                            '01_raw',
                                            'SSM1km',
                                            'V1.1',
                                            'geotiff'),
                    }),
            ]),

    }