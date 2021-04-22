# -*- coding: utf-8 -*-

"""
Module description
"""
# TODO:
#   (+) 
#---------
# NOTES:
#   -

import numpy as np
import pandas as pd
from tempfile import TemporaryDirectory
import os
import time

from io_utils.write.scattered_cube import NcScatteredStack
from tests.test_write.test_regular_stack_writer import generate_random_data


def test_write_point():
    return
    # todo: impelement stack writer, then test

    p = 10
    out_root = tempfile.mkdtemp()
    stack_out = os.path.join(out_root, 'stack')
    imgs_out = os.path.join(out_root, 'imgs')

    index = pd.date_range('2000-01-01', '2000-01-10', freq='D')
    zs = pd.to_datetime(index).to_pydatetime()

    os.makedirs(stack_out, exist_ok=True)
    filepath = os.path.join(stack_out, 'stack.nc')
    img_writer = NcScatteredStack(filepath, z=zs, z_name='time')

    # write data for one loc at one time
    for lon, lat in zip(np.random.uniform(-179, 179, p),
                        np.random.uniform(-89, 89, p)):
        for z in zs:
            data = generate_random_data([z], size=1)
            img_writer.write_point(lon, lat, z, data[z])

    # write data for one loc at all times
    for lon, lat in zip(np.random.uniform(-179, 179, p),
                        np.random.uniform(-89, 89, p)):

        data = generate_random_data([0], size=p)
        img_writer.write_point(np.array([lon] * p),
                               np.array([lat] * p),
                               zs, data[0])

    # write data for all locs at all times
    data = generate_random_data([0], size=p*int(zs.size))
    lons = np.random.uniform(-179, 179, p)
    lats = np.random.uniform(-89, 89, p)
    img_writer.write_point(np.repeat(lons, zs.size),
                           np.repeat(lats, zs.size),
                           np.repeat(zs, zs.size), data[0])

    start = time.time()
    os.makedirs(imgs_out, exist_ok=True)
    img_writer.store_files(imgs_out)
    end = time.time()
    print('Writing file took {} seconds'.format(end - start))

    assert os.path.isfile(os.path.join(stack_out, 'stack.nc'))
    assert len(os.listdir(imgs_out)) == zs.size

if __name__ == '__main__':
    test_write_point()