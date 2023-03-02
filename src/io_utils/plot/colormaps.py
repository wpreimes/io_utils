# -*- coding: utf-8 -*-

"""
Collection of colormaps used within plots for cci and c3s products.
"""

import numpy as np
from matplotlib import colors

cm_sm = colors.LinearSegmentedColormap.from_list('BrownBlue',
    np.array([[134, 80, 16],
            [164, 117, 13],
            [219, 190, 24],
            [250, 249, 156],
            [144, 202, 240],
            [4, 145, 251],
            [8, 83, 211],
            [13, 37, 161]]) / 255.)

cm_sm_anom_c3s = colors.LinearSegmentedColormap.from_list('BrownBlue',
    np.array([[231, 78, 19],
             [255, 255, 255],
             [0, 50, 107]]) / 255.)

cm_sm_anom_c3s_r = colors.LinearSegmentedColormap.from_list('BrownBlue',
    np.array([[0, 50, 107],
           [255, 255, 255],
           [231, 78, 19]]) / 255.)

cm_red_yellow_blue = colors.LinearSegmentedColormap.from_list('RdYlGn',
    np.array([[209, 56, 76],
             [255, 239, 161],
             [50, 133, 187]]) / 255.)

cm_reds = colors.LinearSegmentedColormap.from_list('Reds',
    np.array([[255, 255, 255],
              [255, 239, 161],
              [255, 51, 51]]) / 255.)

def cm_sm_div_esotc(N=256, set_over_under=True):
    cmap =  colors.LinearSegmentedColormap.from_list(
        'EsotcSmAnom',
        np.array([
            [129, 74, 8],
            [178, 117,36],
            [211, 172, 99],
            [236, 216, 167],
            [244, 238, 221],
            [229, 238, 243],
            [183, 215, 232],
            [119, 179, 212],
            [58, 135, 189],
            [27, 91, 157],
            ]) / 255.,
        N=N
    )
    if set_over_under:
        cmap.set_under([104/255,60/255,6/255])
        cmap.set_over([14/ 255, 67/ 255, 123/ 255])
    return cmap
