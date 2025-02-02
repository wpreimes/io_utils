import numpy as np
import pandas as pd
import cartopy
import cartopy.crs as ccrs
import matplotlib as mpl
import matplotlib.pyplot as plt
import cartopy.mpl.geoaxes as geoaxes
from io_utils.plot.misc import map_add_grid, map_add_cbar, meshgrid

def reshape_dat(ds, ndims=2) -> dict:
    """
    Bring data into 2d array shape that contourf and pcolormesh expect.

    Parameters
    ----------
    ds: pd.Series
        The dataset to plot. The index must be a MultiIndex with the first
        level being latitudes and the second level being longitudes.
        The data is in the values.

    Returns
    -------
    data: dict
        Dictionary with keys 'lon', 'lat', 'data'
    """
    names = list(ds.index.names)

    lat_names = ['lat', 'latitude', 'y']
    lon_names = ['lon', 'longitude', 'x']
    ilat = 0
    for n in lat_names:
        if n in names:
            ilat = names.index(n)
    ilon = 1
    for n in lon_names:
        if n in names:
            ilon = names.index(n)

    lats = ds.index.get_level_values(ilat).values
    lons = ds.index.get_level_values(ilon).values

    if ndims == 1:
        data = {'lon': lons, 'lat': lats, 'data': ds.values}
        return data
    if ndims == 2:
        raster = meshgrid(lons, lats)
        lons2d = np.reshape(raster.activearrlon, raster.shape)
        lats2d = np.reshape(raster.activearrlat, raster.shape)

        gpis, _ = raster.find_nearest_gpi(lons, lats)

        dat = np.full(raster.shape, np.nan).flatten()
        np.put(dat, gpis, ds.values)
        dat = dat.reshape(raster.shape)
        data = {'lon': lons2d, 'lat': lats2d, 'data': dat}
    else:
        raise NotImplementedError('ndims must be 1 or 2')

    return data

class MapPlotter:
    def __init__(self, figsize=(8, 4), llc=(-179.9999, -60.),
                 urc=(179.9999, 80), projection=ccrs.Robinson(), ax=None):
        """
        Wrapper around cartopy, pandas and matplotlib to plot data on a map.
        Should handle most simple map cases. For more specific cases, use
        cartopy directly.

        Parameters
        ----------
        figsize: tuple[float, float], optional (default: (8, 4))
            Figure size in inches
        llc: tuple[float, float], optional (default: (-179.9999, -60.))
            Lower left corner of the map (in degrees)
        urc: tuple[float, float], optional (default: (179.9999, 80))
            Upper right corner of the map (in degrees)
        projection: cartopy.crs.Projection, optional (default: ccrs.Robinson())
            Projection of the map (not of the data!)
        ax: matplotlib.axes.Axes, optional (default: None)
            If given, the map will be plotted into this axis.
        """
        self.data_crs = ccrs.PlateCarree()

        if ax is None:
            self.fig = plt.figure(num=None, figsize=figsize, facecolor='w',
                                  edgecolor='k')
            self.ax = plt.axes(projection=projection)
        else:
            if not isinstance(ax, geoaxes.GeoAxes):
                raise ValueError('ax must be a cartopy GeoAxes')
            self.fig = None
            self.ax = ax

        self.ax.set_extent([llc[0], urc[0], llc[1], urc[1]], crs=self.data_crs)

    def __del__(self):
        plt.close(self.fig)

    def add_gridlines(self, grid_loc='0110', gridspace=(60, 20), fontsize=5):
        """
        Add grid lines and lables to the map.

        Parameters
        ----------
        grid_loc : str, optional (default: '0110')
            Location of the grid labels.
            first digit = upper, second digit = right, third digit = lower,
            fourth digit = left
        gridspace: tuple, (optional), default: (30, 20)
            Space between grid lines in degrees. First value is for latitude,
        fontsize: int, optional (default: 5)
            Fontsize of the grid labels (if they are drawn)
        """
        bounds = self.ax.get_extent(crs=self.data_crs)
        llc, urc = (bounds[0], bounds[2]), (bounds[1], bounds[3])
        draw_labels = True if '1' in grid_loc else False
        map_add_grid(self.ax, self.ax.projection, grid_loc=grid_loc, llc=llc,
                     urc=urc, gridspace=gridspace, draw_labels=draw_labels,
                     fontsize=fontsize)

    def add_basemap(self, land_color='white', ocean=False, lakes=False,
                    rivers=False, coastline_size='110m',
                    states=False, borders=False,
                    linewidth_mult=1):
        """
        Add a basemap and basemap features to the map. Note for more advanced
        basemaps, use cartopy and add them directly to the self.imax.

        Parameters
        ----------
        land_color: str or None, optional (default: 'white')
            Color of the land on the map
        ocean: bool or str, optional (default: False)
            False: White / transparent ocean color
            True: Draw ocean in lightskyblue color
            string: Draw ocean in the given color
        coastline_size: str, optional (default: '110m')
            Resolution of the coastlines. See cartopy documentation for
            details.
        states: bool, optional (default: False)
            Whether to add states boundaries to the map.
        borders: bool, optional (default: False)
            Whether to add country borders to the map.
        """
        if ocean:
            facecolor = 'lightskyblue' if ocean is True else ocean
            self.ax.add_feature(
                cartopy.feature.OCEAN, zorder=0, facecolor=facecolor)
        self.ax.add_feature(
            cartopy.feature.LAND, zorder=0, facecolor=land_color)
        if rivers:
            self.ax.add_feature(cartopy.feature.RIVERS, zorder=5,
                                facecolor="lightskyblue")
        if lakes:
            self.ax.add_feature(
                cartopy.feature.LAKES, zorder=5, facecolor="lightskyblue"
            )

        self.ax.coastlines(
            resolution=coastline_size, color='black', zorder=5,
            linewidth=linewidth_mult*0.25)

        if states:
            self.ax.add_feature(
                cartopy.feature.STATES, linewidth=0.05*linewidth_mult, zorder=5)
        if borders:
            self.ax.add_feature(
                cartopy.feature.BORDERS, linewidth=0.1*linewidth_mult, zorder=5)

    def add_colormesh_layer(self, ds, cmap=plt.get_cmap('RdYlBu'), scalef=1,
                            clim=None, add_cbar=False, cbar_kwargs=None):
        """
        Draw a colormesh raster layer for the given dataset.

        Parameters
        ----------
        ds: pd.Series
            The dataset to plot. The index must be a MultiIndex with the
            levels 'lat' and 'lon'. The values must be the data to plot.
        cmap: str or matplotlib.colors.Colormap, optional (default: RdYlBu)
            The colormap to use
        clim: tuple, optional (default: None)
            The range of the colorbar (min, max). When a colorbar is added,
            it will show this range. If None, then matplotlib decides.
            You can also set one of min or max to None.
        add_cbar: bool, optional
            Add colorbar based on this layer
        cbar_kwargs: dict, optional (default: None)
            Keyword arguments passed to the colorbar function. For details see
            :func:`io_utils.plot.misc.map_add_cbar`:
                - cb_label : str, optional (default: None)
                - cb_loc : str, optional (default: bottom)
                - cb_ticksize: int, optional (default: 5)
                - cb_labelsize : int, optional (default: 7)
                - cb_extend : str, optional (default: Both)
                - cb_n_ticks : int, optional (default: None)
                - cb_ext_label_min : str, optional (default: None)
                - cb_ext_label_max : str, optional (default: None)
                - cb_text : list, optional (default: None)

        Returns
        -------
        p: plt.Colormesh
        """
        dat = reshape_dat(ds, ndims=2)

        if isinstance(cmap, str):
            cmap = plt.get_cmap(cmap)

        p = self.ax.pcolormesh(dat['lon'], dat['lat'], dat['data']*scalef,
                               zorder=3,
                               cmap=cmap, transform=ccrs.PlateCarree())

        if clim is not None:
            p.set_clim(vmin=clim[0], vmax=clim[1])

        if add_cbar:
            cbar_kwargs = cbar_kwargs or {}
            map_add_cbar(self.fig, self.ax, p, **cbar_kwargs)

        return p

    def add_contour_layer(self, ds, cmap=plt.get_cmap('RdYlBu', 13),
                          scalef=1, clim=None, add_cbar=False, cbar_kwargs=None):
        """
        Draw a contour layer for the given dataset.

        Parameters
        ----------
        ds: pd.Series
            The dataset to plot. The index must be a MultiIndex with the
            levels 'lat' and 'lon'. The values must be the data to plot.
        cmap: str or matplotlib.colors.Colormap, optional (default: RdYlBu)
            The colormap to use, should not have too many levels.
        clim: tuple, optional (default: None)
            The range of the colorbar (min, max). When a colorbar is added,
            it will show this range. If None, then matplotlib decides.
            You can also set one of min or max to None.
        add_cbar: bool, optional
            Add colorbar based on this layer
        cbar_kwargs: dict, optional (default: None)
            Keyword arguments passed to the colorbar function. For details see
            :func:`io_utils.plot.misc.map_add_cbar`:
                - cb_label : str, optional (default: None)
                - cb_loc : str, optional (default: bottom)
                - cb_ticksize: int, optional (default: 5)
                - cb_labelsize : int, optional (default: 7)
                - cb_extend : str, optional (default: Both)
                - cb_n_ticks : int, optional (default: None)
                - cb_ext_label_min : str, optional (default: None)
                - cb_ext_label_max : str, optional (default: None)
                - cb_text : list, optional (default: None)

        Returns
        -------
        p: plt.Colormesh
        """
        dat = reshape_dat(ds, ndims=2)

        c = dat['data'] * scalef
        if clim is None:
            clim = (np.nanquantile(c.values, 0.01),
                    np.nanquantile(c.values, 0.99))

        n_steps = cmap.N
        step_size = (clim[1] - clim[0]) / n_steps
        levels = np.arange(clim[0], clim[1] + step_size, step_size)

        if 'cb_extend' in cbar_kwargs:
            extend = cbar_kwargs['cb_extend']
        else:
            extend = 'both'

        p = self.ax.contourf(dat['lon'], dat['lat'], c,
                             transform=ccrs.PlateCarree(),
                             vmin=clim[0], vmax=clim[1],
                             levels=levels, extend=extend,
                             cmap=cmap)

        if add_cbar:
            cbar_kwargs = cbar_kwargs or {}
            map_add_cbar(self.fig, self.ax, p, **cbar_kwargs)

        return p


    def add_scatter_layer(self, ds, marker='.', s=1, cmap=plt.get_cmap('RdYlBu'),
                          clim=None, add_cbar=False, cbar_kwargs=None):
        """
        Add a scatter layer to the map, where the points are colored based
        on the passed color map.

        Parameters
        ----------
        ds: pd.Series
            The dataset to plot. The index must be a MultiIndex with the
            levels 'lat' and 'lon'. The values are floats that indicate how
            the points should be colored.
        marker: str, optional (default: '.')
            Marker of the scatter points, see matplotlib documentation for
            details.
        s: int or np.array, optional (default: 1)
            Size of the scatter points. EIther a single value that is applied
            to all points or an array of the same shape as the data.
        cmap: matplotlib.colors.Colormap or str, optional (default: RdYlBu)
            If a string is given, it must be valid color name.
            If a colormap is given the scatter points will be colored
            based on their value.
        clim: tuple, optional (default: None)
            The range of the colorbar (min, max). When a colorbar is added,
            it will show this range. If None, then matplotlib decides.
            You can also set one of min or max to None.
        add_cbar: bool, optional (default: False)
            Add colorbar based on this layer
        cbar_kwargs: dict, optional (default: None)
            Keyword arguments passed to the colorbar function. For details see
            :func:`io_utils.plot.misc.map_add_cbar`:
                - cb_label : str, optional (default: None)
                - cb_loc : str, optional (default: bottom)
                - cb_ticksize: int, optional (default: 5)
                - cb_labelsize : int, optional (default: 7)
                - cb_extend : str, optional (default: Both)
                - cb_n_ticks : int, optional (default: None)
                - cb_ext_label_min : str, optional (default: None)
                - cb_ext_label_max : str, optional (default: None)
                - cb_text : list, optional (default: None)
        """

        dat = reshape_dat(ds, ndims=1)

        p = self.ax.scatter(
            dat['lon'], dat['lat'], c=dat['data'],
            transform=ccrs.PlateCarree(),
            marker=marker,
            cmap=cmap,
            s=s,
            zorder=3,
        )

        if clim is not None:
            p.set_clim(vmin=clim[0], vmax=clim[1])

        if add_cbar:
            cbar_kwargs = cbar_kwargs or {}
            map_add_cbar(self.fig, self.ax, p, **cbar_kwargs)

    def add_hatch_overlay(self, ds, density=3, pattern='/', colors='none', lw=1):
        """
        Add a countour layer to the map. This is useful for overlayers and
        only support simple hatches and no color maps.
        See also https://matplotlib.org/stable/gallery/shapes_and_collections/hatch_style_reference.html

        Parameters
        ----------
        ds: pd.Series
            The dataset to plot. The index must be a MultiIndex with the
            levels 'lat' and 'lon'. The values are boolean values, where True
            means that the point should be marked.
        density: int, optional (default: 3)
            Density of the hatch lines (>=0). Higher density means more
            (smaller) features. 0 means no features.
        pattern: str, optional (default: '/')
            Hatch pattern, contour lines, see matplotlib documentation for
            details.
            e.g, /, ., o, +, -, etc
        colors: str, optional (default: 'none')
            Color of the contour lines. color string or sequence of colors.
            Default is 'none'
        lw: int, optional (default: 1)
            Line width of the contour lines.
        """
        dat = reshape_dat(ds, ndims=2)
        _lw = mpl.rcParams['hatch.linewidth']
        mpl.rcParams['hatch.linewidth'] = lw
        self.ax.contourf(
            dat['lon'], dat['lat'], dat['data'],
            transform=ccrs.PlateCarree(),
            colors=colors,
            levels=[.5, 1.5],
            zorder=3,
            hatches=[density * pattern, density * pattern],
        )
        mpl.rcParams['hatch.linewidth'] = _lw

    def add_scatter_overlay(self, ds, marker='.', s=1, color='black'):
        """
        Add a scatter layer to the map without a colormap.

        Parameters
        ----------
        ds: pd.Series
            The dataset to plot. The index must be a MultiIndex with the
            levels 'lat' and 'lon'. The values are boolean values, where True
            means that the point should be marked.
        marker: str, optional (default: '.')
            Marker of the scatter points, see matplotlib documentation for
            details.
        s: int or np.array, optional (default: 1)
            Size of the scatter points. EIther a single value that is applied
            to all points or an array of the same shape as the data.
        color: str, optional (default: 'black')
            Color of the scatter points, see matplotlib documentation for
            details.
        """
        ds = ds.astype(bool)
        ds[ds == False] = np.nan
        ds = ds.dropna()

        data = reshape_dat(ds, ndims=1)

        self.ax.scatter(
            data['lon'], data['lat'], c=color,
            transform=ccrs.PlateCarree(),
            marker=marker,
            s=s,
            zorder=3,
        )

    def savefig(self, fname, dpi=300, bbox_inches='tight', *args, **kwargs):
        """
        Save figure to file.

        Parameters
        ----------
        fname: str
            Filename to save the figure to
        dpi: int, optional (default: 300)
            Dots per inch
        *args, **kwargs
            Additional arguments passed to the savefig function
        """
        self.fig.savefig(fname, dpi=dpi, bbox_inches=bbox_inches,
                         *args, **kwargs)


if __name__ == '__main__':

    """
    ds = xr.open_dataset("/home/wpreimes/shares/climers/Projects/CCIplus_Soil_Moisture/07_data/ESA_CCI_SM_v08.1_GAPFILLED/07_ts2img/2022/ESACCI-SOILMOISTURE-L3S-SSMV-COMBINED_GAPFILLED-20220122000000-fv08.1.nc")
    df = ds[['sm', 'gapmask']].isel(time=0).to_dataframe().drop(columns='time')
    plotter = MapPlotter(llc=(-30, 35), urc=(40, 70))

    plotter.add_colormesh_layer(df['sm'].dropna(), add_cbar=True, clim=(0, 0.5),
                                cbar_kwargs=dict(cb_label='SM (m3/m3)', cb_loc='left'))
    plotter.add_hatch_overlay(~df['gapmask'].dropna().astype(bool), pattern='.',
                              density=2)
    plotter.add_basemap('white', ocean=True, states=True, borders=True,
                        linewidth_mult=3)

    idx = np.random.choice(df.index, 1000)
    df = pd.Series(index=pd.MultiIndex.from_tuples(idx), data=True)

    plotter.add_scatter_layer(df, marker='.', s=50, cmap=plt.get_cmap('Greens'),
                              add_cbar=True, cbar_kwargs=dict(cb_label='SM (m3/m3)', cb_loc='right'))


    idx = np.random.choice(df.index, 1000)
    df = pd.Series(index=pd.MultiIndex.from_tuples(idx), data=True)

    plotter.add_scatter_overlay(df, marker='+', s=20)

    plotter.add_gridlines('0110', (60, 20))

    plotter.ax.set_title('Test')
    plotter.fig.savefig('test.png', dpi=300, bbox_inches='tight')
    """


