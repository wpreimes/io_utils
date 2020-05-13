# -*- coding: utf-8 -*-

import os
import sys
from collections import OrderedDict

class PathNotFoundError(ValueError):
    def __init__(self, *args):
        super(PathNotFoundError, self).__init__(*args)

class ConfigNotFoundError(ValueError):
    def __init__(self, *args):
        super(ConfigNotFoundError, self).__init__(*args)


class PathConfig(object):

    def __init__(self, dataset_name_or_path, path_config=None):
        """

        Parameters
        ----------
        dataset_name_or_path : tuple or str
            The name of the dataset that this config is valid for (tuple) or
            a single path to the data directly (string).
        path_config : OrderedDict
            Dict that holds the path information
        """
        if isinstance(dataset_name_or_path, str):
            print('No path config available, use path directly.')
            self.pathdirect = True
        else:
            if isinstance(dataset_name_or_path, list):
                dataset_name_or_path = tuple(dataset_name_or_path)
            self.pathdirect = False

        self.name_path = dataset_name_or_path
        self.config = path_config
        self.os = self._curr_os()

        if not self.pathdirect:
            self._assert_path_config()
        else:
            self._assert_path()

    def _assert_path(self):
        if not os.path.exists(self.name_path):
            raise IOError('Passed path does not exist', self.name_path)

    def _assert_path_config(self):
        if self.config is None:
            raise IOError('Configuratin for paths not set, either add it, '
                          'or pass a valid path')
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
        if name not in self.config.keys():
            raise IOError(name, 'Group not found in the current configuration.')
        group_config = self.config[name]
        group_config_os = group_config[self.os]
        return group_config_os

    def load_path(self, force_path_group=None, ignore_path_groups=('__test')):
        """
        Get a path from the path groups

        Parameters
        ----------
        force_path_group : str, optional (default: None)
            Use the path group of this name.
        ignore_path_groups : list, optional (default: '__test')
            Exclude these path groups from the search (if none are forced).

        Returns
        -------
        path : str
            Path where the data is stored, of the first valid path group (where
            the folder was found).

        """
        if self.pathdirect:
            return self.name_path

        if ignore_path_groups is None:
            ignore_path_groups = []

        if force_path_group is not None:
            group = force_path_group
            path = self._load_path_group(group)
            if path is not None and os.path.exists(path):
                print('OS: {}; PathGroup: {}; Dataset: {}; Path: {}'.format(
                    self.os, group, self.name_path, path))
            else:
                raise ConfigNotFoundError('No configuration found for group {}'.
                                        format(group))
            return path
        else:
            for group, ospath in self.config.items():
                if group not in ignore_path_groups:
                    path = self._load_path_group(group)
                    if path is not None and os.path.exists(path):
                        print('OS: {}; PathGroup: {}; Dataset: {}; Path: {}'.format(
                            self.os, group, self.name_path, path))
                        return path
            raise PathNotFoundError('None of the paths in the configuration were found')
