# -*- coding: utf-8 -*-

from collections import OrderedDict
import ogr
import os
import numpy as np
import pandas as pd
import ast

def read_cells_for_continent(infile, *continents):
    """
    Read cells for passed continent(s) from a created text file.

    Parameters
    ----------
    infile: str
        Path to file to read
    continents : str
        One or multiple continents to read cells for.

    Returns
    -------
    cont_cells : OrderedDict
        Cells for the selected continent(s)
    """

    with open(infile, 'r') as f:
        s = f.read()
        cont_cells = ast.literal_eval(s)

    if len(continents) > 0:
        cont_cells = {k : cont_cells[k] for k in continents}

    return cont_cells

def create_cells_for_continents(grid, out_file=None):
    """
    Create a list of cells for all continents. Optionally save it as txt file.

    Parameters
    ----------
    grid : pygeogrids.CellGrid
        Grid that is used to find the cell numbers
    out_file : str, optional (default: None)
        If this path to a file is passed, the output is written there.

    Returns
    -------
    cont_cells : OrderedDict
        Cells per continent.
    """
    df = subgrid_for_polys(grid)
    cont_cells = dict()

    for continent in np.sort(np.unique(df['continent'].values)):
        print('--------------------------------------')
        print('Finding cells for {}'.format(continent))
        subgrid = subgrid_for_polys(grid, continent, silent=True)
        if subgrid is not None:
            cells = subgrid.get_cells()
        else:
            cells = np.array([])
        cont_cells[continent] = cells.tolist()

    if out_file:
        with open(out_file, 'w') as f:
            f.write(str(cont_cells))

    return cont_cells

def subgrid_for_polys(grid, *names, silent=False):
    """
    Create a subgrid that contains only points that are within the passed
    polygons.

    Parameters
    ----------
    grid : pygeogrids.CellGrid
        Input grid to subset, if no names are passed, print a list of options
    silent : bool, optional (default: False)
        Suppress printing progress
    names : str
        To see the options just pass nothing here

    Returns
    ---------
    subgrid : pygeogrids.CellGrid | pd.DataFrame
        Subgrid that contains only points that are withing the shapes of the passed
        countries and/or continents.
    """
    shp_reader = CountryShpReader()

    if len(names) == 0:
        print('Please pass country/continent names from:')
        print(shp_reader.df)
        return shp_reader.df

    gpis = np.array([], dtype=int)

    ids = []
    ids += shp_reader.country_ids(*names)
    ids += shp_reader.country_ids(*shp_reader.continent_countries(*names))

    ids = np.unique(np.array([ids]))

    for i, id in enumerate(ids):
        if not silent:
            print('Creating subset {} of {} ... to speed this up '
                  'improve pygeogrids.grids.get_shp_grid_points()'.format(i+1, ids.size))

        subgrid = grid.get_shp_grid_points(shp_reader._geom(id))
        if subgrid is not None:
            poly_gpis = subgrid.activegpis
            gpis = np.append(gpis, poly_gpis)
        else:
            pass

    if gpis.size == 0:
        return None
    else:
        return grid.subgrid_from_gpis(np.unique(gpis))


class CountryShpReader(object):

    def __init__(self, name_field="NAME", continent_field="CONTINENT"):

        self.name_field = name_field
        self.continent_field = continent_field

        self.path = os.path.join(os.path.dirname(__file__),
                            'countries_shp', 'ne_110m_admin_0_countries.shp')
        self._build()

    def _build(self):
        shp = ogr.Open(self.path, 0)
        layer = shp.GetLayer()
        n_features = layer.GetFeatureCount()

        names, conts, ids = [], [], []

        for n in range(n_features):
            feature = layer.GetFeature(n)
            names.append(feature.GetField(self.name_field))
            conts.append(feature.GetField(self.continent_field))
            ids.append(n)

        self.df = pd.DataFrame(index=ids, data={'continent': conts, 'name': names})

    def _geom(self, id):
        shp = ogr.Open(self.path, 0)
        layer = shp.GetLayer()
        feature = layer.GetFeature(id)
        geom = feature.geometry().Clone()
        return geom

    def country_ids(self, *names):
        if isinstance(names, str):
            names = [names]
        ids = []
        for name in names:
            country_ids = self.df.loc[self.df.name == name].index.values
            for id in country_ids:
                ids.append(id)

        return ids

    def continent_countries(self, *continents):
        if isinstance(continents, str):
            continents = [continents]

        names = np.array([])
        for continent in continents:
            n = self.df.loc[self.df.continent == continent, 'name'].values
            names = np.append(names, n)

        return names

cells_lut = OrderedDict([
 ('AUS', [2247,2319,2283,2246,2318,2282,2210,2174,2354,2353,2245,2137,2209,2317,
          2281,2173,2389,2208,2100,2172,2280,2244,2136,2352,2388,2316,2207,2315,
          2135,2279,2243,2171,2387,2351,2314,2350,2278,2349,2101,2211,2313,2386,2355]),
 ('CONUS',[283,355,391,420,421,422,423,424,426,427,455,456,457,458,
           459,462,463,490,491,492,493,494,495,497,525,526,527,528,
           529,530,531,534,561,562,563,564,565,566,567,573,597,598,599,
           600,601,602,603,607,632,633,634,635,636,637,638,639,643,669,
           670,671,672,673,674,675,679,707,708,709,710,711,744,745,746,
           750,753,754,781,782,783,787,790,818,819,855]),
 ('EU', []),
 ('SA', []),
 ('NA', []),
 ('AFR', [])])