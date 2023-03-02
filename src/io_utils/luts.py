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
from collections.abc import Iterable

import numpy as np

_cci_lc_lut_orig_to_short =     \
     {0: 'Other',
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

_ismn_sensor_types = {
    'CS616-1': 'TDR',
    'CS616-2': 'TDR',
    'CS616': 'TDR',
    'SMP1': 'Resitance', #smp is probably restistance
    'Water-Matric-Potential-Sensor-229L': 'Hygrometric',
    'Water-Matric-Potential-Sensor-229L-W': 'Hygrometric',
    'GS-3': 'Capacitance',
    'CS615': 'TDR',
    'Cosmic-ray-Probe': 'Cosmic ray',
    'EC-TM': 'Capacitance',
    '5TM': 'Capacitance',
    'EC-TM-1': 'Capacitance',
    'EC-TM-2': 'Capacitance',
    'ThetaProbe-ML2X': 'Capacitance',
    '5TE': 'Capacitance',
    'CS655': 'TDR',
    'Decagon-5TE': 'Capacitance',
    'TDR-Soil-Moisture-Equipment-Corp.-TRASE-BE': 'TDR',
    'FM100': 'Droplet spectrometer',
    'SPADE-Time-Domain-Transmissivity': 'TDT',
    'Hydraprobe-II': 'Capacitance',
    'CS650': 'TDR',
    'ECH20-EC-TM': 'Capacitance',
    'WaterScout-SM100': 'Capacitance',
    'TRASE-16': 'TDR',
    'Stevens-Hydra-Probe': 'Capacitance',
    'Hydraprobe-II-Sdi-12': 'Capacitance',
    'Hydraprobe-Analog-(2.5-Volt)': 'Capacitance',
    'Hydraprobe-Analog-(5.0-Volt)': 'Capacitance',
    'Hydraprobe-Digital-Sdi-12-(2.5-Volt)': 'Capacitance',
    'Hydraprobe-Digital-Sdi-12-Thermistor-(linear)': 'Capacitance',
    'n.s.': 'not specified',
    'ThetaProbe-ML3': 'Capacitance',
    'EC5': 'Capacitance',
    'D-LOG-mpts': 'TDR',
    'PR2---Profile-Probe': 'Capacitance',
    'IMKO-TDR-1': 'TDR',
    'IMKO-TDR-2': 'TDR',
    'EC-ET-2': 'Capacitance',
    'EC5-I': 'Capacitance',
    'EC-ET': 'Capacitance',
    'EC5-III': 'Capacitance',
    'EC5-II': 'Capacitance',
    'EC5-IV': 'Capacitance',
    'Stevens-Hydraprobe-II-Sdi-12': 'Capacitance',
    'Hydraprobe-Analog-(2.5-Volt)---area-weighted-average': 'Capacitance',
    'Hydraprobe-Analog-(2.5-Volt)---average': 'Capacitance',
    'EnviroSCAN': 'Capacitance',
    'EnviroSMART': 'Capacitance',
    'IMKO-TDR': 'TDR',
    'GPS': 'GPS*',
    'Hydraprobe-Analog-(CR800)':'Capacitance',
    'Hydraprobe-T1000A':'Capacitance',
}



def lookup(names, orig_to_short=_cci_lc_lut_orig_to_short):
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

def lookup_lc(names, orig_to_merged=_cci_lc_lut_orig_to_short):
    """
    Generalise Land Cover classes to a smaller number of classes.

    Parameters
    ----------
    names: int or str or list
        Landcover class(es) to be looked up.
    orig_to_merged: dict
        Lookup table to use

    Returns
    -------
    values: np.array
        Generalised landcover class(es)
    """
    names = np.atleast_1d(names)
    return lookup(names, orig_to_merged)

def lookup_ismn(names, orig_to_merged=_ismn_sensor_types, remove_postfix=True):
    """
    Generalise ISMN sensor type classes to a smaller number of classes.

    Parameters
    ----------
    names: str or list
        Landcover class(es) to be looked up.
    orig_to_merged: dict
        Lookup table to use
    remove_postfix: bool, optional
        Remove (-A, -B etc.) postfix from sensor type that is often in the data

    Returns
    -------
    values: np.array
        Generalised landcover class(es)
    """
    names = np.atleast_1d(names)
    if remove_postfix:
        names = np.array([x[:-2] if
        x.endswith(('-A', '-B', '-C', '-D', '-E', '-F')) else x for x in names])
    return lookup(names, orig_to_merged)
