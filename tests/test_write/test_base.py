# -*- coding: utf-8 -*-

"""
Module description
"""
# TODO:
#   (+) 
#---------
# NOTES:
#   -

from io_utils.write.new.base import XrBase, NcBase
from smecv_grid.grid import SMECV_Grid_v052
import numpy as np

def test_ncbase():
    return
    outfile = r'C:\Temp\testnc.nc'

    globgrid = SMECV_Grid_v052(None)

    _, lons, lats, _ = globgrid.get_grid_points()
    lons = np.unique(lons)
    lats = np.unique(lats)

    base = NcBase(outfile, mode='w')
    base.create_dim('lon', lons.size)
    base.create_dim('lat', lats.size)
    base.create_dim('time', None) # create unlimited dim time

    test_attr =  {'name': 'test', 'other': 123}
    base.write_var('rand', np.random.rand(3, lats.size, lons.size),
                   dim=('time', 'lat', 'lon'), attr=test_attr)

    other_data = np.full((lats.size, lons.size), np.nan)
    other_data[200:300, 600:700] = 1
    base.append_var(data=other_data, name='rand')




def test_xrbase():
    return
    outfile = r'C:\Temp\test.nc'
    globgrid = SMECV_Grid_v052(None)

    _, lons, lats, _ = globgrid.get_grid_points()
    lons = np.unique(lons)
    lats = np.unique(lats)

    base = XrBase(outfile, mode='w')
    base.create_dim('lon', lons)
    base.create_dim('lat', lats)
    base.create_dim('time', [1,2,3])

    test_attr = {'name': 'test', 'other': 123}
    base.write_var('rand', np.random.rand(3, lats.size, lons.size),
                   dim=('time', 'lat', 'lon'), attr=test_attr)

    assert base.shape('dim')['time'] == 3
    assert base.shape('dim')['lat'] == 720
    assert base.shape('dim')['lon'] == 1440

    other_data = np.full((lats.size, lons.size), np.nan)
    other_data[200:300, 600:700] = 1

    base.expand_dim('time', np.array([4]))

    base.append_var(data=other_data, name='rand', dim=('time'))


    base.flush()




if __name__ == '__main__':
    test_xrbase()
    # test_ncbase()
