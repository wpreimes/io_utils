# -*- coding: utf-8 -*-

"""
Module description
"""
# TODO:
#   (+) 
#---------
# NOTES:
#   -


import os

def get_src_root():
    return os.path.dirname(os.path.abspath(__file__))

def get_test_root():
    proj_root = get_src_root()
    return os.path.join(proj_root, '..', 'tests')