# -*- coding: utf-8 -*-

import os
from io_utils.yml.read import spaceify
import numpy as np
import sys
import io_utils.root_path as root_path

def test_read():
    yml_path = os.path.join(root_path.test_root, '00_testdata', 'yml', 'test_config.yml')
    SPACES = spaceify(yml_path)

    LEVEL1 = SPACES[0]
    A_LEVEL2 = SPACES[1]
    OTHER = SPACES[2]

    assert A_LEVEL2.NOTHING is None

    assert(LEVEL1.A_CLASS == np.ma.masked_array)
    assert(LEVEL1.A_FUNCTION == np.ma.unique)
    assert(LEVEL1.A_MODULE == np.ma)

    if 'win' in sys.platform:
        assert(LEVEL1.PATH == r'D:\data')
    else:
        assert(LEVEL1.PATH == '/data')

    assert(OTHER.TEST_1 == 'TEST1')
    assert(OTHER.TEST_2 == 2)
    assert(OTHER.TEST_DICT == {'one':1})
    assert(OTHER.TEST_LIST == [1,2,3])

if __name__ == '__main__':
    test_read()