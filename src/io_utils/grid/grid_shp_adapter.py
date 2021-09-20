# -*- coding: utf-8 -*-

from collections import OrderedDict
try:
    import ogr
    import osr
except ImportError:
    from osgeo import ogr, osr
import os
import numpy as np
import pandas as pd
from pygeogrids.grids import CellGrid

class GridShpAdapter(object):
    def __init__(self, grid):
        self.grid = grid
        self.shp_reader = CountryShpReader()
        self.country_names = sorted(np.unique(self.shp_reader.df['country'].values))
        self.continent_names = sorted(np.unique(self.shp_reader.df['continent'].values))

    def __str__(self):
        county_names = ', '.join(self.country_names)
        continent_names = ', '.join(self.continent_names)
        return "Continent Names: {} \n \n Country Names: {}".format(
            continent_names, county_names)

    def create_subgrid(self, names, verbose=False):
        """
        Create a subgrid based on country names or continent names.

        Parameters
        ----------
        names : list
            List of countries and/or continents
        verbose : bool, optional (default: False)
            Show progress when creating subgrid

        Returns
        -------
        subgrid : pygeogrids.BasicGrid or pygeogrids.CellGrid
            Subgrid with gpis only for the selected countries/continents
        """

        gpis = np.array([], dtype=int)

        ids = []
        ids += self.shp_reader.country_ids(*names)
        ids += self.shp_reader.country_ids(*self.shp_reader.continent_countries(*names))

        ids = np.unique(np.array([ids]))

        for i, id in enumerate(ids):
            if verbose:
                print('Creating subset {} of {} ... to speed this up '
                      'improve pygeogrids.grids.get_shp_grid_points()'.format(i + 1, ids.size))

            subgrid = self.grid.get_shp_grid_points(self.shp_reader._geom(id))
            if subgrid is not None:
                poly_gpis = subgrid.activegpis
                gpis = np.append(gpis, poly_gpis)
            else:
                pass

        if gpis.size == 0:
            empty_arr = np.ndarray([])
            return CellGrid(lon=empty_arr, lat=empty_arr, cells=empty_arr)
        else:
            return self.grid.subgrid_from_gpis(np.unique(gpis))

    def create_cells_for_continents(self, continents=None, out_file=None):
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
        df = self.shp_reader.df
        cont_cells = dict()

        all_conts = np.sort(np.unique(df['continent'].values))

        if continents is None:
            continents = all_conts

        for continent in all_conts:
            if continent not in continents:
                continue
            print('--------------------------------------')
            print('Finding cells for {}'.format(continent))
            subgrid = self.create_subgrid([continent], verbose=True)
            if subgrid is not None:
                cells = subgrid.get_cells()
            else:
                cells = np.array([])
            cont_cells[continent] = cells.tolist()

        if out_file is not None:
            with open(out_file, 'w') as f:
                f.write(str(cont_cells))

        return cont_cells

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
            name = feature.GetField(self.name_field)
            cont = feature.GetField(self.continent_field)
            names.append(name)
            conts.append(cont)
            ids.append(n)

        self.df = pd.DataFrame(index=ids, data={'continent': conts, 'country': names})

    def _geom(self, id):
        shp = ogr.Open(self.path, 0)
        layer = shp.GetLayer()
        feature = layer.GetFeature(id)
        geom = feature.geometry().Clone()
        # sref = osr.SpatialReference()
        # sref = sref.ImportFromEPSG(4326)
        #geom = geom.AssignSpatialReference(sref)
        return geom

    def country_ids(self, *names):
        if isinstance(names, str):
            names = [names]
        ids = []
        for name in names:
            country_ids = self.df.loc[self.df.country == name].index.values
            for id in country_ids:
                ids.append(id)

        return ids

    def continent_countries(self, *continents):
        if isinstance(continents, str):
            continents = [continents]

        names = np.array([])
        for continent in continents:
            n = self.df.loc[self.df.continent == continent, 'country'].values
            names = np.append(names, n)

        return names
    
if __name__ == '__main__':

    country = 'Morocco'
    from smos.grid import EASE25CellGrid
    #from smecv_grid.grid import SMECV_Grid_v052
    grid = EASE25CellGrid()
    from pygeogrids.netcdf import save_grid
    adapter = GridShpAdapter(grid)
    print(adapter)
    grid = adapter.create_subgrid([country])
    save_grid(r"R:\Projects\SMART-DRI\07_data\sm_country_data\SMOS-IC\ease25grid_{country}.nc".format(country=country),
              grid=grid)