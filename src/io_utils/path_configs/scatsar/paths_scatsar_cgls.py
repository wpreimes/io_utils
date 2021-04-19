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
        ('SCATSAR', 'CGLS', 'C0418', 'E7'):
            # paths will be tried in this order
            OrderedDict([
                ('local',
                    {
                        'win': os.path.join(root_path.d,
                                            'data-read',
                                            'SCATSAR',
                                            '02_processed',
                                            'CGLS',
                                            'C0418'),
                        'lin': os.path.join(root_path.dr,
                                            'USERS',
                                            'wpreimes',
                                            'SCATSAR',
                                            '02_processed',
                                            'CGLS',
                                            'C0418')
                    }),
                ('radar',
                    {
                        'win': os.path.join(root_path.r,
                                            'Datapool',
                                            'SCATSAR',
                                            '02_processed',
                                            'CGLS',
                                            'C0418'),
                        'lin': os.path.join(root_path.r,
                                            'Datapool',
                                            'SCATSAR',
                                            '02_processed',
                                            'CGLS',
                                            'C0418'),
                    }),
            ]),
    }