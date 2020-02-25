# -*- coding: utf-8 -*-

from collections import OrderedDict
import ogr
import os
import numpy as np
import pandas as pd
import ast

smecv52_5deg_cells = os.path.join(os.path.dirname(__file__), 'continents_grid_cells',
                                  'SMECV_v052_land_cells')

def read_cells_for_continent(continent, infile=smecv52_5deg_cells):
    """
    Read cells for passed continent(s) from a created text file.

    Parameters
    ----------
    continent : str or list
        One or multiple continents to read cells for.
    infile: str, optional (default: CCI v5.2 5 deg cells)
        Path to file to read

    Returns
    -------
    ret_cells : list
        Cells for the selected continent(s)
    """
    if isinstance(continent, str):
        continent = [continent]

    with open(infile, 'r') as f:
        s = f.read()
        cont_cells = ast.literal_eval(s)

    if len(continent) > 0:
        ret_cells = []
        for k in continent:
            if k not in cont_cells.keys():
                raise ValueError('{} not found in list, choose one of: {}'.format(
                    k, ', '.join(cont_cells.keys())))
            else:
                ret_cells += cont_cells[k]
    else:
        ret_cells = None

    return ret_cells

def create_cells_for_continents(grid, continents=None, out_file=None):
    """
    Create a list of cells for all continents. Optionally save it as txt file.

    Parameters
    ----------
    grid : pygeogrids.CellGrid
        Grid that is used to find the cell numbers
    contintinents : list, optional (default: None)
        Limit to these continents, if None is passed, all are used
    out_file : str, optional (default: None)
        If this path to a file is passed, the output is written there.

    Returns
    -------
    cont_cells : OrderedDict
        Cells per continent.
    """

    df = subgrid_for_polys(grid)
    cont_cells = dict()

    all_conts = np.sort(np.unique(df['continent'].values))

    if continents is None:
        continents = all_conts

    for continent in all_conts:
        if continent not in continents:
            continue
        print('--------------------------------------')
        print('Finding cells for {}'.format(continent))
        subgrid = subgrid_for_polys(grid, continent, silent=True)
        if subgrid is not None:
            cells = subgrid.get_cells()
        else:
            cells = np.array([])
        cont_cells[continent] = cells.tolist()

    if out_file is not None:
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