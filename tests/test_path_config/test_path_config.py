# -*- coding: utf-8 -*-

from io_utils.read.path_config import PathConfig
from io_utils.path_configs.gldas.paths_gldas21 import path_settings


def test_path_config():
    dataset = ('GLDAS21', 'core')
    conf = PathConfig(dataset, path_settings[dataset])
    assert conf.os in ['win', 'lin']

    path = conf.load_path()