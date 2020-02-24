# -*- coding: utf-8 -*-

"""
Generally useful lookup tables.

"""
# TODO:
#   (+) 
#---------
# NOTES:
#   -

import itertools
from collections import Iterable

def ccilc_lut(names):
    """
    LUT between ESA CCI LC and combined LC classes and vice verse.

    Parameters
    ----------
    name : str or list
        One or more classes names that are being looked uo

    Returns
    -------
    lu_name : str or list
        The looked up input
    """
    if isinstance(names, str) or not isinstance(names, Iterable):
        names = [names]

    orig_to_short = {0: 'Other',
                    10: 'Cropland',
                    11: 'Cropland',
                    12: 'Cropland',
                    20: 'Cropland',
                    30: 'Cropland',
                    40: 'TreeCover',
                    50: 'TreeCover',
                    60: 'TreeCover',
                    61: 'TreeCover',
                    62: 'TreeCover',
                    70: 'TreeCover',
                    71: 'TreeCover',
                    72: 'TreeCover',
                    80: 'TreeCover',
                    81: 'TreeCover',
                    82: 'TreeCover',
                    90: 'TreeCover',
                    100: 'TreeCover',
                    110: 'TreeCover',
                    120: 'Grassland',
                    121: 'Grassland',
                    122: 'Grassland',
                    130: 'Grassland',
                    140: 'Other',
                    150: 'Other',
                    152: 'Other',
                    153: 'Other',
                    160: 'TreeCover',
                    170: 'TreeCover',
                    180: 'Grassland',
                    190: 'UrbanAreas',
                    200: 'Other',
                    201: 'Other',
                    202: 'Other',
                    210: 'Other',
                    220: 'Other'}

    short_to_orig = {}
    for orig, short in orig_to_short.items():
        if short not in short_to_orig.keys():
            short_to_orig[short] = [orig]
        else:
            short_to_orig[short].append(orig)

    if all([n in orig_to_short.keys() for n in names]):
        lu_names = [orig_to_short[n] for n in names]
    elif all([n in short_to_orig.keys() for n in names]):
        lu_names = [short_to_orig[n] for n in names]
        lu_names = list(itertools.chain.from_iterable(lu_names))
    else:
        raise ValueError('Some input value is not in the list of classes or classes names are mixed.')


    return lu_names