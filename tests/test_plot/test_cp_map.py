# -*- coding: utf-8 -*-

from io_utils.plot.plot_maps import cp_map
import numpy as np
import pandas as pd
import tempfile
import os
import matplotlib.pyplot as plt


def test_area_multiindex():
    out_dir = tempfile.mkdtemp()

    lons = np.linspace(-20, 20, 41)
    lats = np.linspace(20, -20, 41).transpose()

    lons, lats = np.meshgrid(lons, lats)

    # multiindex: lats, lons
    index =pd.MultiIndex.from_arrays(np.array([lats.flatten(), lons.flatten()]),
                                     names=['lats', 'lons'])
    df = pd.DataFrame(index=index)
    df['data'] = np.random.rand(df.index.size)
    f, imax, im = cp_map(df, 'data', resxy=(1,1), offset=(0,0))

    filename = 'plot_area_multiindex.png'
    f.savefig(os.path.join(out_dir, filename))
    print('Stored plot in {}')
    assert os.path.isfile(os.path.join(out_dir, filename))

def test_area_gpi():
    out_dir = tempfile.mkdtemp()

    gpis = np.arange(346859, 374200)

    df = pd.DataFrame(index=gpis)
    df['data'] = np.random.rand(df.index.size)
    f, imax, im = cp_map(df, 'data', resxy=(0.25,0.25))
    filename = 'plot_area_gpi.png'
    f.savefig(os.path.join(out_dir, filename))

    assert os.path.isfile(os.path.join(out_dir, filename))

if __name__ == '__main__':
    test_area_multiindex()
    test_area_gpi()

