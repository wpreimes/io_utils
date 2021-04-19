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
        ('CSAR', 'CGLS', 'SWI', '1km', 'V1.0', 'geotiff'):
            # paths will be tried in this order
            OrderedDict([
                ('local',
                    {
                        'win': os.path.join(root_path.d,
                                            'data-read',
                                            'CSAR',
                                            '02_processed',
                                            'CGLS',
                                            'SWI1km',
                                            'V1.0',
                                            'geotiff'),
                        'lin': os.path.join(root_path.dr,
                                            'USERS',
                                             getpass.getuser(),
                                            'CGLS',
                                            '02_processed',
                                            'SWI1km',
                                            'V1.0',
                                            'geotiff')
                    }),
                ('radar',
                    {
                        'win': os.path.join(root_path.r,
                                            'Datapool',
                                            'CGLS',
                                            '01_raw',
                                            'SWI1km',
                                            'V1.0',
                                            'geotiff'),
                        'lin': os.path.join(root_path.r,
                                            'Datapool',
                                            'CGLS',
                                            '01_raw',
                                            'SWI1km',
                                            'V1.0',
                                            'geotiff'),
                    }),
            ]),
    }