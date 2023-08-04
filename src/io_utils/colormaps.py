# -*- coding: utf-8 -*-

"""
Collection of colormaps used within plots for cci and c3s products.
"""

import numpy as np
from matplotlib import colors

def smecv_sm(N: int = 256, set_over_under: bool = True) \
        -> colors.LinearSegmentedColormap:
    """
    Default Colormap for soil moisture in CCI and C3S
    Brown-Yellow-Blue
    """
    steps = np.array([[134, 80, 16],
                      [164, 117, 13],
                      [219, 190, 24],
                      [250, 249, 156],
                      [144, 202, 240],
                      [4, 145, 251],
                      [8, 83, 211],
                      [13, 37, 161]]) / 255.
    cmap = colors.LinearSegmentedColormap.from_list('smecv_sm', steps, N=N)

    if set_over_under:
        cmap.set_under(np.array([112, 65, 12]) / 255)
        cmap.set_over(np.array([7, 25, 106]) / 255)

    return cmap

def smecv_nobs(N: int = 256, set_over_under: bool = True) \
        -> colors.LinearSegmentedColormap:
    """
    Colormap used for number of observations in CCI and C3S.
    Red-Yellow-Green-Blue
    """
    steps = np.array([[209, 56, 76],
                      [255, 239, 161],
                      [50, 133, 187]]) / 255.
    cmap = colors.LinearSegmentedColormap.from_list('smecv_nobs', steps, N=N)

    if set_over_under:
        cmap.set_under(np.array([172, 46, 62]) / 255.)
        cmap.set_over(np.array([45, 122, 170]) / 255)

    return cmap

def smecv_esotc_anom(N: int = 256, set_over_under: bool = True) \
        -> colors.LinearSegmentedColormap:
    """
    Colormap used to plotter soil moisture anomalies, in the C3S ESotC report.
    """
    cmap = colors.LinearSegmentedColormap.from_list(
        'smecv_esotc_anom',
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
        cmap.set_under(np.array([104,60,6]) / 255)
        cmap.set_over(np.array([14, 67, 123]) / 255)
    return cmap
