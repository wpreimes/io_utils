# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize
import numpy as np
import cartopy
import cartopy.crs as ccrs
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import pandas as pd
import matplotlib as mpl
from smecv_grid.grid import SMECV_Grid_v042
import matplotlib.ticker as ticker
import warnings
from io_utils.utils import safe_arange
import io_utils.plot.colormaps as my_colormaps


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
        warnings.warn('{} style is not supported.')

def is_spherical(projection):
    if projection in [ccrs.Robinson()]:
        return True
    else:
        return False

def add_grid_labels(ax, x0, x1, y0, y1, dx, dy,
                    lft=True, rgt=True, top=True, bot=True, spherical=False,
                    edgle_label_x=False, edge_label_y=True):
    """
    Add grid line labels manually for projections that aren't supported

    Parameters
    ----------
    ax (geoaxes.GeoAxesSubplot)
    x0 (scalar)
    x1 (scalar)
    y0 (scalar)
    y1 (scalar)
    dx (scalar)
    dy (scalar)
    lft (bool): whether to label the left side
    rgt (bool): whether to label the right side
    top (bool): whether to label the top side
    bot (bool): whether to label the bottom side
    spherical (bool): pad the labels better if a side of ax is spherical
    edgle_label_x (bool): Plot the first and last Lon label
    edge_label_y (bool): Plot the first and last Lat label
    """
    if dx <= 10:
        dtype = float
    else:
        dtype = int

    if dy <= 10:
        dtype = float
    else:
        dtype = int

    lons = np.arange(x0, x1 + dx / 2., dx, dtype=dtype)
    for i, lon in enumerate(lons):
        if not edgle_label_x:
            if i==0 or i==lons.size-1:
                continue
        if top:
            ax.text(lon, y1, '{0}$^\circ$\n\n'.format(lon),
                    va='center', ha='center',
                    transform=ccrs.PlateCarree(), fontsize=5)
        if bot:
            ax.text(lon, y0, '\n\n{0}$^\circ$'.format(lon),
                    va='center', ha='center',
                    transform=ccrs.PlateCarree(), fontsize=5)

    lats = np.arange(y0, y1 + dy / 2., dy, dtype=dtype)
    for i, lat in enumerate(lats):
        if not edge_label_y:
            if i==0 or i==lats.size-1:
                continue
        if spherical:
            if lat == 0:
                va = 'center'
            elif lat > 0:
                va = 'bottom'
            else:
                va = 'top'
        else:
            va = 'center'

        ax.text(x0, lat, '{0}$^\circ$  '.format(lat), va=va, ha='right',
                transform=ccrs.PlateCarree(), alpha=0. if not lft else 1.,
                fontsize=5)
        ax.text(x1, lat, '  {0}$^\circ$'.format(lat), va=va, ha='left',
                transform=ccrs.PlateCarree(), alpha=0. if not rgt else 1.,
                fontsize=5)


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

def map_add_grid(imax, projection, grid_loc, llc, urc, gridspace, draw_labels):
    """
    Add a grid to the map

    Parameters
    ----------
    imax : plt.Axes
    projection : ccrs.projection
    grid_loc : str
    llc : tuple
    urc : tuple
    gridspace : tuple
    draw_labels : bool

    Returns
    -------
    imax : plt.Axes
    """
    minx, maxx = np.round(llc[0]), np.round(urc[0])
    miny, maxy = np.round(llc[1]), np.round(urc[1])
    dx, dy = gridspace[0], gridspace[1]
    gl = imax.gridlines(crs=ccrs.PlateCarree(), draw_labels=False,
                        linewidth=0.5, color='black', alpha=0.15, linestyle='--')

    xlocs = np.arange(minx, maxx + dx, dx)
    ylocs = np.arange(miny, maxy + dy, dy)
    gl.xlocator = mticker.FixedLocator(xlocs)
    gl.ylocator = mticker.FixedLocator(ylocs)
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER

    if draw_labels:
        spher = is_spherical(projection)
        grid_kwargs = {p: True if g == '1' else False for p, g in zip(['top', 'rgt', 'bot', 'lft'], grid_loc)}
        add_grid_labels(imax, minx, maxx, miny, maxy, dx, dy,
                        spherical=spher, edgle_label_x=False,
                        edge_label_y=True if spher else False,
                        **grid_kwargs)

    return imax

def cp_scatter_map(lons, lats, values, projection=ccrs.Robinson(), title=None,
                   llc=(-179.9999, -60.), urc=(179.9999, 80), cbrange=(0,1),
                   cmap=plt.get_cmap('RdYlBu'), coastline_size='110m', veg_mask=False,
                   gridspace=(60,20), grid_label_loc='1001', style=None, markersize=None,
                   ocean=False, land='white', states=False, borders=False,
                   scale_factor=1., watermark=None, show_cbar=True, **cbar_kwargs):

    '''
    Plot data as scatterplot on a map

    Parameters
    ----------
    lons: np.array
        List of longitudes of the points to plot
    lats : np.array
        List of latitudes of the points to plot (must be same size as lats)
    values : np.array
        List of values to plot (must be same size as lats and lons)
    projection : ccrs.projection, optional (default: ccrs.Robinson())
        The cartopy projection for the map
    title: str, optional (default: None)
        Title for the map, if None is passed, no Title is created.
    llc : tuple, optional (default: (-179.9999, -60.))
        (lon, lat) : Coords of the lower left corner of the subset to plot
    urc : tuple, optional (default: (179.9999, 80.))
        (lon, lat) : Coords of the upper right corner of the subset to plot
    cbrange : tuple, optional (default: (0,1))
        (min, max) : The color range of values to plot
    cmap : mpl.colormap, optional (default: 'jet')
        A matplotlib colormap to use. You can also pass your own cmaps!
    coastline_size : str, optional (default: '110m')
        Size of the coastlines to plot with cartopy
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
        The plot figure
    imax : plt.axes
        The ax of the map that was created
    im : plt.axes
        The plot ax
    '''

    set_style(style)

    values = values * scale_factor
    f = plt.figure(num=None, figsize=(8, 4), facecolor='w', edgecolor='k')

    data_crs = ccrs.PlateCarree()

    imax = plt.axes(projection=projection)
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
    im = plt.scatter(lons, lats, c=values, cmap=cmap, s=markersize,
        vmin=cbrange[0], vmax=cbrange[1], edgecolors='black', linewidths=0.05,
                     zorder=3, transform=data_crs)

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
        imax.set_title(title, fontsize=10)
        #f.suptitle(title, fontsize=10)
    if watermark:
        # todo: add text to plot corner
        raise NotImplementedError
    if show_cbar:
        map_add_cbar(f, imax, im, **cbar_kwargs)
    else:
        plt.tight_layout(pad=3)



    return f, imax, im

def map_add_cbar(f, imax, im, cb_label=None, cb_loc='bottom', cb_ticksize=5,
                 cb_labelsize=7, cb_extend='both', cb_n_ticks=None, cb_ext_label_min=None,
                 cb_ext_label_max=None, cb_text=None):
    """
    Add a colorbar to the bottom of the map

    Parameters
    ----------
    f : plt.Figure
        The map figure
    imax : plt.Axes
        The cartopy axes
    im : plt.Axes
        The data Axes
    cb_label : str, optional (default: None)
        Label that is shown below the colorbar
    cb_loc : str, optional (default: bottom)
        Location of the colorbar (bottom , left, right, top)
    cb_labelsize : int, optional (default: 7)
        Size of the colorbar label in points.
    cb_extend : str, optional (default: Both)
        Which sides of the colorbar are shown as an arrow.
        One of: neither, both, max, min
        By default, both sides are arrows.
    cb_n_ticks : int, optional (default: None)
        Override the default number of colobar ticks and use this many ticks
        instead. If None is passed, let matplotlib decide.
    cb_ext_label_min : str, optional (default: None)
        Additional label for the left side of the colorbar
    cb_ext_label_max : str, optional (default: None)
        Additional label for the right if the colorbar
    cb_text : list, optional (default: None)
        Strings that are put below, next to the cbar with equal space
    """

    if not cb_ext_label_min and not cb_ext_label_max:
        exteme_labels = False
    else:
        exteme_labels = True

    cax, kw = mpl.colorbar.make_axes(imax, location=cb_loc,
                                     aspect=35 if cb_loc in ['top', 'bottom'] else 20,
                                     extend=cb_extend, shrink=0.7, use_gridspec=True,
                                     pad=0.07 if not exteme_labels else 0.08)

    cb = f.colorbar(im, cax=cax, **kw)
    cb.ax.tick_params(labelsize=cb_ticksize)
    if cb_n_ticks is not None:
        if cb_n_ticks == 0:
            cb.set_ticks([])
        else:
            tick_locator = ticker.MaxNLocator(nbins=cb_n_ticks)
            cb.locator = tick_locator
            cb.update_ticks()

    if exteme_labels:
        if cb_ext_label_min:
            if cb_loc in ['top', 'bottom']:
                cb.ax.text(0, 1.1, cb_ext_label_min, fontsize=5, rotation=0, ha='left',
                           transform=cax.transAxes)
            else:
                cb.ax.text(0.5, -0.06, cb_ext_label_min, fontsize=5, rotation=0, va='bottom',
                           ha='center', transform=cax.transAxes)
        if cb_ext_label_max:
            if cb_loc in ['top', 'bottom']:
                cb.ax.text(1, 1.1, cb_ext_label_max, fontsize=5, rotation=0, ha='right',
                           transform=cax.transAxes)
            else:
                cb.ax.text(0.5, 1.05, cb_ext_label_max, fontsize=5, rotation=0, va='top',
                           ha='center', transform=cax.transAxes)

    if cb_text is not None:
        hs = []
        vs = []
        if cb_loc in ['top', 'bottom']:
            off = (1. / len(cb_text)) / 2.
            for i, t in enumerate(cb_text):
                hs.append(i * (1. / len(cb_text)) + off)
            vs = [-0.8 if cb_loc == 'bottom' else 1.2] * len(cb_text)
        else:
            off = (1. / len(cb_text)) / 2.
            for i, t in enumerate(cb_text):
                vs.append(i * (1. / len(cb_text)) + off)
            hs = [1.2 if cb_loc == 'right' else -0.2] * len(cb_text)
        for i, (h,v) in enumerate(zip(hs, vs)):
            if cb_loc in ['top', 'bottom']:
                cb.ax.text(h, v, cb_text[i], fontsize=cb_ticksize, rotation=0,
                           transform=cax.transAxes, ha='center',
                           va='top' if cb_loc=='bottom' else 'bottom')
            else:
                cb.ax.text(h, v, cb_text[i], fontsize=cb_ticksize, rotation=0,
                           transform=cax.transAxes, va='center',
                           ha='left' if cb_loc == 'right' else 'right')


    cb.set_label(cb_label if cb_label is not None else '', fontsize=cb_labelsize,
                 labelpad=5, color='k')

def cp_map(df, col=None, mask_cols_colors=None, resxy=(0.25,0.25), offset=(0.5,0.5), projection=ccrs.Robinson(),
           title=None, title_size=10, llc=(-179.9999, -90.), urc=(179.9999, 90.), flip_ud=False,
           cbrange=(0,1), cmap=plt.get_cmap('RdYlBu'), coastline_size='110m',
           veg_mask=False, gridspace=(60,20), grid_label_loc='0011', style=None,
           ocean=False, land='grey', states=False, borders=False, scale_factor=1., watermark=None,
           show_cbar=True, ax=None, **cbar_kwargs):

    '''
    Plot data as an area on a map.

    Parameters
    ----------
    df : pd.Dataframe
        The DataFrame that contains the data to plot
        The index must either be a multiindex (with lat in the FIRST and lon in
        the SECOND index col) and sorted by lat or a list of ints, that are the
        GPIs of the data.
    col : str, optional (default: None)
        The column in df that contains the data to plot, not necessary if a
        Series is passed.
    mask_cols_colors : dict, Optional (default: None)
        Dictionary with mask columns in df as keys and colors as values
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
        (lon, lat) : Coords of the lower left corner of the subset to plot,
        or you can add a country name that we search in the country-bounding-boxes
        package (todo: add feature)
    urc : tuple, optional (default: (179.9999, 80.))
        (lon, lat) : Coords of the upper right corner of the subset to plot
        or you can add a country name that we search in the country-bounding-boxes
        package
    flip_ud : bool, optional (default: False)
        Force flipping the data upside down before plotting it.
    cbrange : tuple, optional (default: (0,1))
        (min, max) : The color range of values to plot
    cmap : mpl.colormap, optional (default: 'jet')
        A matplotlib colormap to use. You can also pass your own cmaps!
    coastline_size : str, optional (default: '110m')
        Size of the coastlines to plot with cartopy
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
        Add this text to the corner of the plot.
    show_cbar : bool, optional (default: True)
        Add visualization of the colorbar at the bottom
    poly_masks : dict, optional (default: None)
        shapes (keys) that are used and colors to fill them with or None as color
        to mask everything BUT the masked data.
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
        The plot figure
    imax : plt.axes
        The ax of the map that was created
    im : plt.axes
        The plot ax
    '''

    if mask_cols_colors is None:
        mask_cols_colors = dict()

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
    glob_df = pd.DataFrame(index=glob_index, data={'gpi': np.arange(glob_index.size)})

    if isinstance(df.index, pd.MultiIndex):
        s_lats, s_lons = df.index.get_level_values(0), df.index.get_level_values(1)

        index = pd.MultiIndex.from_arrays(
            np.array([s_lats, s_lons]), names=['lats', 'lons'])
        data = {mask: df[mask] for mask in mask_cols_colors.keys()}
        data.update({col: df[col]})
        df = pd.DataFrame(index=index, data=data)
        df['gpi'] = np.arange(df.index.size)
    else:
        glob_df = glob_df.set_index('gpi')

    for c in [col] + list(mask_cols_colors.keys()):
        glob_df[c] = df[c]

    df = data = None # clear memory

    layers = {}

    for layer_name in [col] + list(mask_cols_colors.keys()):

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
            colors = [mask_cols_colors[name], (1., 1., 1.)]  # dark green
            layer_cmap = LinearSegmentedColormap.from_list(name, colors, N=2)
        else:
            layer_cmap = cmap

        im = imax.pcolormesh(glob_lons, glob_lats, img_masked, cmap=layer_cmap, transform=data_crs,
                             rasterized=True)

    im.set_clim(vmin=cbrange[0], vmax=cbrange[1])

    # if veg_mask:
    #     if not resxy == (0.25, 0.25):
    #         raise ValueError(resxy, 'Vegetation mask only implemented for 0.25x0.25 grid')
    #     # Plot a dense vegetation mask as in the ESA CCI SM grid
    #     veg_gpis, veg_lons, veg_lats, _  = SMECV_Grid_v042('rainforest').get_grid_points()
    #     glob_df['veg_mask'] = np.nan
    #     if isinstance(glob_df.index, pd.MultiIndex):
    #         veg_index = pd.MultiIndex.from_arrays([veg_lats, veg_lons], names=['lat', 'lon'])
    #         glob_df.loc[veg_index, 'veg_mask'] = 1.
    #     else:
    #         glob_df.loc[glob_df.loc[veg_gpis].index, 'veg_mask'] = 1.
    #     img = np.empty(glob_df.index.size, dtype='float32')
    #     img.fill(np.nan)
    #     img[range(glob_df.index.size)] = glob_df['veg_mask'].values
    #     veg_img_masked = np.ma.masked_invalid(img.reshape((180 * 4, 360 * 4)))
    #
    #     colors = [(7. / 255., 79. / 255., 25. / 255.), (1., 1., 1.)]  # dark green
    #     vegcmap = LinearSegmentedColormap.from_list('Veg', colors, N=2)
    #
    #     imax.pcolormesh(glob_lons, glob_lats, veg_img_masked, cmap=vegcmap, transform=data_crs,
    #                     rasterized=True)

    imax.coastlines(resolution=coastline_size, color='black', linewidth=0.25)
    #imax.add_feature(cartopy.feature.LAND, color='white', zorder=0)

    if title:
        imax.set_title(title, fontsize=title_size)
        #f.suptitle(title, fontsize=10)

    if watermark:
        # todo: add text to plot corner
        raise NotImplementedError
    if show_cbar and f is not None:
        map_add_cbar(f, imax, im, **cbar_kwargs)
    else:
        plt.tight_layout(pad=3)


    return f, imax, im


if __name__ == '__main__':
    from io_utils.plot.colormaps import cm_sm, cm_reds
    from io_utils.plot.nc_var_plotters import NcVarPlotter
    from datetime import datetime
    import matplotlib.pyplot as plt
    import xarray as xr
    import numpy as np


    # file = r"R:\Datapool\C3S\01_raw\v201912\TCDR\060_dailyImages\combined\2019\C3S-SOILMOISTURE-L3S-SSMV-COMBINED-DAILY-20190621000000-TCDR-v201912.0.0.nc"
    # ds = xr.open_dataset(file)
    #
    # norm_unc = xr.DataArray(
    #     data=((ds.variables['sm_uncertainty'].values / ds.variables['sm'].values) * 100).astype(np.float32),
    #     dims=ds['sm'].dims,  # copy from any other data variable
    #     coords=ds.coords,
    #     attrs=dict(
    #         description="normalised uncertainty",
    #         valid_range=np.array([0,100]),
    #         units="perc.",
    #     ),
    # )
    #
    # new_ds = ds.assign(norm_unc=norm_unc)
    #
    newfile = r"R:\Projects\CCIplus_Soil_Moisture\07_data\ESA_CCI_SM_v06.1\060_daily_images\passive\2017\ESACCI-SOILMOISTURE-L3S-SSMV-PASSIVE-20170414000000-fv06.1.nc"
    #
    # new_ds.to_netcdf(newfile)

    cmap = plt.get_cmap('Reds')
    plotter = NcVarPlotter(newfile, out_dir=r'C:\Temp', cell_center_origin=True, z_var='time')
    plotter.plot_variable('sm',
                          cbrange=(0, 1), cb_loc='right', cb_extend='max',
                          cb_label='SM uncertainty (relative) [%]', cmap=cmap)


    # ds = xr.open_dataset(file)
    # cmap = plt.get_cmap('Reds')
    # plotter = NcVarPlotter(file, out_dir=r'C:\Temp', cell_center_origin=False, z_var='time')
    # plotter.plot_variable('norm_unc',
    #                       time='2019-06-21', cbrange=(0, 100), cb_loc='right', cb_extend='max',
    #                       cb_label='SM uncertainty (relative) [%]', cmap=cmap)
    #
    # from smecv_grid.grid import SMECV_Grid_v052
    # gpis, lons, lats,cells = SMECV_Grid_v052('land').get_grid_points()
    # data_py3 = pd.read_csv(
    #     r"\\project9\data-write\RADAR\ESA_CCI_SM\v06.0.0\python3_old_cov\050_errp_images\errp_combined_gapfilled.csv")
    # data_py3 = data_py3.set_index('gpi')
    #
    # data_py2 = pd.read_csv(
    #     r"\\project9\data-write\RADAR\ESA_CCI_SM\v06.0.0\python2\050_errp_images\errp_combined_gapfilled.csv")
    # data_py2 = data_py2.set_index('gpi')
    #
    # data_py3['snr_ascat_diff'] = data_py3['snr_ascat'] - data_py2['snr_ascat']
    #
    # #df = pd.DataFrame(index=[lons, lats], data={'gpi': gpis})
    # df = pd.DataFrame(index=gpis, data={'lons': lons, 'lats': lats})
    # df['snr_ascat_diff'] = data_py3['snr_ascat_diff']
    # df.set_index(['lons', 'lats'])
    # cp_map(df, 'snr_ascat_diff', cbrange=(-1,1))
    #
    # subplot_kw = {'projection': ccrs.Orthographic(-80, 35)}
    # fig, ax = plt.subplots(ncols=2, nrows=1, figsize=(10, 7),
    #                        subplot_kw={'projection': ccrs.Robinson()})
    # llc, urc = [(113.338953078, -43.6345972634), (153.569469029, -10.6681857235)]
    # cp_map(data, 'var', ax=ax[0], llc=llc, urc=urc)
    # cp_map(data, 'var', ax=ax[1], llc=llc, urc=urc)