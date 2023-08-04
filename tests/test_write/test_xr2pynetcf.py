from tempfile import TemporaryDirectory
from smecv_grid.grid import SMECV_Grid_v052
import numpy as np
import xarray as xr
import pandas as pd
from io_utils.data.write.xr2pynetcf import datacube2orthomulti
from pynetcf.time_series import GriddedNcOrthoMultiTs
import os

def test_datacube_to_timeseries():
    globgrid = SMECV_Grid_v052(None)
    landgrid = SMECV_Grid_v052('land')
    shp = (720, 1440)
    mask = np.full(np.prod(shp), True)
    mask[landgrid.activegpis] = False
    mask = np.flipud(mask.reshape(shp))

    time = pd.date_range('2019-02-01', '2019-02-03', freq='D')
    gpis = np.flipud(np.arange(0, np.prod(shp)).reshape(*shp).astype(np.int32))
    var1 = np.stack([gpis + i for i in range(len(time))], axis=0).astype(
        np.float32)
    cells = np.flipud(
        np.repeat(np.arange(36 * 72).reshape(72, 36).transpose(), 20,
                  axis=1).repeat(20, axis=0)).astype(np.int16)
    gpis = np.flipud(np.arange(0, np.prod(shp)).reshape(*shp).astype(np.int32))

    res_stat = xr.Dataset(
        data_vars={
            'var1': (['time', 'lat', 'lon'], var1),
            'gpi': (['lat', 'lon'], gpis),
            'cell': (['lat', 'lon'], cells),
            'ts_mask': (['lat', 'lon'], mask.astype(bool)),
        },
        coords={
            'lon': np.sort(np.unique(globgrid.activearrlon)),
            'lat': np.flipud(np.sort(np.unique(globgrid.activearrlat))),
            'time': time
        },
        attrs=dict(description="Test"),
    )
    res_stat['var1'].attrs = {'name': 'test'}

    with TemporaryDirectory() as outdir:
        datacube2orthomulti(
            res_stat, outdir, n_proc=1,
            time_from='2019-02-02',
            cells=[1322, 1323, 1324, 1358, 1359, 1360]
        )
        assert len(os.listdir(outdir)) == 6
        ds = GriddedNcOrthoMultiTs(outdir, grid=landgrid)
        ts_land = ds.read(5, 48)
        assert not ts_land.empty
        ds.close()
