import xarray as xr
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, BoundaryNorm
import pandas as pd
from collections import OrderedDict
from typing import List, Union, Literal
from scipy.stats import mode
import pygeogrids

try:
    import matplotlib.pyplot as plt
    import cartopy.crs as ccrs
    plotlibs = True
except ImportError:
    plotlibs = False

# R, G, B, Opacity
colors_values = OrderedDict([
     (0,    [0.156862745098039, 0.156862745098039, 0.156862745098039, 1.0]),
     (20,   [1.0, 0.733333333333333, 0.133333333333333, 1.0]),
     (30,   [1.0, 1.0, 0.298039215686274, 1.0]),
     (40,   [0.941176470588235, 0.588235294117647, 1.0, 1.0]),
     (50,   [0.980392156862745, 0.0, 0.0, 1.0]),
     (60,   [0.705882352941176, 0.705882352941176, 0.705882352941176, 1.0]),
     (70,   [0.941176470588235, 0.941176470588235, 0.941176470588235, 1.0]),
     (80,   [0.0, 0.196078431372549, 0.784313725490196, 1.0]),
     (90,   [0.0, 0.588235294117647, 0.627450980392157, 1.0]),
     (100,  [0.980392156862745, 0.901960784313726, 0.627450980392157, 1.0]),
     (111,  [0.345098039215686, 0.282352941176471, 0.12156862745098, 1.0]),
     (112,  [0.0, 0.6, 0.0, 1.0]),
     (113,  [0.43921568627451, 0.4, 0.243137254901961, 1.0]),
     (114,  [0.0, 0.8, 0.0, 1.0]),
     (115,  [0.305882352941176, 0.458823529411765, 0.12156862745098, 1.0]),
     (116,  [0.0, 0.470588235294118, 0.0, 1.0]),
     (121,  [0.4, 0.376470588235294, 0.0, 1.0]),
     (122,  [0.552941176470588, 0.705882352941176, 0.0, 1.0]),
     (123,  [0.552941176470588, 0.454901960784314, 0.0, 1.0]),
     (124,  [0.627450980392157, 0.862745098039216, 0.0, 1.0]),
     (125,  [0.572549019607843, 0.6, 0.0, 1.0]),
     (126,  [0.392156862745098, 0.549019607843137, 0.0, 1.0]),
     (200,  [0.0, 0.0, 0.501960784313726, 1.0]),
     (255,  [1.0, 1.0, 1.0, 1.0]),
     ])

colors_meanings = OrderedDict([
    (0,     'No input data available'),
    (20,    'Shrubs'),
    (30,    'Herbaceous vegetation'),
    (40,    'Cultivated and managed vegetation/agriculture (cropland)'),
    (50,    'Urban / built up'),
    (60,    'Bare / sparse vegetation'),
    (70,    'Snow and Ice'),
    (80,    'Permanent water bodies'),
    (90,    'Herbaceous wetland'),
    (100,   'Moss and lichen'),
    (111,   'Closed forest, evergreen needle leaf'),
    (112,   'Closed forest, evergreen, broad leaf'),
    (113,   'Closed forest, deciduous needle leaf'),
    (114,   'Closed forest, deciduous broad leaf'),
    (115,   'Closed forest, mixed'),
    (116,   'Closed forest, unknown'),
    (121,   'Open forest, evergreen needle leaf'),
    (122,   'Open forest, evergreen broad leaf'),
    (123,   'Open forest, deciduous needle leaf'),
    (124,   'Open forest, deciduous broad leaf'),
    (125,   'Open forest, mixed'),
    (126,   'Open forest, unknown'),
    (200,   'Open sea'),
    (255,   'No data'),
])

colors_missing = {0: 1., 1: 1., 2: 1., 3: 0.}

def cut_to_n(arr, shp:Union[int, tuple]):
    # shp : (row, col) or el
    if arr.ndim == 1:
        assert isinstance(shp, int), "Expected Single Value"
        over_els = len(arr) % shp
        return arr if over_els == 0 else arr[:-over_els]
    elif arr.ndim == 2:
        assert len(shp) == 2, "Expected Tuple"
        rows, cols = arr.shape
        over_rows = rows % shp[0]
        over_cols = cols % shp[1]
        arr = arr[slice(None) if not over_rows else slice(None, -over_rows),
                  slice(None) if not over_cols else slice(None, -over_cols)]
        return arr
    else:
        raise ValueError("Unexpected input format, pass a 1d or 2d array")


def subblocks(arr, block_y, block_x, handle_mismatch='drop', flatten_inner=True):
    """
    Based on: https://stackoverflow.com/questions/16856788/slice-2d-array-into-smaller-2d-arrays

    Split input array into sub-block of the passed shape.

    e.g. np.array([[1,2,3,4],
                   [5,6,7,8],
                   [9,10,11,12],
                   [13,14,15,16]])

       with block_x=block_y=2:

       np.array([
        np.array([[1,2], [5,6]]),
        np.array([[3,4], [7,8]]),
        np.array([[9,10], [13,14]]),
        np.array([[11,12], [15,16]])
        ])

    Return an array of shape (n, nrows, ncols) where
    n * nrows * ncols = arr.size

    If arr is a 2D array, the returned array should look like n subblocks with
    each subblock preserving the "physical" layout of arr.

    Parameters
    ----------
    arr : np.array
        2d array to split into subblocks
    block_x: int
        Number of elements in each subplot along x dimension
    block_y: int
        Number of elements in each subplot along y dimension
    handle_mismatch : Optional[Literal['drop', 'mirror']]
        Handle cases where the shape of N is not a multiple or the selected
        block size (i.e. when some blocks are not filled).
        e.g. when a 10x10 image is split into 3x3 blocks.
        'drop' : removes any blocks when they are missing elements
        'mirror': mirrors the last column(s)/row(s) to fill incomplete blocks
        None: will raise an Error if the shapes dont match
    flatten_inner: bool, optional (default: True)
        Removes 1 dimension from the returned data, so that each block is a
        single 1d array, instead of a 2d array.
    """
    if not len(arr.shape) == 2:
        raise ValueError("Input array must be a 2d array with full column/rows.")
    rows, cols = arr.shape

    over_rows = rows % block_y
    over_cols = cols % block_x
    if (over_rows != 0) or (over_cols != 0):
        if handle_mismatch.lower() == 'drop':  # drop lines that are too many
            arr = cut_to_n(arr, (block_y, block_x))
            rows, cols = arr.shape
        elif handle_mismatch.lower() == 'mirror':  # repeat last few lines in reverse order to fill the last group
            n_miss_cols, n_miss_rows = (block_x-over_cols), (block_y-over_rows)
            miss_cols = arr[:, -n_miss_cols:][:, ::-1]
            arr = np.append(arr, miss_cols, axis=1)
            miss_rows = arr[-n_miss_rows:, :][::-1]
            arr = np.append(arr, miss_rows, axis=0)
            rows, cols = rows+n_miss_rows, cols+n_miss_cols
        else:
            raise ValueError(f"Passed array has shape ({rows, cols}) which is not divisible"
                             f"by the passed subset shape ({block_y, block_x}). You can"
                             f"pass exact=False to ignore this.")

    blocks = (arr.reshape(rows // block_y,
                          block_y,
                          -1,
                          block_x)
             .swapaxes(1,2)
             .reshape(-1, block_y, block_x))

    blocks = blocks.reshape(rows // block_y,
                            cols // block_x,
                            blocks.shape[1],
                            blocks.shape[2])

    if flatten_inner:
        return blocks.reshape(blocks.shape[0], blocks.shape[1], blocks.shape[2]*blocks.shape[3])
    else:
        return blocks

class CglsLcImg(xr.Dataset):
    """
    Read a single CGLS Landcover classification file from disk into memory
    as xarray Dataset.
    Original files have a resolution of 100 m, which only makes sense for small
    subsets (extent keyword). For large areas, choose a resolution (in degrees)
    to resample the data to.
    ----------------------------------------------------------------------------
    Data is available as global tiff files at
    https://zenodo.org/record/3939050/files/PROBAV_LC100_global_v3.0.1_2019-nrt_Discrete-Classification-map_EPSG-4326.tif
    https://zenodo.org/record/3518038/files/PROBAV_LC100_global_v3.0.1_2018-conso_Discrete-Classification-map_EPSG-4326.tif
    https://zenodo.org/record/3518036/files/PROBAV_LC100_global_v3.0.1_2017-conso_Discrete-Classification-map_EPSG-4326.tif
    https://zenodo.org/record/3518026/files/PROBAV_LC100_global_v3.0.1_2016-conso_Discrete-Classification-map_EPSG-4326.tif
    https://zenodo.org/record/3939038/files/PROBAV_LC100_global_v3.0.1_2015-base_Discrete-Classification-map_EPSG-4326.tif

    """
    _colors_values = colors_values
    _colors_meanings = colors_meanings

    def __init__(self, dataset):
        super(CglsLcImg, self).__init__(dataset)

    @classmethod
    def from_netcdf(cls, path, extent=None) -> 'CglsLcImg':
        """
        Load dataset from file generated with :func:`cgls_lc.CglsLcImg.to_netcdf`

        Parameters
        ----------
        path : str
            Path to the input netcdf file that was generated from original tiff
            using :func:`cgls_lc.CglsLcImg.to_netcdf`
        extent : List[float], optional (default: None)
            Spatial subset to load from the original image
            [min_lon, max_lon, min_lat, max_lat]

        Returns
        -------
        ds : CglsLcImg
        """
        ds = xr.open_dataset(path)
        if extent is not None:
            ds = ds.sel(x=slice(extent[0], extent[1], None),
                        y=slice(extent[3], extent[2], None))
        return cls(ds)

    @classmethod
    def from_tiff(cls, path, extent=None) -> 'CglsLcImg':
        """
        Load dataset from original downloaded tiff files. Needs rasterio installed.

        Parameters
        ----------
        path : str
            Path to the downloaded tiff file.
        extent : List[float], optional (default: None)
            Spatial subset to load from the original image
            [min_lat, max_lat, min_lon, max_lon]

        Returns
        -------
        ds : CglsLcImg
        """
        da = xr.open_rasterio(path)
        if extent is not None:
            da = da.sel(x=slice(extent[2], extent[3], None),
                        y=slice(extent[1], extent[0], None))

        da = da.rename({'x': 'lon', 'y': 'lat'})

        for k in ['transform', 'crs']:
            da.attrs.pop(k)

        year = da.attrs['time_reference_year']

        return cls(da.to_dataset('band').rename({1: f'lc_{year}'}))

    @property
    def extent(self) -> List[float]:
        # get bbox of current dataset [min_lon, max_lon, min_lat, max_lat]
        return [np.min(self['lon'].values),
                np.max(self['lon'].values),
                np.min(self['lat'].values),
                np.max(self['lat'].values)]

    def _gen_cmap(self) -> (LinearSegmentedColormap, BoundaryNorm):
        # Generate CGLS LC colormap from color information.
        df = pd.DataFrame.from_dict(self._colors_values) \
            .T \
            .reindex(range(256)) \
            .fillna(colors_missing)
        colors = df.values
        lc_cmap = LinearSegmentedColormap.from_list(
            'LC cmap', colors, colors.shape[0])
        boundaries = np.array(list(range(colors.shape[0])))
        norm = BoundaryNorm(boundaries,colors.shape[0], clip=True)

        return lc_cmap, norm

    def generate_grid(self, cellsize=5.) -> pygeogrids.CellGrid:
        """
        Generate pygeogrids grid object (CellGrid) from latitude and longitude
        values of the dataset.
        Note: for large subsets (global images) this might not work.

        Parameters
        ----------
        cellsize: float, optional (default: 5.)


        Returns
        -------

        """
        grid = pygeogrids.grids.gridfromdims(
            self['lon'].values, self['lat'].values,origin='bottom')\
            .to_cell_grid(cellsize)

        return grid


    def spatial_resample(self, var='lc_2019', n=100):
        """ 
        Create new instance with reduced resolution (majority filter)
        
        Parameters
        ----------
        var: str
            Name of the variable in the original image to resample.
        n : int, optional (default: 100)
            Resampling factor, e.g. 100 means that 100x100 pixels of the original
            input image are combined (majority filter). The new lat/lon is the mean
            of the original coordinates for each group.

        Returns
        -------
        ds : CglsLcImg
            Resampled data
        """
        if var is None:
            var = [v for v in list(self.variables.keys()) if v not in self.dims]
        var = np.atleast_1d(var)

        resampled_lats = np.apply_along_axis(np.mean, axis=1, arr=np.array(
            np.split(cut_to_n(self['lat'].values, n), len(self['lat']) // n)))
        resampled_lons = np.apply_along_axis(np.mean, axis=1, arr=np.array(
            np.split(cut_to_n(self['lon'].values, n), len(self['lon']) // n)))

        data_vars = {}
        for v in var:
            data_blocks = subblocks(self[v].values, n, n, handle_mismatch='drop',
                                    flatten_inner=True)
            shape2d = (data_blocks.shape[0], data_blocks.shape[1])
            s = data_blocks.reshape(np.prod(shape2d), data_blocks.shape[2])

            data_blocks = np.apply_along_axis(mode, axis=1, arr=s)[:, 0].reshape(shape2d)
            data_vars[v] = (["lat", "lon"], data_blocks)

        return CglsLcImg(xr.Dataset(data_vars=data_vars,
                                    coords=dict(lon=resampled_lons, lat=resampled_lats),
                                    attrs=self.attrs))

    def to_netcdf(self, *args, **kwargs):
        # Write current dataset to (compressed) netcdf file.
        if 'encoding' not in kwargs:
            encoding = {k : dict(zlib=True, complevel=9)
                        for k in self.variables.keys()}
        else:
            encoding = kwargs.pop('encoding')

        super(CglsLcImg, self).to_netcdf(*args, encoding=encoding, **kwargs)

    def plot(self, var='lc_2019', ax=None, **kwargs):
        """
        Plot raster values using the CGLS LC color map using plt.imshow.
        Needs plotting libraries installed.
        """
        if not plotlibs:
            return
        data_crs = ccrs.PlateCarree()

        if ax is None:
            ax = plt.subplot(projection=data_crs)

        ax.set_extent(self.extent, crs=data_crs)
        lc_cmap, norm = self._gen_cmap()
        im = ax.imshow(self[var], transform=data_crs, extent=self.extent,
                       cmap=lc_cmap, norm=norm, **kwargs)

        return im
