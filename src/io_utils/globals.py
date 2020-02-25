# -*- coding: utf-8 -*-

import os

src_root = os.path.join(os.path.dirname(os.path.abspath(__file__)))

test_root = os.path.join(src_root, '..', '..', 'tests')
if not os.path.exists(test_root):
    test_root = None