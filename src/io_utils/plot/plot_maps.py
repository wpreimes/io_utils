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


'''
Create a cartopy map from gridded or from pointed values.

Requires: matplotlib, numpy, cartopy, pandas
Optional: smecv_grid 
'''
# TODO # (+) Make the vegetation mask work for different resolutions as well
       # (+) Make this a class instead
       # Add function to draw markers/pointers

# NOTES # -


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
                    transform=ccrs.PlateCarree())
        if bot:
            ax.text(lon, y0, '\n\n{0}$^\circ$'.format(lon),
                    va='center', ha='center',
                    transform=ccrs.PlateCarree())

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
                transform=ccrs.PlateCarree(), alpha=0. if not lft else 1.)
        ax.text(x1, lat, '  {0}$^\circ$'.format(lat), va=va, ha='left',
                transform=ccrs.PlateCarree(), alpha=0. if not rgt else 1.)


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

def map_add_cbar(f, imax, im, cblabel=None, cblabelsize=7, extend='both',
                 n_ticks=None, ext_label_min=None, ext_label_max=None):
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
    cblabel : str, optional (default: None)
        Label that is shown below the colorbar
    cblabelsize : int, optional (default: 7)
        Size of the colorbar label in points.
    extend : str, optional (default: Both)
        Which sides of the colorbar are shown as an arrow.
        One of: neither, both, max, min
        By default, both sides are arrows.
    n_ticks : int, optional (default: None)
        Override the default number of colobar ticks and use this many ticks
        instead. If None is passed, let matplotlib decide.
    ext_label_min : str, optional (default: None)
        Additional label for the left side of the colorbar
    ext_label_max : str, optional (default: None)
        Additional label for the right if the colorbar
    """

    if not ext_label_min and not ext_label_max:
        exteme_labels = False
    else:
        exteme_labels = True

    cax, kw = mpl.colorbar.make_axes(imax, location='bottom',
        extend=extend, shrink=0.7,
        pad=0.07 if not exteme_labels else 0.08)

    cb = f.colorbar(im, cax=cax, **kw)
    cb.ax.tick_params(labelsize=7)
    if n_ticks:
        tick_locator = ticker.MaxNLocator(nbins=n_ticks)
        cb.locator = tick_locator
        cb.update_ticks()

    if exteme_labels:
        if ext_label_min:
            cb.ax.text(0, 1.1, ext_label_min , fontsize=5, rotation=0, ha='left',
                       transform = cax.transAxes)
        if ext_label_max:
            cb.ax.text(1, 1.1, ext_label_max , fontsize=5, rotation=0, ha='right',
                       transform=cax.transAxes)

    cb.set_label(cblabel if cblabel is not None else '', fontsize=cblabelsize,
                 labelpad=5, color='k')


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
                        linewidth=1, color='black', alpha=0.2, linestyle='--')

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
                   gridspace=(60,20), grid_label_loc='1001', style=None,
                   ocean=False, land='white', states=False, borders=False,
                   scale_factor=1., show_cbar=True, **cbar_kwargs):

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
    if style is None:
        pass
    elif style == 'seaborn_poster':
        import seaborn as sns
        sns.set_context("poster", font_scale=1.)
        plt.style.use('seaborn-talk')
    else:
        warnings.warn('{} style is not supported.')

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
    markersize = 1.5 * (360 / lon_interval)
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
        f.suptitle(title, fontsize=10)

    if show_cbar:
        map_add_cbar(f, imax, im, **cbar_kwargs)
    else:
        plt.tight_layout(pad=3)

    return f, imax, im

def cp_map(df, col=None, resxy=(0.25,0.25), offset=(0.5,0.5), projection=ccrs.Robinson(),
           title=None, llc=(-179.9999, -60.), urc=(179.9999, 80), flip_ud=False,
           cbrange=(0,1), cmap=plt.get_cmap('RdYlBu'), coastline_size='110m',
           veg_mask=False, gridspace=(60,20), grid_label_loc='1001', style=None, ocean=False,
           land='grey', states=False, borders=False, scale_factor=1., watermark=None,
           show_cbar=True, **cbar_kwargs):

    '''
    Plot data as an area on a map.

    Parameters
    ----------
    df : pd.Dataframe or pd.Series
        The DataFrame that contains the data to plot
        The index must either be a multiindex (with lat in the FIRST and lon in
        the SECOND index col) and sorted by lat or a list of ints, that are the
        GPIs of the data.
    col : str, optional (default: None)
        The column in df that contains the data to plot, not necessary if a
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
    title: str, optional (default: None)
        Title for the map.
    llc : tuple, optional (default: (-179.9999, -60.))
        (lon, lat) : Coords of the lower left corner of the subset to plot
    urc : tuple, optional (default: (179.9999, 80.))
        (lon, lat) : Coords of the upper right corner of the subset to plot
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
    watermark : str, optional (default: None)
        Add this text to the corner of the plot.
    show_cbar : bool, optional (default: True)
        Add visualization of the colorbar at the bottom
    -------------------------
    Optional keywords that are passed when making the colorbar
    -------------------------
        cblabel : str, optional (default: None)
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
    if style is None:
        pass
    elif style == 'seaborn_poster':
        import seaborn as sns
        sns.set_context("poster", font_scale=1.)
        plt.style.use('seaborn-talk')
    else:
        warnings.warn('{} style is not supported.')

    if isinstance(df, pd.Series):
        dat = df
    else:
        dat = df[col]

    dy, dx = float(resxy[1]), float(resxy[0])
    offsetx, offsety = float(offset[0]), float(offset[1])

    glob_lons = (np.arange(360 * int(1. / dx)) * dx) - (180. - (dx * offsetx))
    glob_lats = (np.arange(180 * int(1. / dy)) * dy) - (90. - (dy * offsety))

    glob_lons, glob_lats = np.meshgrid(glob_lons, glob_lats)

    glob_index = pd.MultiIndex.from_arrays(np.array([glob_lats.flatten(),
                                                     glob_lons.flatten()]),
                                           names=['lats', 'lons'])
    glob_df = pd.DataFrame(index=glob_index, data={'gpi': np.arange(glob_index.size)})

    if isinstance(df.index, pd.MultiIndex):
        s_lats, s_lons = df.index.get_level_values(0), df.index.get_level_values(1)

        index =pd.MultiIndex.from_arrays(
            np.array([s_lats, s_lons]), names=['lats', 'lons'])
        df = pd.DataFrame(index=index, data={'dat': dat})
        df['gpi'] = np.arange(df.index.size)
    else:
        df = dat.to_frame('dat')
        glob_df = glob_df.set_index('gpi')

    glob_df['dat'] = df['dat']
    df = None # clear memory
    dat = None

    img = np.empty(glob_df.index.size, dtype='float32')
    img.fill(np.nan)
    index = np.array(range(glob_df.shape[0]))
    img[index] = glob_df['dat'].values * scale_factor
    img_masked = np.ma.masked_invalid(img.reshape(180 * int(1. / dy),
                                                  360 * int(1. / dx)))

    if flip_ud:
        img_masked = np.flipud(img_masked)

    f = plt.figure(num=None, figsize=(8, 4), facecolor='w', edgecolor='k')

    data_crs = ccrs.PlateCarree()

    imax = plt.axes(projection=projection)

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


    im = imax.pcolormesh(glob_lons, glob_lats, img_masked, cmap=cmap, transform=data_crs,
                         rasterized=True)

    im.set_clim(vmin=cbrange[0], vmax=cbrange[1])

    if veg_mask:
        if not resxy == (0.25, 0.25):
            raise ValueError(resxy, 'Vegetation mask only implemented for 0.25x0.25 grid')
        # Plot a dense vegetation mask as in the ESA CCI SM grid
        veg_gpis, veg_lons, veg_lats, _  = SMECV_Grid_v042('rainforest').get_grid_points()
        glob_df['veg_mask'] = np.nan
        if isinstance(glob_df.index, pd.MultiIndex):
            veg_index = pd.MultiIndex.from_arrays([veg_lats, veg_lons], names=['lat', 'lon'])
            glob_df.loc[veg_index, 'veg_mask'] = 1.
        else:
            glob_df.loc[glob_df.loc[veg_gpis].index, 'veg_mask'] = 1.
        img = np.empty(glob_df.index.size, dtype='float32')
        img.fill(np.nan)
        img[range(glob_df.index.size)] = glob_df['veg_mask'].values
        veg_img_masked = np.ma.masked_invalid(img.reshape((180 * 4, 360 * 4)))

        colors = [(7. / 255., 79. / 255., 25. / 255.), (1., 1., 1.)]  # dark green
        vegcmap = LinearSegmentedColormap.from_list('Veg', colors, N=2)

        imax.pcolormesh(glob_lons, glob_lats, veg_img_masked, cmap=vegcmap, transform=data_crs,
                        rasterized=True)

    imax.coastlines(resolution=coastline_size, color='black', linewidth=0.25)
    #imax.add_feature(cartopy.feature.LAND, color='white', zorder=0)

    if title:
        f.suptitle(title, fontsize=10)

    if watermark:
        imax.text()
    if show_cbar:
        map_add_cbar(f, imax, im, **cbar_kwargs)
    else:
        plt.tight_layout(pad=3)


    return f, imax, im



def usecase_scatter():
    lons = np.linspace(-160, 160, 160)
    lats = np.linspace(90, -90, 160)
    values = np.random.rand(160)

    f, imax, im = cp_scatter_map(lons, lats, values)

    f.savefig(r'C:\Temp\test.png', dpi=200)


def usecase_area_multiindex():
    lons = np.linspace(-20, 20, 41)
    lats = np.linspace(20, -20, 41).transpose()

    lons, lats = np.meshgrid(lons, lats)

    # multiindex: lats, lons
    index =pd.MultiIndex.from_arrays(np.array([lats.flatten(), lons.flatten()]),
                                     names=['lats', 'lons'])
    df = pd.DataFrame(index=index)
    df['data'] = np.random.rand(df.index.size)
    cp_map(df, 'data', resxy=(1,1), offset=(0,0))

def usecase_area_gpi():

    gpis = np.arange(346859, 374200)

    df = pd.DataFrame(index=gpis)
    df['data'] = np.random.rand(df.index.size)
    cp_map(df, 'data', resxy=(0.25,0.25))

def usecase_real_data():
    from netCDF4 import Dataset
    data_path = r"X:\staff\wpreimes\GLOBAL_basic_validation_full_period.nc"
    ds = Dataset(data_path)
    data = ds.variables['n_obs'][:].filled()
    lons = ds.variables['lon'][:]
    lats = ds.variables['lat'][:]

    lons, lats = np.meshgrid(lons, lats)

    # order matters [lat, lon]!!
    index =pd.MultiIndex.from_arrays(np.array([lats.flatten(), lons.flatten()]),
                                     names=['lats','lons'])
    df = pd.DataFrame(index=index).sort_index()
    df['n_obs'] = data.flatten()

    cp_map(df, 'n_obs', resxy=(0.25,0.25), cbrange=(0,5000), veg_mask=True)

def usecase_sara_data():
    from cartopy.io.shapereader import Reader
    from cartopy.feature import ShapelyFeature

    data_path = r"C:\Temp\sara\csv\output.csv"
    df = pd.read_csv(data_path, parse_dates=True, index_col=0)
    lons, lats = df['lon'].values, df['lat'].values
    # make a multiindex from the lat and lon columns of your data
    index =pd.MultiIndex.from_arrays(np.array([lats.flatten(), lons.flatten()]),
                                     names=['lats', 'lons'])
    df.index = index
    df = df.drop(columns=['lat', 'lon']) # drop the old data (copied as the index now)

    f, imax, im = cp_map(df, 'slp_combined', resxy=(0.25,0.25), cbrange=(-0.0004,0.0004), veg_mask=False,
           projection=ccrs.PlateCarree(), title='Plot Title', ocean=False, land=None,
           gridspace=(60,20), states=False, borders=False, llc=(45.,25.),  urc=(60.,40.),
            cblabel='slp_combined', cblabelsize=10,
           extend='both', ext_label_min=None, ext_label_max=None)
    # first argument is the data frame, second is the column in the df to plot
    # third is the resolution of your data, llc is the lower left corner of you
    # subplot (lon, lat) and urc the upper right corner.

    shape_file = r"X:\guests\sazadi\csv\ZayandehRud\transformed\transformed_transparent.shp"

    shape_feature = ShapelyFeature(Reader(shape_file).geometries(),
                                   ccrs.PlateCarree(), edgecolor='black',
                                   facecolor="none")
    imax.add_feature(shape_feature, facecolor="none", alpha=.8)


def usecase_adam():
    from netCDF4 import Dataset
    from smecv_grid.grid import SMECV_Grid_v052

    image = r"R:\Datapool_processed\ESA_CCI_SM\ESA_CCI_SM_v04.7\060_daily_images\combined\2019\ESACCI-SOILMOISTURE-L3S-SSMV-COMBINED-20190416000000-fv04.7.nc"
    ds = Dataset(image)
    dat = ds.variables['sm'][:]
    dat = dat.filled(np.nan).flatten()
    _, resampled_lons, resampled_lats, _  = SMECV_Grid_v052(None).get_grid_points()

    index =pd.MultiIndex.from_arrays(np.array([resampled_lats, resampled_lons]),
                                     names=['lats', 'lons'])
    df = pd.DataFrame(index=index, data={'sm': dat})


    f, imax, im = cp_map(df, 'sm', resxy=(0.25,0.25), cbrange=(0,0.5), veg_mask=False,
           projection=ccrs.Robinson(), title='testtitle', ocean=False, land='white',
           gridspace=None, states=False, borders=True,  llc=(-179.9999, -90.), urc=(179.9999, 90),
            cblabel='ESA CCI SM [$m^3/m^3$]', cblabelsize=10, grid_label_loc='0000', coastline_size='110m',
           extend='both', ext_label_min='MIN', ext_label_max='MAX')

    f.savefig(r'C:\Temp\test.png', dpi=200)

if __name__ == '__main__':
    usecase_adam()
    #usecase_sara_data()
    #usecase_real_data()
    #usecase_area_gpi()
    #usecase_area_multiindex()
    #usecase_scatter()