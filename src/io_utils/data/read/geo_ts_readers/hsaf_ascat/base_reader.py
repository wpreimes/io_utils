# -*- coding: utf-8 -*-

from ascat.h_saf import AscatGriddedNcTs
import os
from pynetcf.time_series import GriddedNcOrthoMultiTs
from pygeogrids.netcdf import load_grid
from io_utils.data.read.geo_ts_readers.mixins import (
    ContiguousRaggedTsCellReaderMixin,
    OrthoMultiTsCellReaderMixin,
)

class HSAFAscatSSMTs(AscatGriddedNcTs, ContiguousRaggedTsCellReaderMixin):

    def __init__(self, ts_path, grid_path=None,
                 fn_format="H115_H116_{:04d}", **kwargs):

        if grid_path is None:
            grid_path = os.path.join(ts_path, "grid.nc")

        if 'exact_index' in kwargs:
            if not kwargs['exact_index']:
                raise NotImplementedError("Use the resampling keyword instead.")
            else:
                kwargs.pop('exact_index')

        super(HSAFAscatSSMTs, self).__init__(path=ts_path,
                                             fn_format=fn_format,
                                             grid_filename=grid_path,
                                             **kwargs)


class HSAFAscatSMDASTs(GriddedNcOrthoMultiTs, OrthoMultiTsCellReaderMixin):

    def __init__(self, ts_path, grid_path=None, **kwargs):
        """
        Class for reading GLDAS time series after reshuffling.
        Parameters
        ----------
        ts_path : str
            Directory where the netcdf time series files are stored
        grid_path : str, optional (default: None)
            Path to grid file, that is used to organize the location of time
            series to read. If None is passed, grid.nc is searched for in the
            ts_path.
        Optional keyword arguments that are passed to the Gridded Base:
        ------------------------------------------------------------------------
            parameters : list, optional (default: None)
                Specific variable names to read, if None are selected, all are read.
            offsets : dict, optional (default:None)
                Offsets (values) that are added to the parameters (keys)
            scale_factors : dict, optional (default:None)
                Offset (value) that the parameters (key) is multiplied with
            ioclass_kws: dict
                Optional keyword arguments to pass to OrthoMultiTs class:
                ----------------------------------------------------------------
                    read_bulk : boolean, optional (default:False)
                        if set to True the data of all locations is read into memory,
                        and subsequent calls to read_ts read from the cache and not from disk
                        this makes reading complete files faster#
                    read_dates : boolean, optional (default:False)
                        if false dates will not be read automatically but only on specific
                        request useable for bulk reading because currently the netCDF
                        num2date routine is very slow for big datasets
        """
        if grid_path is None:
            grid_path = os.path.join(ts_path, "grid.nc")

        grid = load_grid(grid_path)
        super(HSAFAscatSMDASTs, self).__init__(ts_path, grid, **kwargs)

if __name__ == '__main__':
    from ascat.h_saf import AscatGriddedNcTs
    grid = "/home/wpreimes/shares/radar/Projects/H_SAF_CDOP4/05_deliverables_products/auxiliary/warp5_grid/TUW_WARP5_grid_info_2_3.nc"
    path = "/home/wpreimes/shares/radar/Projects/H_SAF_CDOP4/05_deliverables_products/H120/H119_H120r14"
    ds = AscatGriddedNcTs(path, fn_format="H119_H120_{:04d}", grid_filename=grid)
    ts = ds.read(15, 45)