# -*- coding: utf-8 -*-

from io_utils.plot.plot_maps import cp_map, cp_scatter_map
import numpy as np
import pandas as pd
import tempfile
import os
import io_utils.root_path as root_path
from netCDF4 import Dataset
from smecv_grid.grid import SMECV_Grid_v052
from io_utils.plot.colormaps import cm_sm
import cartopy.crs as ccrs
import shutil
from tempfile import TemporaryDirectory

def test_scatter_map():
    with TemporaryDirectory() as out_dir:
        lons = np.linspace(-160, 160, 160)
        lats = np.linspace(90, -90, 160)
        values = np.random.rand(160)

        f, imax, im = cp_scatter_map(lons, lats, values)

        filename = 'plot_scatter.png'

        f.savefig(os.path.join(out_dir, filename))
        print('Stored plot in {}')
        assert os.path.isfile(os.path.join(out_dir, filename))

def test_area_multiindex():
    with TemporaryDirectory() as out_dir:
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
    with TemporaryDirectory() as out_dir:
        gpis = np.arange(346859, 374200)

        df = pd.DataFrame(index=gpis)
        df['data'] = np.random.rand(df.index.size)
        f, imax, im = cp_map(df, 'data', resxy=(0.25,0.25))
        filename = 'plot_area_gpi.png'
        f.savefig(os.path.join(out_dir, filename))

        assert os.path.isfile(os.path.join(out_dir, filename))

def test_pretty_plot():

    image = os.path.join(root_path.test_root, '00_testdata', 'plot',
        'ESACCI-SOILMOISTURE-L3S-SSMV-COMBINED-20100701000000-fv04.5.nc')
    ds = Dataset(image)
    dat = ds.variables['sm'][:]
    dat = dat.filled(np.nan).flatten()
    _, resampled_lons, resampled_lats, _  = SMECV_Grid_v052(None).get_grid_points()

    index =pd.MultiIndex.from_arrays(np.array([resampled_lats, resampled_lons]),
                                     names=['lats', 'lons'])
    df = pd.DataFrame(index=index, data={'sm': dat}).dropna()

    cb_kwargs = dict(cb_label='ESA CCI SM [$m^3/m^3$]', cb_labelsize=7,
                     cb_extend='both', cb_ext_label_min='DRY',
                     cb_ext_label_max='WET', cb_loc='right')

    f, imax, im = cp_map(df, 'sm', resxy=(0.25,0.25), cbrange=(0,50.), veg_mask=True,
                         cmap=cm_sm, projection=ccrs.Sinusoidal(),
                         title='Overloaded Plot with too much Information',
                         ocean=True, land='grey', gridspace=(60,20), states=True,
                         borders=True,  llc=(-179.9999, -90.), urc=(179.9999, 90),
                         scale_factor=100,
                         grid_label_loc='0111', coastline_size='110m',
                         cb_kwargs=cb_kwargs)

    out_dir = tempfile.mkdtemp()
    try:
        filename = 'pretty_plot.png'
        f.savefig(os.path.join(out_dir, 'pretty_plot.png'), dpi=200)
        assert os.path.isfile(os.path.join(out_dir, filename))
    finally:
        shutil.rmtree(out_dir)


if __name__ == '__main__':
    test_scatter_map()
    test_pretty_plot()
    test_area_multiindex()
    test_area_gpi()

