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
import warnings

import numpy as np

_cci_lc_lut_orig_to_short =     \
     {0: 'Other',       # no_data
      10: 'Cropland',   # cropland_rainfed
      11: 'Cropland',   # cropland_rainfed_herbaceous_cover
      12: 'Cropland',   # cropland_rainfed_tree_or_shrub_cover
      20: 'Cropland',   # cropland_irrigated
      30: 'Cropland',   # mosaic_cropland
      40: 'TreeCover',  # mosaic_natural_vegetation
      50: 'TreeCover',  # tree_broadleaved_evergreen_closed_to_open
      60: 'TreeCover',  # tree_broadleaved_deciduous_closed_to_open
      61: 'TreeCover',  # tree_broadleaved_deciduous_closed
      62: 'TreeCover',  # tree_broadleaved_deciduous_open
      70: 'TreeCover',  # tree_needleleaved_evergreen_closed_to_open
      71: 'TreeCover',  # tree_needleleaved_evergreen_closed
      72: 'TreeCover',  # tree_needleleaved_evergreen_open
      80: 'TreeCover',  # tree_needleleaved_deciduous_closed_to_open
      81: 'TreeCover',  # tree_needleleaved_deciduous_closed
      82: 'TreeCover',  # tree_needleleaved_deciduous_open
      90: 'TreeCover',  # tree_mixed
      100: 'TreeCover', # mosaic_tree_and_shrub
      110: 'TreeCover', # mosaic_herbaceous
      120: 'Grassland', # shrubland
      121: 'Grassland', # shrubland_evergreen
      122: 'Grassland', # shrubland_deciduous
      130: 'Grassland', # grassland
      140: 'Other',     # lichens_and_mosses
      150: 'Other',     # sparse_vegetation
      152: 'Other',     # sparse_shrub
      153: 'Other',     # sparse_herbaceous
      160: 'TreeCover', # tree_cover_flooded_fresh_or_brakish_water
      170: 'TreeCover', # tree_cover_flooded_saline_water
      180: 'Grassland', # shrub_or_herbaceous_cover_flooded
      190: 'UrbanAreas',# urban
      200: 'Other',     # bare_areas
      201: 'Other',     # bare_areas_consolidated
      202: 'Other',     # bare_areas_unconsolidated
      210: 'Other',     # water
      220: 'Other',     # snow_and_ice
      }

_ismn_sensor_types = {
    'CS616-1': 'TDR',
    'CS616-2': 'TDR',
    'CS616': 'TDR',
    'SMP1': 'Resistance', #smp is probably restistance
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
    'Hydraprobe-II-Sdi-12-S': 'Capacitance',
    'Hydraprobe-II-Sdi-12-W': 'Capacitance',
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
    'TDR-100': 'TDR',
    'AquaCheck': 'Capacitance',  # Capacitance/FRD
    'Buriable-Waveguide': 'TDR',
    'GS1-Port-2': 'Capacitance',  # Capacitance/FRD
    'GS1-Port-1': 'Capacitance',
    'GS1-Port-3': 'Capacitance',
    'HYDRA': 'Capacitance',
    'TEROS10': 'Capacitance',   # Capacitance/FRD
    'TEROS12': 'Capacitance',   # Capacitance/FRD
    'TRIME-EZ': 'TDR',
    'Flower-Power': 'Flower-Power',
}


def lookup(names, lut, ignore_missing=False):
    """
    Search in LUT (both directions).

    Parameters
    ----------
    name : str or list
        One or more classes names that are being looked up
    lut: dict
        Lookup table (works in both directions)
    ignore_missing: bool, optional
        Values that are not in the LUT (or if values from the left and right
        are mixed) a warning is raised for the cases.
        If this is False, then an Error is raised instead.

    Returns
    -------
    lu_name : str or list
        The looked up input
    """

    if isinstance(names, str) or not isinstance(names, Iterable):
        names = [names]

    short_to_orig = {}
    for orig, short in lut.items():
        if short not in short_to_orig.keys():
            short_to_orig[short] = [orig]
        else:
            short_to_orig[short].append(orig)

    if all([n in lut.keys() for n in names]):
        lu_names = [lut[n] for n in names]
    elif all([n in short_to_orig.keys() for n in names]):
        lu_names = [short_to_orig[n] for n in names]
        lu_names = list(itertools.chain.from_iterable(lu_names))
    else:
        if ignore_missing:
            n_from_right = np.count_nonzero(np.array([n in short_to_orig.keys() for n in names]))
            n_from_left = np.count_nonzero(np.array([n in lut.keys() for n in names]))
            if n_from_left >= n_from_right:
                pass
            else:
                lut = short_to_orig
            looked_up = []
            for n in names:
                try:
                    looked_up.append(lut[n])
                except KeyError:
                    warnings.warn(f"Could not find `{n}` in lookup table.")
                    looked_up.append(np.nan)
            return looked_up
        else:
            raise ValueError(
                "Some input value is not in the list of classes or "
                "classes names are mixed. You can ignore these cases by setting"
                " `handle_missing='warn'")

    return np.array(lu_names)

def lookup_lc(names, lut=_cci_lc_lut_orig_to_short, ignore_missing=False):
    """
    Generalise Land Cover classes to a smaller number of classes.

    Parameters
    ----------
    names: int or str or list
        Landcover class(es) to be looked up.
    lut: dict
        Lookup table to use
    ignore_missing: bool, optional
        Values that are not in the LUT (or if values from the left and right
        are mixed) a warning is raised for the cases (otherwise an Error
         is raised).

    Returns
    -------
    values: np.array
        Generalised landcover class(es)
    """
    names = np.atleast_1d(names)
    return lookup(names, lut, ignore_missing=ignore_missing)

def lookup_ismn_sensor(names, lut=_ismn_sensor_types, remove_postfix=True,
                       ignore_missing=True):
    """
    Generalise ISMN sensor type classes to a smaller number of classes.

    Parameters
    ----------
    names: str or list
        Landcover class(es) to be looked up.
    lut: dict
        Lookup table to use
    remove_postfix: bool, optional
        Remove (-A, -B etc.) postfix from sensor type that is often in the data
    ignore_missing: bool, optional
        Values that are not in the LUT (or if values from the left and right
        are mixed) a warning is raised for the cases (otherwise an Error
         is raised).

    Returns
    -------
    values: np.array
        Generalised sensor type(s)
    """
    names = np.atleast_1d(names)
    if remove_postfix:
        names = np.array([x[:-2] if
        x.endswith(('-A', '-B', '-C', '-D', '-E', '-F')) else x for x in names])
    return lookup(names, lut, ignore_missing=ignore_missing)

