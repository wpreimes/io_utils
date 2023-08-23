import tempfile
import unittest
import os
import xarray as xr
import io_utils.root_path as root_path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from io_utils.plot.map import MapPlotter


class TestMapPlotter(unittest.TestCase):
    def setUp(self) -> None:
        self.plotter = MapPlotter(llc=(-30, 35), urc=(40, 70))
        image = os.path.join(
            root_path.test_root, '00_testdata', 'plot',
            'ESACCI-SOILMOISTURE-L3S-SSMV-COMBINED-20100701000000-fv04.5.nc')
        ds = xr.open_dataset(image)
        self.df = ds[['sm', 'flag']].isel(time=0).to_dataframe().drop(
            columns='time')

    def test_all_in_one(self):
        np.random.seed(123)
        self.plotter.add_colormesh_layer(self.df['sm'].dropna(), add_cbar=True,
                                    cbar_kwargs=dict(cb_label='SM (m3/m3)',
                                                     cb_loc='left'))
        self.df['mask'] = self.df['flag'] == 0
        self.plotter.add_hatch_overlay(
            self.df['mask'].dropna().astype(bool), pattern='.', density=2, lw=2)

        idx = np.random.choice(self.df.index, 1000)
        df = pd.Series(index=pd.MultiIndex.from_tuples(idx), data=True)

        self.plotter.add_scatter_layer(
            df, marker='.', s=50, cmap=plt.get_cmap('Greens'),
            add_cbar=True, clim=(0, 1),
            cbar_kwargs=dict(cb_label='SM (m3/m3)',cb_loc='right'))

        self.plotter.add_basemap('white', ocean=True, states=True, borders=True,
                                linewidth_mult=3)

        idx = np.random.choice(df.index, 1000)
        df = pd.Series(index=pd.MultiIndex.from_tuples(idx), data=True)

        self.plotter.add_scatter_overlay(df, marker='+', s=20)

        self.plotter.add_gridlines('0110', (60, 20))

        self.plotter.ax.set_title('Test')

        with tempfile.TemporaryDirectory() as out_path:
            fname = os.path.join(out_path, 'test.png')
            self.plotter.fig.savefig(fname, dpi=300, bbox_inches='tight')
            assert os.path.isfile(fname)
