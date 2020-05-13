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
import numpy as np

def decode_scatsar(data):
    data = data.astype(float)
    data[data>=240] = np.nan
    data /= 2.
    return data

class ScatSarCGLSReader(object):

    def __init__(self, path, parameters=None, grid_sampling=500):
        
        self.path = path
        if isinstance(parameters, str):
            parameters = [parameters]

        self.parameters = parameters

        self.grid = Equi7Grid(grid_sampling).EU

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

        self.sref = osr.SpatialReference()
        self.sref.ImportFromEPSG(4326)

    def read_ts(self, *args, **kwargs):
        """ Read data for a single point from data cube """
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(*args, **kwargs)
        ts = self.scatsardc.filter_spatially_by_geom(point, sref=self.sref)
        print(datetime.now(), 'Read point..')
        df = decode_scatsar(ts.load_by_coords(
                    point.GetX(), point.GetY(), sref=self.sref, dtype="dataframe"))

        df = df.set_index(df.index.get_level_values('time'))

        if self.parameters is not None:
            df = df.loc[:, self.parameters]

        return df

if __name__ == '__main__':
    import os
    ds = ScatSarCGLSReader(os.path.join("R:\Datapool", "SCATSAR", "02_processed", "CGLS", "C0418"),
                           parameters=['1'])
    ts = ds.read_ts(11.592313, 48.0013213)
    ts.to_csv(r'C:\Temp\scatsartestts.csv')
    print(ts)
    ts = ds.read_ts(12.592313, 49.0013213)
    print(ts)