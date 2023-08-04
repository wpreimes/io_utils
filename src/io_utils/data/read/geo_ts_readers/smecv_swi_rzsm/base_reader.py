# -*- coding: utf-8 -*-

"""
Reader for the ESA CCI SWI time series data of different versions
"""
# TODO:
#   (+)
#---------
# NOTES:
#   -

from io_utils.data.read.geo_ts_readers.esa_cci_sm.base_reader import SmecvTs

class GeoSmecvSwiRzsmTs(SmecvTs):
    # Reader implementation that uses the PATH configuration from above

    # fill values in the data columns
    _col_fillvalues = {}

    def __init__(self, ts_path, grid_path=None, **kwargs):

        super(GeoSmecvSwiRzsmTs, self).__init__(ts_path, grid=grid_path, **kwargs)

    def read(self, *args, **kwargs):
        return super(GeoSmecvSwiRzsmTs, self).read(*args, **kwargs)

