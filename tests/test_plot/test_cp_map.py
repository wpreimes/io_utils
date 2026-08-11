# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

from io_utils.plot.map import MapPlotter
import numpy as np
import pandas as pd
import tempfile
import os
import io_utils.root_path as root_path
from netCDF4 import Dataset
from smecv_grid.grid import SMECV_Grid_v052
from io_utils.colormaps import smecv_sm
import cartopy.crs as ccrs
import shutil
from tempfile import TemporaryDirectory
import xarray as xr

def test_scatter_map():
    with TemporaryDirectory() as out_dir:
        lons = np.linspace(-160, 160, 160)
        lats = np.linspace(90, -90, 160)
        values = np.random.rand(160)
        ds = pd.Series(
            index=pd.MultiIndex.from_arrays([lats, lons], names=['lat', 'lon']),
            data=values
        )
        plotter = MapPlotter()
        plotter.add_basemap()
        plotter.add_scatter_layer(ds)
        filename = 'plot_scatter.png'
        plotter.savefig(os.path.join(out_dir, filename))
        print('Stored plotter in {}')
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
        plotter = MapPlotter()
        plotter.add_basemap()
        plotter.add_colormesh_layer(df["data"])
        filename = 'plot_area_multiindex.png'
        plotter.savefig(os.path.join(out_dir, filename))
        print('Stored plotter in {}')
        assert os.path.isfile(os.path.join(out_dir, filename))

def test_pretty_plot():
    image = os.path.join(root_path.test_root, '00_testdata', 'plot',
        'ESACCI-SOILMOISTURE-L3S-SSMV-COMBINED-20100701000000-fv04.5.nc')
    ds = xr.open_dataset(image)
    df = ds[['sm']].isel(time=0).to_dataframe().drop(columns='time')

    grid = SMECV_Grid_v052('rainforest')
    index = pd.MultiIndex.from_arrays(
        np.array([grid.activearrlat, grid.activearrlon]),
        names=['lat', 'lon'])
    df['rainforest'] = np.nan
    df.loc[index, 'rainforest'] = 1

    cb_kwargs = dict(cb_label='ESA CCI SM [$m^3/m^3$]', cb_labelsize=7,
                     cb_extend='both', cb_ext_label_min='DRY',
                     cb_ext_label_max='WET', cb_loc='right')

    plotter = MapPlotter(projection=ccrs.Sinusoidal(),
                         llc=(-179.9999, -90.), urc=(179.9999, 90))
    plotter.add_basemap(ocean=True, borders=True, states=True)
    plotter.add_colormesh_layer(df['sm'].dropna(), cmap=smecv_sm(),
                                add_cbar=True, cbar_kwargs=cb_kwargs)
    plotter.add_colormesh_layer(df['rainforest'].dropna(),
                                cmap=plt.get_cmap("Greens"))
    plotter.add_gridlines()

    with tempfile.TemporaryDirectory() as out_dir:
        filename = 'pretty_plot.png'
        plotter.savefig(os.path.join(out_dir, 'pretty_plot.png'), dpi=200)
        assert os.path.isfile(os.path.join(out_dir, filename))


if __name__ == '__main__':
    test_pretty_plot()

    # test_scatter_map()
    # test_area_multiindex()
    # test_area_gpi()

