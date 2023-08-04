# -*- coding: utf-8 -*-

from collections import OrderedDict
try:
    try:
        import ogr
        import osr
    except (ImportError, ModuleNotFoundError):
        from osgeo import ogr, osr
except ImportError:
    raise ImportError('Could not import ogr/osr, please install `gdal` with conda.')
import os
import numpy as np
import pandas as pd
from pygeogrids.grids import CellGrid
from typing import Union, List, Optional
from io_utils.utils import deprecated

path_shp_countries = os.path.join(
    os.path.dirname(__file__), 'countries_shp', 'ne_110m_admin_0_countries.shp')

@deprecated("Use get_shp_grid_points function")
class GridShpAdapter(object):
    def __init__(self, grid):
        self.grid = grid
        self.shp_reader = CountryShpReader()
        self.country_names = sorted(np.unique(self.shp_reader.features['NAME'].values))
        self.continent_names = sorted(np.unique(self.shp_reader.features['CONTINENT'].values))

    def __repr__(self):
        s = (
            f"Continent Names: \n"
            f"{self.continent_names} \n"
            f"Country Names: \n"
            f"{self.country_names}"
        )
        return s

    def create_subgrid(self, names, verbose=False):
        """
        Create a subgrid based on country names or continent names.

        Parameters
        ----------
        names : list[str]
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
        ids += self.shp_reader.country_ids(*names).tolist()
        ids += self.shp_reader.country_ids(*self.shp_reader.continent_ids(names)).tolist()

        ids = np.unique(np.array([ids]))

        for i, id in enumerate(ids):
            if verbose:
                print('Creating subset {} of {} ... to speed this up '
                      'improve pygeogrids.grids.get_shp_grid_points()'.format(i + 1, ids.size))

            subgrid = self.grid.get_shp_grid_points(self.shp_reader.geom(id))
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
        df = self.shp_reader.features
        cont_cells = dict()

        all_conts = np.sort(np.unique(df['CONTINENT'].values))

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

class ShpReader:
    """
    Wrapper around gdal to read geometries with chosen name from passed
    shapefile field. Shapefiles with more features and many feature columns
    are smaller than fewer features / columns.
    If you know the column where you look for a values, pass it as the `field`,
    this will also speed up the search.
    """
    def __init__(
            self,
            shp_path: str,
            fields: Optional[Union[list, str]] = None,
            driver: str = 'ESRI Shapefile'
        ):
        """
        Read shp-file and create feature table
        
        Parameters
        ----------
        shp_path: str
            Path to shapefile
        fields: list[str], str or None
            Shapefile fields to read from attribute table. If None is passed,
            all fields are read.
        driver: str, optional
            Driver to use for reading shapefile. Default is ESRI Shapefile.
        
        Attributes
        ----------
        features: pd.DataFrame
            Feature table where each row is a polygon in the shp file and
            each column represents a field. Fields contain attributes used
            to filter out the relevant polygons.
        """
        self.shp_path = shp_path
        self.driver = driver
        self._init_open_shp()

        self.fields = None if fields is None else np.atleast_1d(fields)
        all_fields = [field.name for field in self.layer.schema]

        if self.fields is None:
            self.fields = all_fields
        else:
            # check each element of fields is in all_fields
            for field in self.fields:
                if field not in all_fields:
                    raise ValueError(f"Field {field} not in shapefile")

        # The feature table contains all geometries in the shp file and
        # their attributes from shp fields as columns.
        # Attributes are used to select relevant features, e.g. countries
        # by name.
        self.features = self._init_build_feature_table()

    def __repr__(self):
        name = self.__class__.__name__
        return f"shp_path: {self.shp_path}\n" \
               f"See `{name}.features` for the full feature table.\n" \
               f"----------------------------------------------------\n" \
               f"{len(self.features.index)} features with Fields: " \
               f"{self.fields}"

    def _init_open_shp(self):
        """
        Open shapefile and get layer
        """
        self.driver = ogr.GetDriverByName(self.driver)
        self.ds = self.driver.Open(self.shp_path)
        self.layer = self.ds.GetLayer()
        self.srs = self.layer.GetSpatialRef()

    def _init_build_feature_table(self):
        """
        Extract names of features in the relevant fields and stores them
        in a pandas dataframe.
        Each row in the data frame refers to the same feature in the shapefile.
        The index is the id under which the feature is found.
        Columns can be used to find the id(s) for a given name.

        Returns
        -------
        df: pd.DataFrame
            Dataframe with feature ids and names for features in passed fields

        """
        ids = []
        features = {}

        for n in range(self.layer.GetFeatureCount()):
            feature = self.layer.GetFeature(n)
            for field in self.fields:
                if field not in features:
                    features[field] = []
                features[field].append(feature.GetField(field))
            ids.append(n)

        return pd.DataFrame(index=ids, data=features)

    def lookup_id(self, names: Union[str, list, np.ndarray]) -> np.ndarray:
        """
        Lookup ids for passed names in passed field
        """
        names = np.atleast_1d(names)
        rows = np.unique(np.where(np.isin(self.features.values, names))[0])
        return self.features.index.values[rows]

    def geom(self, id) -> ogr.Geometry:
        """
        Get geometry of feature with passed id
        """
        feature = self.layer.GetFeature(id)
        geom = feature.geometry().Clone()
        return geom


@deprecated("Use get_shp_grid_points function")
class CountryShpReader(ShpReader):
    def __init__(self):
        path = os.path.join(os.path.dirname(__file__),
                            'countries_shp', 'ne_110m_admin_0_countries.shp')

        super().__init__(shp_path=path, fields=['NAME', 'CONTINENT'])

    def get_geoms(self, names: Union[str, list]) -> list:
        """
        Get geometries for passed names

        Parameters
        ----------
        names: str or list
            Names of countries or continents to get geometries for.
            Possible names are
        """
        ids = self.lookup_id(names)
        return [self.geom(id) for id in ids]

    def continent_countries(self, *continents):
        if isinstance(continents, str):
            continents = [continents]

        names = np.array([])
        for continent in continents:
            n = self.features.loc[self.features["CONTINENT"] == continent, 'NAME'].values
            names = np.append(names, n)

        return names

    def country_ids(self, *names) -> np.array:
        """
        Get feature ids of passed COUNTRY names.

        Parameters
        ----------
        name: str
            Name(s) of one or multiple countries to get ids for

        Returns
        -------
        ids: list[int]
            Ids of countries with passed names
        """
        return self.lookup_id(names)

    def continent_ids(self, names) -> np.array:
        """
        Get feature ids of passed CONTINENT names.
        Note that Europe and Asia were arbitrarily split into two continents.

        Parameters
        ----------
        name: str, list[str]
            Name(s) of one or multiple continents to get ids for

        Returns
        -------
        ids: list[int]
            Ids of countries with passed names
        """
        return self.lookup_id(names)


def subgrid_for_shp(grid, values, shp_path=path_shp_countries,
                    field=None, shp_driver='ESRI Shapefile',
                    verbose=False):
    """
    Cut grid to selected shape(s) from passed shapefile

    Parameters
    ----------
    grid: CellGrid
        Grid that should be cut to shape(s) in passed shapefile
    values: np.ndarray or list
        Values in field that are used to select the shape(s) to cut the grid
        to. Usually e.g. a list of country names or continent names.
        The passed values are looked up in all loaded fields, i.e. in all
        columns of the feature table. A polygon is selected if the value
        appears in ANY of the columns (fields) of the feature table.
    shp_path: str, optional
        Path to shapefile. By default we use the 110m resolution country
        shape file provided in this package.
        ----------------------------------------------------------------------
        It contains the following country names (field: 'NAME'):
        ['Afghanistan', 'Albania', 'Algeria', 'Angola', 'Antarctica',
        'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan',
        'Bahamas', 'Bangladesh','Belarus', 'Belgium', 'Belize', 'Benin',
        'Bhutan', 'Bolivia', 'Bosnia and Herz.', 'Botswana', 'Brazil',
        'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia',
        'Cameroon', 'Canada', 'Central African Rep.', 'Chad', 'Chile','China',
        'Colombia', 'Congo', 'Costa Rica', 'Croatia', 'Cuba', 'Cyprus',
        'Czechia', "Côte d'Ivoire", 'Dem. Rep. Congo', 'Denmark', 'Djibouti',
        'Dominican Rep.', 'Ecuador', 'Egypt', 'El Salvador', 'Eq. Guinea',
        'Eritrea', 'Estonia', 'Ethiopia', 'Falkland Is.', 'Fiji', 'Finland',
        'Fr. S. Antarctic Lands', 'France', 'France (SA)', 'Gabon', 'Gambia',
        'Georgia', 'Germany', 'Ghana', 'Greece', 'Greenland', 'Guatemala',
        'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hungary',
        'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel',
        'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kosovo',
        'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho',
        'Liberia', 'Libya', 'Lithuania', 'Luxembourg', 'Macedonia',
        'Madagascar', 'Malawi', 'Malaysia', 'Mali', 'Mauritania', 'Mexico',
        'Moldova', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique',
        'Myanmar', 'N. Cyprus', 'Namibia', 'Nepal', 'Netherlands',
        'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria',
        'North Korea', 'Norway', 'Oman', 'Pakistan', 'Palestine', 'Panama',
        'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland',
        'Portugal', 'Puerto Rico', 'Qatar', 'Romania', 'Russia (AS)',
        'Russia (EU)', 'Rwanda', 'S. Sudan', 'Saudi Arabia', 'Senegal',
        'Serbia', 'Sierra Leone', 'Slovakia', 'Slovenia', 'Solomon Is.',
        'Somalia', 'Somaliland', 'South Africa', 'South Korea', 'Spain',
        'Sri Lanka', 'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Syria',
        'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Timor-Leste', 'Togo',
        'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Uganda',
        'Ukraine', 'United Arab Emirates', 'United Kingdom',
        'United States of America', 'Uruguay', 'Uzbekistan', 'Vanuatu',
        'Venezuela', 'Vietnam', 'W. Sahara', 'Yemen', 'Zambia', 'Zimbabwe',
        'eSwatini']
        ----------------------------------------------------------------------
        and the following continent names (field: 'CONTINENT'):
        ['Africa', 'Antarctica', 'Asia', 'Europe', 'North America', 'Oceania',
        'Seven seas (open ocean)', 'South America']
    field: str or list[str], optional
        Shapefile field(s) to use for attribute table columns.
        If None is passed, all fields are used (slow). Limiting the fields
        leads to faster lookup times and is recommended especially for complex
        shapefiles.
        For the default countries shp file it is suggested to use the fields:
        "NAME" and "CONTINENT" to search for countries and continents by their
        names.
    shp_driver: str, optional
        Driver to use for reading vector shapefile. Default is ESRI Shapefile.
    verbose: bool, optional
        If True, print some information while processing. This also prints
        all available fields and the attribute table after loading the file.

    Returns
    -------
    subgrid: CellGrid
        Subgrid that is cut to the shape(s) in the shapefile
    """
    shp_reader = ShpReader(shp_path, fields=field, driver=shp_driver)

    if verbose:
        print(shp_reader)

    if verbose:
        print("--------------")
        print("Feature table:")
        print(shp_reader.features)

    ids = np.unique(shp_reader.lookup_id(values))

    if len(ids) == 0:
        raise ValueError(f"No features found for {values} in "
                         f"fields {shp_reader.fields}")

    gpis = np.array([], dtype=int)
    for i, id in enumerate(ids):
        if verbose:
            print('Creating subset {} of {} ... to speed this up '
                  'improve pygeogrids.grids.get_shp_grid_points()'.format(
                   i + 1, ids.size))

        subgrid = grid.get_shp_grid_points(shp_reader.geom(id))
        if subgrid is not None:
            poly_gpis = subgrid.activegpis
            gpis = np.append(gpis, poly_gpis)
        else:
            pass

    if gpis.size == 0:
        empty_arr = np.array([])
        return CellGrid(lon=empty_arr, lat=empty_arr, cells=empty_arr)
    else:
        return grid.subgrid_from_gpis(np.unique(gpis))


if __name__ == '__main__':
    from smecv_grid.grid import SMECV_Grid_v052
    grid = SMECV_Grid_v052()
    sgrid = subgrid_for_shp(grid, ['Russia'],
                            verbose=True)
