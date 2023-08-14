# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import cartopy
import cartopy.crs as ccrs
import pandas as pd
from smecv_grid.grid import SMECV_Grid_v042
from warnings import warn

from io_utils.plot.misc import map_add_grid, map_add_cbar
from io_utils.utils import safe_arange

'''
Create a cartopy map from gridded or from pointed values.

Requires: matplotlib, numpy, cartopy, pandas
Optional: smecv_grid 
'''
# TODO # (+) Make the vegetation mask work for different resolutions as well
# (+) Make this a class instead
# Add function to draw markers/pointers

# NOTES # -


def set_style(style):
    if style is None:
        pass
    elif style == 'seaborn_poster':
        import seaborn as sns
        sns.set_context("poster", font_scale=1.)
        plt.style.use('seaborn-talk')
    else:
        warn('{} style is not supported.')


def map_add_pointer(f, imax, im, tip_loc, text_loc, pointer_label,
                    linewidth=2, fontsize=25):
    """

    Parameters
    ----------
    f
    imax
    im
    pointer_start : list of tuple
    pointer_end : list of tuple
    pointer_label : list of tuple
    linewidth
    fontsize

    Returns
    -------

    """
    transform = ccrs.PlateCarree()._as_mpl_transform(imax)
    for start, end, label in zip(tip_loc, text_loc, pointer_label):
        imax.annotate(label, xy=start, xytext=end,
                      arrowprops=dict(facecolor='black',
                                      arrowstyle="-",
                                      connectionstyle="arc3,rad=0",
                                      alpha=1., linewidth=linewidth),
                      xycoords=transform,
                      fontsize=fontsize,
                      fontweight='bold',
                      ha='center', va='center')

    return f, imax, im


def cp_scatter_map(lons, lats, values, projection=ccrs.Robinson(), title=None, title_size=10,
                   llc=(-179.9999, -60.), urc=(179.9999, 80), cbrange=(0, 1),
                   cmap=plt.get_cmap('RdYlBu'), coastline_size='110m', veg_mask=False,
                   gridspace=(60, 20), grid_label_loc='1001', style=None, markersize=None,
                   ocean=False, land='white', states=False, borders=False,
                   scale_factor=1., watermark=None, show_cbar=True, ax=None,
                   cb_kwargs=None, plot_kwargs=None):

    '''
    Plot data as scatterplot on a map

    Parameters
    ----------
    lons: np.array
        List of longitudes of the points to plotter
    lats : np.array
        List of latitudes of the points to plotter (must be same size as lats)
    values : np.array
        List of values to plotter (must be same size as lats and lons)
    projection : ccrs.projection, optional (default: ccrs.Robinson())
        The cartopy projection for the map
    title: str, optional (default: None)
        Title for the map, if None is passed, no Title is created.
    llc : tuple, optional (default: (-179.9999, -60.))
        (lon, lat) : Coords of the lower left corner of the subset to plotter
    urc : tuple, optional (default: (179.9999, 80.))
        (lon, lat) : Coords of the upper right corner of the subset to plotter
    cbrange : tuple, optional (default: (0,1))
        (min, max) : The color range of values to plotter
    cmap : mpl.colormap, optional (default: 'jet')
        A matplotlib colormap to use. You can also pass your own cmaps!
    coastline_size : str, optional (default: '110m')
        Size of the coastlines to plotter with cartopy
    veg_mask : bool, optional (default: False)
        Add the ESA CCI SM mask for dense vegetation to the dataset.
        This needs the smecv_grid package installed.
    gridspace : tuple or None, optional (default: (60,20))
        (dx, dy) : Spacing in the x (lon) and y (lat) direction
        If this is None, no grid is plotted
    grid_label_loc : str or None, optional (default: '0011')
        'top, right, bottom, left' : The 4 potential label elements (starting at
        the top), 1 means activated, 0 means deactivated.
        1111 to print all grids, 0011 to print the bottom and left grid etc.
        If this is None, no grid is plotted
    style: str, optional (default: None)
        Apply style backend.
        Current options: 'seaborn_poster', ...
    ocean : bool, optional (default: False)
        Fill water bodies with light blue color before plotting data.
    land : str or None, optional (default: 'grey')
        Fill land with this color before plotting data.
    states : bool, optional (default: False)
        Add state borders to the map (only interesting when plotting subsets)
    borders : bool, optional (default: False)
        Add country borders to the map (only interesting when plotting subsets)
    scale_factor : float (optional, default: 1.)
        A factor that the values are multiplied with before plotting them
    show_cbar : bool, optional (default: True)
        Add visualization of the colorbar at the bottom
    ax : matplotlib.Axes.ax
        Ax to use, if None is passed a new one is created.
    -------------------------
    Optional keywords that are passed when making the colorbar
    -------------------------
        cbtitle : str, optional (default: None)
            Title that is shown below the colorbar
        cblabelsize : int, optional (default: 7)
            Size of the colorbar label in points.
        extend : str, optional (default: 'both')
            Which sides of the colorbar are shown as an arrow.
            One of: neither, both, max, min
        n_ticks: int, optional (default: None)
            Override the default number of colobar ticks and use this many ticks
            instead. If None is passed, let matplotlib decide.
        ext_label_min : str, optional (default: None)
            Additional label for the min of the colorbar
        ext_label_max : str, optional (default: None)
            Additional label for the max if the colorbar

    Returns
    -------
    fig : plt.figure
        The plotter figure
    imax : plt.axes
        The ax of the map that was created
    im : plt.axes
        The plotter ax
    '''
    warn("`cp_scatter_map` is deprecated. Use io_utils.plot.map module instead",
         DeprecationWarning)

    if plot_kwargs is None:
        plot_kwargs = {}
    if cb_kwargs is None:
        cb_kwargs = {}

    set_style(style)

    values = values * scale_factor

    if ax is None:
        f = plt.figure(num=None, figsize=(8, 4), facecolor='w', edgecolor='k')
        imax = plt.axes(projection=projection)
    else:
        f = None
        imax = ax


    data_crs = ccrs.PlateCarree()

    imax.coastlines(resolution=coastline_size, color='black', linewidth=0.25)

    if ocean:
        imax.add_feature(cartopy.feature.OCEAN, zorder=0)
    if land:
        imax.add_feature(cartopy.feature.LAND, zorder=0, facecolor=land)
    if states:
        imax.add_feature(cartopy.feature.STATES, linewidth=0.05, zorder=2)
    if borders:
        imax.add_feature(cartopy.feature.BORDERS, linewidth=0.1, zorder=2)

    if llc is not None and urc is not None:
        imax.set_extent([llc[0], urc[0], llc[1], urc[1]], crs=data_crs)

    if gridspace is not None:
        if grid_label_loc is None:
            grid_label_loc = '0000'
        if grid_label_loc == '0000':
            draw_labels = False
        else:
            draw_labels = True
        imax = map_add_grid(imax, projection, grid_label_loc, llc, urc, gridspace,
                            draw_labels=draw_labels)

    lon_interval = max([llc[0], urc[0]]) - min([llc[0], urc[0]])
    markersize = 1.5 * (360 / lon_interval) if markersize is None else markersize
    if 'linewidths' not in plot_kwargs:
        plot_kwargs['linewidths'] = 0.05
    im = imax.scatter(lons, lats, c=values, cmap=cmap, s=markersize,
                      vmin=cbrange[0], vmax=cbrange[1], edgecolors='black',
                      zorder=3, transform=data_crs, **plot_kwargs)

    if veg_mask:
        # Plot a dense vegetation mask as in the ESA CCI SM grid
        df = pd.DataFrame(index=SMECV_Grid_v042(None).get_grid_points()[0],
                          data={'lons': SMECV_Grid_v042(None).get_grid_points()[1],
                                'lats': SMECV_Grid_v042(None).get_grid_points()[2]})
        veg_gpis = SMECV_Grid_v042('rainforest').get_grid_points()[0]
        df['veg_mask'] = np.nan
        df.loc[df.loc[veg_gpis].index, 'veg_mask'] = 1.
        img = np.empty(df.index.size, dtype='float32')
        img.fill(np.nan)
        img[df.index] = df['veg_mask'].values
        veg_img_masked = np.ma.masked_invalid(img.reshape((180 * 4, 360 * 4)))


        colors = [(7. / 255., 79. / 255., 25. / 255.), (1., 1., 1.)]  # dark greeb
        vegcmap = LinearSegmentedColormap.from_list('Veg', colors, N=2)

        imax.pcolormesh(df['lons'].values.reshape((180 * 4, 360 * 4)),
                        np.flipud(df['lats'].values.reshape((180 * 4, 360 * 4))),
                        veg_img_masked, cmap=vegcmap, transform=data_crs, rasterized=True)

    if title:
        imax.set_title(title, fontsize=title_size)

    if watermark:
        # todo: add text to plotter corner
        raise NotImplementedError
    if show_cbar:
        map_add_cbar(f, imax, im, **cb_kwargs)
    else:
        plt.tight_layout(pad=3)



    return f, imax, im


def cp_map(df, col=None, resxy=(0.25,0.25),
           offset=(0.5,0.5), projection=ccrs.Robinson(),
           title=None, title_size=10, llc=(-179.9999, -90.), urc=(179.9999, 90.), flip_ud=False,
           cbrange=(0, 1), cmap=plt.get_cmap('RdYlBu'), coastline_size='110m',
           gridspace=(60, 20), grid_label_loc='0011', style=None,
           ocean=False, land='grey', states=False, borders=False, scale_factor=1., watermark=None,
           show_cbar=True, ax=None, cb_kwargs=None, plot_kwargs=None):

    '''
    Plot data as an area on a map.

    Parameters
    ----------
    df : pd.Dataframe
        The DataFrame that contains the data to plotter
        The index must either be a multiindex (with lat in the FIRST and lon in
        the SECOND index col) and sorted by lat or a list of ints, that are the
        GPIs of the data.
    col : str, optional (default: None)
        The column in df that contains the data to plotter, not necessary if a
        Series is passed.
    resxy : tuple, optional (default: (0.25,0.25))
        Resolution if the grid that the passed data is on
        First arg in lon direction, second one in lat direction.
    offset : tuple, optional (default: (0.5,0.5))
        Offset to add to longitude and latitude regarding the origin of the pixel.
        (0.5, 0.5) means that the origin in in the pixel center
        (0,0) means that it is in the top left
        (1,1) means that it is in the bottom right etc.
    projection : ccrs.projection, optional (default: ccrs.Robinson())
        The projection of the map that is created
        Not all projections from https://scitools.org.uk/cartopy/docs/latest/crs/projections.html
        work properly yet, todo: improve that.
    title: str, optional (default: None)
        Title for the map.
    llc : tuple, optional (default: (-179.9999, -60.))
        (lon, lat) : Coords of the lower left corner of the subset to plotter,
        or you can add a country name that we search in the country-bounding-boxes
        package (todo: add feature)
    urc : tuple, optional (default: (179.9999, 80.))
        (lon, lat) : Coords of the upper right corner of the subset to plotter
        or you can add a country name that we search in the country-bounding-boxes
        package
    flip_ud : bool, optional (default: False)
        Force flipping the data upside down before plotting it.
    cbrange : tuple, optional (default: (0,1))
        (min, max) : The color range of values to plotter
    cmap : mpl.colormap, optional (default: 'jet')
        A matplotlib colormap to use. You can also pass your own cmaps!
    coastline_size : str, optional (default: '110m')
        Size of the coastlines to plotter with cartopy
    veg_mask : bool, optional (default: False)
        Add the ESA CCI SM mask for dense vegetation to the dataset
    gridspace : tuple or None, optional (default: (60,20))
        (dx, dy) : Spacing in the x (lon) and y (lat) direction
        Set this to None to not show a grid.
    grid_label_loc : str or None, optional (default: '0011')
        'top, right, bottom, left' : The 4 potential label elements (starting at
        the top), 1 means activated, 0 means deactivated.
        1111 to print all grids, 0011 to print the bottom and left grid etc.
    style: str, optional (default: 'seaborn_poster')
        Apply style backend.
        Current options: 'seaborn_poster', ...
    ocean : bool, optional (default: False)
        Fill water bodies with light blue color before plotting data.
    land : str or None, optional (default: 'grey')
        Fill land with this color before plotting data.
    states : bool, optional (default: False)
        Add state borders to the map (only interesting when plotting subsets)
    borders : bool, optional (default: False)
        Add country borders to the map (only interesting when plotting subsets)
    scale_factor : float (optional, default: 1.)
        A factor that the values are multiplied with before plotting them
    watermark : str, optional (default: None)
        Add this text to the corner of the plotter.
    show_cbar : bool, optional (default: True)
        Add visualization of the colorbar at the bottom
    ax : matplotlib.Axes.ax
        Ax to use, if None is passed a new one is created.
    -------------------------
    Optional keywords that are passed when making the colorbar
    -------------------------
    cblabel : str, optional (default: None)
        Title that is shown below the colorbar
    cblabelsize : int, optional (default: 7)
        Size of the colorbar label in points.
    cb_extend : str, optional (default: 'both')
        Which sides of the colorbar are shown as an arrow.
        One of: neither, both, max, min
    n_ticks: int, optional (default: None)
        Override the default number of colobar ticks and use this many ticks
        instead. If None is passed, let matplotlib decide.
    cb_ext_label_min : str, optional (default: None)
        Additional label for the min of the colorbar
    cb_ext_label_max : str, optional (default: None)
        Additional label for the max if the colorbar


    Returns
    -------
    fig : plt.figure
        The plotter figure
    imax : plt.axes
        The ax of the map that was created
    im : plt.axes
        The plotter ax
    '''

    warn("`cp_map` is deprecated. Use io_utils.plot.map module instead",
         DeprecationWarning)

    if plot_kwargs is None:
        plot_kwargs = {}
    if cb_kwargs is None:
        cb_kwargs = {}

    set_style(style)

    dy, dx = float(resxy[1]), float(resxy[0])
    offsetx, offsety = float(offset[0]), float(offset[1])
    for o in (offsetx, offsety):
        if (o > 1) or (o < 0):
            raise ValueError('Invalid offset, pass anything between 0 and 1')

    lon_start = -180
    lon_end = 180 - dx
    if offsetx != 0:
        lon_start += dx * offsetx
        lon_end += dx * offsetx
    glob_lons = safe_arange(lon_start, lon_end, dx)
    n_lons = glob_lons.size

    lat_start = -90
    lat_end = 90 - dy
    if offsety != 0:
        lat_start += dy * offsety
        lat_end += dy * offsety
    glob_lats = safe_arange(lat_start, lat_end, dy)
    n_lats = glob_lats.size

    glob_lons, glob_lats = np.meshgrid(glob_lons, glob_lats)

    glob_index = pd.MultiIndex.from_arrays(np.array([glob_lats.flatten(),
                                                     glob_lons.flatten()]),
                                           names=['lats', 'lons'])
    glob_df = pd.DataFrame(index=glob_index,
                           data={'gpi': np.arange(glob_index.size)})

    if isinstance(df.index, pd.MultiIndex):
        s_lats, s_lons = df.index.get_level_values(0), df.index.get_level_values(1)

        index = pd.MultiIndex.from_arrays(
            np.array([s_lats, s_lons]), names=['lats', 'lons'])
        data = {}
        data[col] = df[col]
        df = pd.DataFrame(index=index, data=data)
        df['gpi'] = np.arange(df.index.size)
    else:
        glob_df = glob_df.set_index('gpi')

    for c in [col]:
        glob_df[c] = df[c]

    df = data = None # clear memory

    layers = {}

    for layer_name in [col]:

        img = np.empty(glob_df.index.size, dtype='float32')
        img.fill(np.nan)
        index = np.array(range(glob_df.shape[0]))
        if layer_name == col:
            img[index] = glob_df[col].values * scale_factor

        img_masked = np.ma.masked_invalid(img.reshape(n_lats, n_lons))
        if flip_ud:
            img_masked = np.flipud(img_masked)

        layers[layer_name] = img_masked


    data_crs = ccrs.PlateCarree()
    if ax is None:
        f = plt.figure(num=None, figsize=(8, 4), facecolor='w', edgecolor='k')
        imax = plt.axes(projection=projection)
    else:
        f=None
        imax = ax

    if ocean:
        imax.add_feature(cartopy.feature.OCEAN, zorder=0)
    if land is not None:
        imax.add_feature(cartopy.feature.LAND, zorder=0, facecolor=land)
    if states:
        imax.add_feature(cartopy.feature.STATES, linewidth=0.05, zorder=2)
    if borders:
        imax.add_feature(cartopy.feature.BORDERS, linewidth=0.1, zorder=2)

    if gridspace is not None:
        if grid_label_loc is None:
            grid_label_loc = '0000'
        if grid_label_loc == '0000':
            draw_labels = False
        else:
            draw_labels = True
        imax = map_add_grid(imax, projection, grid_label_loc, llc, urc, gridspace,
                            draw_labels=draw_labels)


    if llc is not None and urc is not None:
        imax.set_extent([llc[0], urc[0], llc[1], urc[1]], crs=data_crs)

    for name, img_masked in layers.items():
        if name != col:
            pass
        else:
            layer_cmap = cmap

        im = imax.pcolormesh(glob_lons, glob_lats, img_masked,
                             cmap=layer_cmap, transform=data_crs,
                             rasterized=True, **plot_kwargs)

    im.set_clim(vmin=cbrange[0], vmax=cbrange[1])

    imax.coastlines(resolution=coastline_size, color='black', linewidth=0.25)
    #imax.add_feature(cartopy.feature.LAND, color='white', zorder=0)

    if title:
        imax.set_title(title, fontsize=title_size)
        #f.suptitle(title, fontsize=10)

    if watermark:
        # todo: add text to plotter corner
        raise NotImplementedError
    if show_cbar and f is not None:
        map_add_cbar(f, imax, im, **cb_kwargs)
    else:
        plt.tight_layout(pad=3)


    return f, imax, im
