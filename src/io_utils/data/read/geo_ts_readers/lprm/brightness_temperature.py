import os
import numpy as np
import pandas as pd
from pygeobase.io_base import ImageBase, MultiTemporalImageBase
from pygeobase.object_base import Image
from datetime import datetime
from pygeogrids.grids import gridfromdims
from pygeogrids.netcdf import load_grid
from pynetcf.time_series import GriddedNcOrthoMultiTs
import xarray as xr

"""
Readers for raw (brightness temperature) data used in LPRM to derive soil
moisture from passive sensors
"""

class LprmBtNcImg(ImageBase):
        """
        Class for reading one Brightness Temperature nc (from tif) File.
        BT values are resampled to a regular 0.25 grid already.
        """

        def __init__(
            self,
            filename,
            mode="r",
            subgrid=None,
            parameters=None,
            array_1D=False,
        ):
            """
            Parameters
            ----------
            filename: str
                filename of the tiff file
            mode: string, optional
                mode of opening the file, only 'r' is implemented at the moment
            parameters : list[str], optional (default: None)
                List of paramters to read. If None, all parameters are read.
            subgrid : Cell Grid
                Subgrid of the global SMECV Grid to use for reading image data
                (e.g only land points)
            array_1D: boolean, optional
                if set then the data is read into 1D arrays.
                Needed for some legacy code.
            """

            super().__init__(filename, mode=mode)

            self.parameters = parameters
            self.grid = subgrid
            self.array_1D = array_1D

        def _check_grid_2d_compatible(self) -> bool:
            # Check data for the chosen grid can be reshaped to 2d array
            compat2d = False
            nlons = len(np.unique(self.grid.activearrlon))
            nlats = len(np.unique(self.grid.activearrlat))
            if self.grid.activegpis.size == nlons * nlats:
                compat2d = True
            self.shape = (nlats, nlons)
            return compat2d

        def read(self, timestamp):
            """
            Read data from image to numpy arrays

            Parameters
            ----------
            timestamp: datetime
                There is not time information in the file itself. But in the
                filename. However, we don't parse the filename, but it is
                required to pass the time stamp to the read function.

            Returns
            -------
            img: Image
            """

            try:
                ds = xr.open_dataset(self.filename, engine='netcdf4')
            except IOError:
                raise IOError(f"Error opening file {self.filename}")

            if self.grid is None:
                self.grid = gridfromdims(ds['lon'].values, ds['lat'].values,
                                         origin='bottom')

            compat2d = self._check_grid_2d_compatible()

            if (not compat2d) and (not self.array_1D):
                raise ValueError(
                    "To read data as 2d images, grid must be a gap-free "
                    "subset of the global SMECV grid. Try `array_1D=True` "
                    "instead."
                )

            if self.parameters is None:
                self.parameters = list(ds.data_vars.keys())

            # data is sorted from lower left corner to upper right corner
            # and flattened into a 1d array.
            data = {
                p: np.flipud(ds[p].values[0, ...]).flatten()[self.grid.activegpis]
                for p in self.parameters
            }

            if self.array_1D:
                return Image(
                    self.grid.activearrlon,
                    self.grid.activearrlat,
                    data,
                    metadata=dict(),
                    timestamp=timestamp,
                )
            else:
                for key in data:
                    data[key] = np.flipud(
                        data[key].reshape(self.shape)
                    )

                return Image(
                    np.flipud(self.grid.activearrlon.reshape(self.shape)),
                    np.flipud(self.grid.activearrlat.reshape(self.shape)),
                    data,
                    metadata=dict(),
                    timestamp=timestamp,
                )


class LprmBtNcDs(MultiTemporalImageBase):

    def __init__(
        self,
        data_path,
        parameters=None,
        fname_templ="AMSR2_BT_{datetime}.nc",
        datetime_format="%Y%m%d",
        subpath_templ=None,
        subgrid=None,
        array_1D=False,
    ):
        """
        Class for reading a collection of Brightness Temperature Netcdf Files.

        Parameters
        ----------
        data_path : str
            Path to the folder containing the BT
        parameters : list[str], optional (default: None)
            List of paramters to read. If None, all parameters are read.
        fname_templ : str, optional (default: AMSR2_BT_{datetime}.nc)
            template for the file names, must contain a placeholder {datetime}
            where the time stamp of the image is found.
            Can contain * or ? wildcards (must NOT be contained in the original
            file name)
        datetime_format : str, optional (default: %Y%m%d)
            How the date in the filename ({datetime}) is formatted.
        subgrid : CellGrid or None, optional (default: None)
            Subgrid of the global SMECV Grid to use for reading image data
            (e.g only land points). If None is passed, then a (global) gapfree
            grid is created from the nc files.
        array_1D: boolean, optional (default: False)
            If set then the data is read into 1D arrays.
        """
        ioclass_kws = {
            "parameters": parameters,
            "subgrid": subgrid,
            "array_1D": array_1D,
        }

        exact_templ = True
        for char in ['*', '?']:
            if char in fname_templ:
                exact_templ = False
                break

        super().__init__(
            data_path,
            LprmBtNcImg,
            fname_templ=fname_templ,
            datetime_format=datetime_format,
            subpath_templ=subpath_templ,
            ioclass_kws=ioclass_kws,
            exact_templ=exact_templ,
        )

    def tstamps_for_daterange(self, start_date, end_date):
        """
        return timestamps for daterange,

        Parameters
        ----------
        start_date: datetime
            start of date range
        end_date: datetime
            end of date range

        Returns
        -------
        timestamps : list
            list of datetime objects of each available image between
            start_date and end_date
        """
        dt = pd.date_range(start_date, end_date, freq="D")
        return [dt.to_pydatetime() for dt in dt]

class TsReader(GriddedNcOrthoMultiTs):
    def __init__(self, ts_path, grid_path=None, remove_outliers=3, **kwargs):
        """
        Just the same as GriddedNcOrthoMultiTs...

        Class for reading time series after reshuffling.

        Parameters
        ----------
        ts_path : str
            Directory where the netcdf time series files are stored
        grid_path : str, optional (default: None)
            Path to grid file, that is used to organize the location of time
            series to read. If None is passed, grid.nc is searched for in the
            ts_path.
        remove_outliers: int or None, optional (default: 3)
            If not None, outliers are removed from the time series if they are
            above or below N*std from the mean of the time series. Where N is
            the here passed integer.


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
        self.remove_outliers = remove_outliers
        if grid_path is None:
            grid_path = os.path.join(ts_path, "grid.nc")

        grid = load_grid(grid_path)
        super().__init__(ts_path, grid, **kwargs)

    def read(self, *args, **kwargs):
        ts = super().read(*args, **kwargs)
        if self.remove_outliers is not None:
            outliers = abs(ts - ts.mean())  > self.remove_outliers * ts.std()
            ts = ts.mask(outliers, np.nan)

        return ts

    def read_ts(self, *args, **kwargs):
        self.read(*args, **kwargs)


if __name__ == '__main__':
    from io_utils.data.read.geo_ts_readers.adapters import PreprocessingAdapter, lprm_bt2surft
    path = "/home/wpreimes/shares/climers/Projects/CCIplus_Soil_Moisture/07_data/BrightnessTemperature/time_series/AMSR2/"
    reader = PreprocessingAdapter(TsReader(path, ioclass_kws={'read_bulk': True}),
                                  func=lprm_bt2surft, column='bt_36.5V')
    img = reader.read(30, 8.5)
