# -*- coding: utf-8 -*-

from io_utils.data.write.regular_cube import NcRegGridStack
import numpy as np
from smecv_grid import SMECV_Grid_v052
import pandas as pd
import tempfile
import os
import time

def generate_random_data(z:np.array, n_var:int=10, size=1):
    data = {}
    for t in z:
        if size == 1:
            zd =  {'var{}'.format(i): np.random.rand(1)[0] for i in range(n_var)}
        else:
            zd =  {'var{}'.format(i): np.random.rand(size) for i in range(n_var)}
        data[t] = zd

    return  data

def test_write_area():
    out_root = tempfile.mkdtemp()
    stack_out = os.path.join(out_root, 'stack')
    imgs_out = os.path.join(out_root, 'imgs')

    index = pd.date_range('2000-01-01', '2000-01-10', freq='D')
    zs = pd.to_datetime(index).to_pydatetime()

    img_writer = NcRegGridStack(dx=0.25, dy=0.25, z=zs, z_name='time')

    land_grid = SMECV_Grid_v052('land')

    cell = [2283]
    print(cell)
    cell_gpis, cell_lons, cell_lats = land_grid.grid_points_for_cell(cell)
    for z in img_writer.ds.time.values:
        df = pd.DataFrame(index=range(cell_gpis.size),
                          data={'lon': cell_lons,
                                'lat': cell_lats,
                                'var1': np.random.rand(cell_gpis.size),
                                'var2': np.random.rand(cell_gpis.size)})
        img_writer.write_image(df, z=z)

    start = time.time()
    os.makedirs(stack_out, exist_ok=True)
    img_writer.store_stack(os.path.join(stack_out, 'stack.nc'))
    os.makedirs(imgs_out, exist_ok=True)
    img_writer.store_files(imgs_out)
    end = time.time()
    print('Writing file took {} seconds'.format(end - start))

    assert os.path.isfile(os.path.join(stack_out, 'stack.nc'))
    assert len(os.listdir(imgs_out)) == zs.size


def test_write_points():
    # test writing a small stack of global validation results point by point
    out_root = tempfile.mkdtemp()
    stack_out = os.path.join(out_root, 'stack')
    imgs_out = os.path.join(out_root, 'imgs')

    index = np.array(['2000-01-01 to 2010-12-10',
                      '2011-01-01 to 2018-12-10'])
    z = index

    land_grid = SMECV_Grid_v052('land')

    img_writer = NcRegGridStack(dx=0.25, dy=0.25, z=z, z_name='period')

    gpis, lons, lats, cells = land_grid.subgrid_from_cells(2244).get_grid_points()
    data = generate_random_data(z=index, n_var=5, size=lons.size)
    idx = '2000-01-01 to 2010-12-10'
    data_dict = data[idx]
    img_writer.write_point(lons, lats, z=np.array([idx]*lons.size), data=data_dict)

    idx = '2011-01-01 to 2018-12-10'
    data_dict = data[idx]
    img_writer.write_point(lons, lats, z=np.array([idx]*lons.size), data=data_dict)

    start = time.time()
    os.makedirs(stack_out, exist_ok=True)
    img_writer.store_stack(os.path.join(stack_out, 'stack.nc'))
    os.makedirs(imgs_out, exist_ok=True)
    img_writer.store_files(imgs_out)
    end = time.time()
    print('Writing file took {} seconds'.format(end - start))

    assert os.path.isfile(os.path.join(stack_out, 'stack.nc'))
    assert len(os.listdir(imgs_out)) == index.size

def test_write_ts():

    out_root = tempfile.mkdtemp()
    stack_out = os.path.join(out_root, 'stack')
    imgs_out = os.path.join(out_root, 'imgs')

    index = pd.date_range('2000-01-01', '2000-01-10', freq='D')
    z = pd.to_datetime(index).to_pydatetime()

    land_grid = SMECV_Grid_v052('land')

    ts_writer = NcRegGridStack(dx=0.25, dy=0.25, z=z, z_name='time')

    gpis, lons, lats, cells = land_grid.get_grid_points()
    i=0
    for lon, lat in zip(lons, lats):
        if i > 10: break
        data = pd.DataFrame(index=index,
                            data={'var_{}'.format(i): np.random.rand(10) for i in range(5)})
        ts_writer.write_series(lon, lat, data)
        i+=1

    start = time.time()
    os.makedirs(stack_out, exist_ok=True)
    ts_writer.store_stack(os.path.join(stack_out, 'stack.nc'))
    os.makedirs(imgs_out, exist_ok=True)
    ts_writer.store_files(imgs_out)
    end = time.time()
    print('Writing file took {} seconds'.format(end - start))

    assert os.path.isfile(os.path.join(stack_out, 'stack.nc'))
    assert len(os.listdir(imgs_out)) == z.size

if __name__ == '__main__':
    test_write_area()
    test_write_ts()
    test_write_points()
