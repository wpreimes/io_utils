from io_utils.parallel import apply_to_elements
import pandas as pd
from pynetcf.time_series import OrthoMultiTs
import xarray as xr
import numpy as np
from smecv_grid.grid import SMECV_Grid_v052
import os

# todo: store grid file upon conversion

def _store(dat: xr.Dataset, cell: int, out_path: str):
    sel = np.where(~dat['ts_mask'].values) if 'ts_mask' in dat.data_vars else ...
    gpis = dat['gpi'].values[sel]
    lats = dat['lat'].values[sel]
    lons = dat['lon'].values[sel]
    time = pd.to_datetime(dat['time'].values).to_pydatetime()

    data = {}
    for var in dat.data_vars.keys():
        if dat[var].ndim != 2:
            continue
        else:
            data[var] = np.transpose(dat[var].values[:, sel[0]])

    var_attrs = {var: dat[var].attrs for var in data.keys()}

    if not np.all([len(v) > 0 for k, v in data.items()]):
        return
    else:
        if os.path.isfile(os.path.join(out_path, f"{cell:04}.nc")):
            mode = 'a'
        else:
            mode = 'w'

        cell_writer = OrthoMultiTs(
            filename=os.path.join(out_path, f"{cell:04}.nc"),
            n_loc=len(gpis), mode=mode)

        cell_writer.write_ts_all_loc(gpis, data, time,
                                     lons=lons, lats=lats,
                                     attributes=var_attrs)
        cell_writer.close()


def datacube2orthomulti(ds, out_path, time_from=None, time_to=None,
                        cells=None, n_proc=1):
    """
    Convert a xarray Dataset to pynetcf GriddedOrthoMultiTs format.
    The Dataset must have 3 dimensions (lat, lon, time).
    The dataset is split up into chunks / cells and each one is written to
    a separate netcdf file.
    Rules:
        - there must be a 2d variable 'cell' (lon, lat image)
        - there must be a 2d varable 'gpi' (lon, lat image)
        - if there is a variable mask, only gpis where mask is False are stored
        - the dimensions must be lat, lon, time

    Parameters
    ----------
    ds: xr.DataSet
        The dataset to store as time series
    out_path: str
        Path where time series are stored.
    time_from: str, optional (default: None)
        To limit the time range of time series to store
    time_to: str, optional (default: None)
        To limit the time range of time series to store
    cells: list or np.ndarray, optional (default: None)
        If only certain cells should be stored they can be passed here.
    n_proc: int, optional (default: 1)
        Number of parallel processes
    """
    if (time_from is not None) or (time_to is not None):
        ds = ds.sel(time=slice(time_from, time_to))
    iter_kwargs = {'cell': [], 'dat': []}
    for cell, dat in ds.groupby('cell'):
        if (cells is not None) and (cell not in cells):
            continue
        else:
            iter_kwargs['dat'].append(dat.compute())
            iter_kwargs['cell'].append(cell)
    ds.close()
    del ds
    apply_to_elements(_store, ITER_KWARGS=iter_kwargs,
                      STATIC_KWARGS={'out_path': out_path},
                      n_proc=n_proc)

if __name__ == '__main__':
    globgrid = SMECV_Grid_v052(None)
    landgrid = SMECV_Grid_v052('land')
    mask = np.full((720*1440), True)
    mask[landgrid.activegpis] = False
    mask = np.flipud(mask.reshape((720, 1440)))

    time = pd.date_range('2019-02-01', '2019-02-28', freq='D')
    gpis = np.flipud(np.arange(0, 720 * 1440).reshape(720, 1440).astype(np.int32))
    var1 = np.stack([gpis + i for i in range(len(time))], axis=0).astype(np.float32)
    cells = np.flipud(np.repeat(np.arange(36*72).reshape(72, 36).transpose(), 20, axis=1).repeat(20, axis=0)).astype(np.int16)
    gpis = np.flipud(np.arange(0, 720*1440).reshape(720, 1440).astype(np.int32))

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
    #res_stat = res_stat.chunk({'lon': 20, 'lat': 20})
    #res_stat.to_netcdf('/tmp/test.nc')

    datacube2orthomulti(res_stat, '/tmp/cellfiles', n_proc=4,
                        time_from='2019-02-10', cells=[2244,2245,2246,2247])
