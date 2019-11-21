# -*- coding: utf-8 -*-

import os
import sys
from collections import OrderedDict

class PathConfig(object):

    def __init__(self, dataset_name, path_config):
        """

        Parameters
        ----------
        dataset_name : str or tuple
            The name of the dataset that this config is valid for
        path_config : OrderedDict
            Dict that holds the path information
        """
        self.name = dataset_name
        self.config = path_config
        self.os = self._curr_os()

        self._assert_path_config()

    def _assert_path_config(self):
        if not isinstance(self.config, OrderedDict):
            raise IOError('Configuration must be an ordered Dictionary')
        for group, ospaths in self.config.items():
            if not isinstance(ospaths, dict):
                raise IOError('Path definitions must be passed as a dictionary')
            if not self.os in list(ospaths.keys()):
                raise IOError('OS {} is not defined in config'.format(self.os))

    @staticmethod
    def _curr_os():
        if 'win' in sys.platform:
            return 'win'
        else:
            return 'lin'

    def _load_path_group(self, name):
        group_config = self.config[name]
        group_config_os = group_config[self.os]
        return group_config_os

    def load_path(self, ignore_path_groups=None):
        if ignore_path_groups is None:
            ignore_path_groups = []
        for group, ospath in self.config.items():
            if group not in ignore_path_groups:
                path = self._load_path_group(group)
                if path is not None and os.path.exists(path):
                    print('OS: {}; PathGroup: {}; Dataset: {}'.format(
                        self.os, group, self.name))
                    return path

        raise ValueError('None of the paths in the configuration were found')

