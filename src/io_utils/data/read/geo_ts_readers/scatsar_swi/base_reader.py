# -*- coding: utf-8 -*-

"""
Module description
"""
# TODO:
#   (+) 
#---------
# NOTES:
#   -

from equi7grid.equi7grid import Equi7Grid
import yeoda.datacube as dc
from geopathfinder.naming_conventions.sgrt_naming import SgrtFilename
from geopathfinder.folder_naming import build_smarttree
from osgeo import ogr
from osgeo import osr
from datetime import datetime
import glob
import numpy as np
import os

def decode_scatsar(data):
    data = data.astype(float)
    data[data>=240] = np.nan
    data /= 2.
    return data

class ScatSarCglsSwiReader(object):

    def __init__(self, path, tval=5, grid_sampling=500):
        
        self.path = path

        self.grid_sampling = grid_sampling
        self.scatsardc = None#
        self.grid = None

        self.tval = f"{str(tval).zfill(3)}"

    def _build(self):
        if self.grid is None:
            self.grid = Equi7Grid(self.grid_sampling).EU

        folder_hierarchy = ["subgrid_name", "tile_name", "var_name"]
        print(datetime.now(), 'Build smart tree..')

        self.dir_tree = build_smarttree(self.path, folder_hierarchy,
                                        register_file_pattern="^[^Q].*.tif")

        dim = ["time", "var_name", "tile_name"]
        print(datetime.now(), 'Create data cube..')

        self.scatsardc = dc.EODataCube(filepaths=self.dir_tree.file_register,
                                       smart_filename_class=SgrtFilename,
                                       dimensions=dim, grid=self.grid,
                                       sdim_name="tile_name")

        self.scatsardc.filter_files_with_pattern(pattern=f'swi_t{self.tval}',
                                                 full_path=True)

        self.sref = osr.SpatialReference()
        self.sref.ImportFromEPSG(4326)

    def read(self, *args, **kwargs):
        """ Read data for a single point from data cube """
        # import pandas as pd

        if self.scatsardc is None:
            self._build()
            
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(*args, **kwargs)
        ts = self.scatsardc.filter_spatially_by_geom(point, sref=self.sref)
        print(datetime.now(), 'Read point..')
        df = decode_scatsar(ts.load_by_coords(
                    point.GetX(), point.GetY(), sref=self.sref, dtype="dataframe"))

        df = df.set_index(df.index.get_level_values('time'))
        df = df.rename(columns={'1': f"swi_t{self.tval}"})

        return df


# Scatsar SWI (Drypan) Laura
class ScatSarSWIDrypanReader(object):
    """
    Class reading SCATSAR SWI anomalies.
    Projected in Web Mercator Projection (EPSG:3857)
    """

    def __init__(self, path, smart_filename_class, switchflip=False):

        self.path = path
        self.smart_filename_class = smart_filename_class
        self.dc = None

        self.switchflip = switchflip


    def _build(self):
        """
        Builds a yeoda EODataCube of SCATSAR SWI anomalies data.
        """
        print(f'{datetime.now()}: Building Datacube....')

        file_paths = glob.glob(os.path.join(self.path, '*.tif'))
        dims = ['time']
        self.dc = dc.EODataCube(filepaths=file_paths,
                                dimensions=dims,
                                smart_filename_class=self.smart_filename_class)
        print(f'{datetime.now()}: DONE!')

        self.sref = osr.SpatialReference()
        self.sref.ImportFromEPSG(3857)


    def read(self, lon, lat):
        """
        Reads data for a single point (lon, lat).
        """
        if self.dc is None:
            self._build()

        print(datetime.now(), 'Read single point...', end='')
        geom = ogr.Geometry(ogr.wkbPoint)
        geom.AddPoint(lon, lat)

        source = osr.SpatialReference()
        source.ImportFromEPSG(4326)
        transform = osr.CoordinateTransformation(source, self.sref)
        geom.Transform(transform)

        ts = self.dc.filter_spatially_by_geom(geom, sref=self.sref)
        df = ts.load_by_coords(geom.GetX(), geom.GetY(), sref=self.sref, dtype="dataframe")
        df = df.rename(columns={'1': "SCATSAR_SWI"})
        df = df.set_index(df.index.get_level_values('time'))

        if self.switchflip:
            df *= -1

        return df