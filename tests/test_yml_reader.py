# -*- coding: utf-8 -*-

import os
from io_utils.yml.read import spaceify, read_settings
import numpy as np
import sys

this_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
yml_path = os.path.join(this_path, '00_testdata', 'yml', 'test_config.yml')

def test_read_yml():
    SPACES = spaceify(yml_path)

    LEVEL1 = SPACES[0]
    A_LEVEL2 = SPACES[1]
    OTHER = SPACES[2]

    assert A_LEVEL2.NOTHING is None
    assert A_LEVEL2.sublev['sublev_b'] == 'b'
    assert A_LEVEL2.sublev['sublev_a'] is None
    assert A_LEVEL2.sublev['sublev_c'] == LEVEL1.A_FUNCTION
    assert A_LEVEL2.sublev['sublev_d'] == {'d': 1}
    assert A_LEVEL2.sublev['deeper']['deeper']['deeper']['bottom'] is None
    assert A_LEVEL2.sublev['deeper']['deeper']['deeper']['bottom_list'] == [1,2,3]

    assert(LEVEL1.A_CLASS == np.ma.masked_array)
    assert(LEVEL1.A_FUNCTION == np.ma.unique)
    assert(LEVEL1.A_MODULE == np.ma)

    if 'win' in sys.platform:
        assert(LEVEL1.PATH == r'C:\Users')
        assert LEVEL1.OS_VAR == 'windows'
    else:
        assert LEVEL1.OS_VAR == 'linux'
        assert(LEVEL1.PATH == '/home')

    assert LEVEL1.relPATH == os.path.join('this', 'relpath')
    assert(OTHER.TEST_1 == 'TEST1')
    assert(OTHER.TEST_2 == 2)
    assert(OTHER.TEST_DICT == {'one':1})
    assert(OTHER.TEST_LIST == [1,2,3])


if __name__ == '__main__':
    test_read_yml()
