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

