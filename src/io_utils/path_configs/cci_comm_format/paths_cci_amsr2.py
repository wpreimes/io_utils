# -*- coding: utf-8 -*-

from collections import OrderedDict
import os
import io_utils.root_path as root_path
import getpass

path_settings = \
    {
        ('CCIDs', 'v052', 'AMSR2', 'DES'):
        # paths will be tried in this order, there is no limit to the potential pathes here
            OrderedDict([
                ('local',
                 {
                     'win': os.path.join(root_path.d,
                                         'data-read',
                                         'CCIDs',
                                         'ESA_CCI_SM_v05.2',
                                         '011_resampledTemporal',
                                         'amsr2'),
                     'lin': os.path.join(root_path.dr,
                                         'USERS',
                                          getpass.getuser(),
                                         'CCIDs',
                                         'ESA_CCI_SM_v05.2',
                                         '011_resampledTemporal',
                                         'amsr2'),
                 }),
                ('climers',
                 {
                     'win': os.path.join(root_path.m,
                                         'Archive_Projects',
                                         'CCI_Soil_Moisture',
                                         '07_data',
                                         'ESA_CCI_SM_v05.2',
                                         '011_resampledTemporal',
                                         'amsr2'),
                     'lin': os.path.join(root_path.m,
                                         'Archive_Projects',
                                         'CCI_Soil_Moisture',
                                         '07_data',
                                         'ESA_CCI_SM_v05.2',
                                         '011_resampledTemporal',
                                         'amsr2'),
                 }),
]),
}
