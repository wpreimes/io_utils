# -*- coding: utf-8 -*-
from smecv_grid.grid import SMECV_Grid_v052
from pygenio.time_series import IndexedRaggedTs
from pygeobase.io_base import GriddedTsBase
from pygeogrids.grids import CellGrid
import os
import pandas as pd
import pytesmo.timedate.julian as julian

class CCIDs(GriddedTsBase):

    """
    CCI Dataset class reading genericIO data in the CCI common format

    Data in common input format is
    returned as a pandas.DataFrame for temporal resampling.

    Parameters
    ----------
    path : string
        Path to dataset.
    mode : str, optional
        File mode and can be read 'r', write 'w' or append 'a'. Default: 'r'
    grid : grid object
        Grid on which to work
    fn_format : str, optional
        The filename format of the cell files. Default: '{:04d}'
    """

    def __init__(self, path, grid=None, fn_format='{:04d}',
                 custom_dtype=None, **ioclass_kws):
        if grid is None:
            grid = SMECV_Grid_v052()

        if 'custom_dtype' not in ioclass_kws.keys():
            ioclass_kws['custom_dtype'] = custom_dtype

        super(CCIDs, self).__init__(path, grid, IndexedRaggedTs,
                                    mode='r',
                                    fn_format=fn_format,
                                    ioclass_kws=ioclass_kws)

    def _read_gp(self, gpi, only_valid=False, mask_sm_nan=False,
                 mask_invalid_flags=False, sm_nan=-999999.,
                 mask_jd=False, jd_min=2299160, jd_max=1827933925,
                 valid_flag=0, **kwargs):
        """
        Read data into common format

        Parameters
        ----------
        self: type
            description
        gpi: int
            grid point index
        only_valid: boolen, optional
           if set only valid observations will be returned.
           This means that the data will be masked for soil moisture
           NaN values and also for flags other than 0
        mask_sm_nan: boolean, optional
           if set to True then the time series will be masked
           for soil moisture NaN values
        mask_invalid_flags: boolean, optional
           if set then all flags that do not have the value of
           valid_flag are removed
        sm_nan: float, optional
           value to use as soil moisture NaN
        valid_flag: int, optional
           value indicating a valid flag

        Returns
        -------
        ts: pandas.DataFrame
            DataFrame in common format
        """

        ts = super(CCIDs, self)._read_gp(gpi, **kwargs)

        if ts is None:
            return None

        if only_valid:
            mask_sm_nan = True
            mask_invalid_flags = True
        if mask_sm_nan:
            ts = ts[ts['sm'] != sm_nan]
        if mask_invalid_flags:
            ts = ts[ts['flag'] == valid_flag]
        if mask_jd:
            ts = ts[(ts['jd'] >= jd_min) & (ts['jd'] <= jd_max)]
        if ts.size == 0:
            raise IOError("No data for gpi %i" % gpi)

        index_tz = julian.julian2datetimeindex(ts['jd'])
        index_no_tz = pd.DatetimeIndex([i.tz_localize(None) for i in index_tz])

        ts = pd.DataFrame(ts, index=index_no_tz)

        # ts = pd.DataFrame(ts, index=julian.julian2datetimeindex(ts['jd']))

        return ts

    def read_cell(self, cell):
        """
        Read complete data set from cell file.

        Parameters
        ----------
        cell : int
            Cell number.

        Returns
        -------
        location_id : numpy.ndarray
            Location ids.
        cell_data : numpy.recarray
            Cell data set.
        """
        if isinstance(self.grid, CellGrid) is False:
            raise TypeError("Associated grid is not of type "
                            "pygeogrids.CellGrid.")

        if self.mode != 'r':
            raise ValueError("File not opened in read mode.")

        filename = os.path.join(self.path, self.fn_format.format(cell))
        self.fid = self.ioclass(filename, mode=self.mode, **self.ioclass_kws)

        cell_data = self.fid.dat_fid.read()
        self.fid.dat_fid.close()

        return self.fid.idx, cell_data