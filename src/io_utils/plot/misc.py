import matplotlib as mpl
import numpy as np
from cartopy import crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from matplotlib import ticker as mticker, pyplot as plt, ticker as ticker
from pygeogrids.grids import gridfromdims

from io_utils.utils import safe_arange


def is_spherical(projection):
    if projection in [ccrs.Robinson()]:
        return True
    else:
        return False


def add_grid_labels(ax, x0, x1, y0, y1, dx, dy,
                    lft=True, rgt=True, top=True, bot=True, spherical=False,
                    edgle_label_x=False, edge_label_y=True, fontsize=5):
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
    fontsize (int): Fontsize of the labels
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
                    transform=ccrs.PlateCarree(), fontsize=fontsize)
        if bot:
            ax.text(lon, y0, '\n\n{0}$^\circ$'.format(lon),
                    va='center', ha='center',
                    transform=ccrs.PlateCarree(), fontsize=fontsize)

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
                fontsize=fontsize)
        ax.text(x1, lat, '  {0}$^\circ$'.format(lat), va=va, ha='left',
                transform=ccrs.PlateCarree(), alpha=0. if not rgt else 1.,
                fontsize=fontsize)


def map_add_grid(imax, projection, grid_loc, llc, urc, gridspace,
                 draw_labels, fontsize=5):
    """
    Add a grid to the map

    Parameters
    ----------
    imax : plt.Axes
        Image ax
    projection : ccrs.projection
        Projection of the map
    grid_loc : str
        Location of the grid lines.
        first digit = upper, second digit = right, third digit = lower,
        fourth digit = left
    llc : tuple
        Lower left corner of the map
    urc : tuple
        Upper right corner of the map
    gridspace : tuple
        Spacing of the grid in x and y direction
    draw_labels : bool
        Whether to draw the labels or not
    fontsize : int, optional
        Fontsize of the labels

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
        grid_kwargs['fontsize'] = fontsize
        add_grid_labels(imax, minx, maxx, miny, maxy, dx, dy,
                        spherical=spher, edgle_label_x=False,
                        edge_label_y=True if spher else False,
                        **grid_kwargs)

    return imax


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

    if f:
        cb = f.colorbar(im, cax=cax, **kw)
    else:
        cb = plt.colorbar(im, cax=cax, **kw)
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


def meshgrid(lons, lats):
    """
    Generate a grid from the given lons and lats with the given resolution.

    Parameters
    ----------
    lons: np.ndarray
        1D array of longitudes
    lats: np.ndarray
        1D array of latitudes

    Returns
    -------
    grid: pygeogrids.grids.BasicGrid
        Grid object, global with 2d shape
    """
    dx = np.nanmin(np.diff(np.sort(np.unique(lons))))
    dy = np.nanmin(np.diff(np.sort(np.unique(lats))))

    xmin, xmax = np.nanmin(lons), np.nanmax(lons)
    ymin, ymax = np.nanmin(lats), np.nanmax(lats)

    xdim = safe_arange(xmin, xmax + dx, dx)
    ydim = safe_arange(ymin, ymax + dy, dy)

    return gridfromdims(np.sort(xdim), np.sort(ydim), origin='bottom')
