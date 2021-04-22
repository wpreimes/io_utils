# -*- coding: utf-8 -*-

from io_utils.read.path_config import PathConfig
from io_utils.path_configs.gldas.paths_gldas21 import path_settings
import os

def test_path_config():
    dataset = ('GLDAS21', 'core')
    conf = PathConfig(dataset, path_settings[dataset])
    assert conf.os in ['win', 'lin']
    # this should fall back to testdata if not on GEO:
    path = conf.load_path(ignore_path_groups=None)
    assert os.path.exists(path)

if __name__ == '__main__':
    test_path_config()