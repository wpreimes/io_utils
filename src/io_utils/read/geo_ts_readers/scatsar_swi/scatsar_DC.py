import os
import numpy as np
from equi7grid.equi7grid import Equi7Grid
import yeoda.datacube as dc
from geopathfinder.naming_conventions.sgrt_naming import SgrtFilename
from geopathfinder.folder_naming import build_smarttree
from osgeo import ogr
from osgeo import osr
import rsroot

def decode_scatsar(data):
    data = data.astype(float)
    data[data>=240] = np.nan
    data /= 2.
    return data

class ScatsarTs(object):
    def __init__(self, path):
        self.grid = Equi7Grid(500).EU
        self.path = path
        folder_hierarchy = ["subgrid_name", "tile_name", "var_name"]
        self.dir_tree = build_smarttree(path, folder_hierarchy,
                                        register_file_pattern="^[^Q].*.tif")
        dim = ["time", "var_name", "tile_name"]
        self.scatsardc = dc.EODataCube(filepaths=self.dir_tree.file_register,
                                       smart_filename_class=SgrtFilename,
                                       dimensions=dim, grid=self.grid,
                                       sdim_name="tile_name")

        self.sref = osr.SpatialReference()
        self.sref.ImportFromEPSG(4326)

    def read(self, *args, **kwargs):
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(*args, **kwargs)
        ts = self.scatsardc.filter_spatially_by_geom(point, sref=self.sref)
        df = decode_scatsar(ts.load_by_coords(
                    point.GetX(), point.GetY(), sref=self.sref, dtype="dataframe"))
        return df


if __name__ == '__main__':
    ds = ScatsarTs(os.path.join(rsroot.r, "Datapool", "SCATSAR", "02_processed", "CGLS", "C0418"))
    ts = ds.read(11.592313, 48.0013213)
    print(ts)
# rootdir_path = os.path.join(rsroot.r, "Datapool", "SCATSAR", "02_processed", "CGLS", "C0418")
# folder_hierarchy = ["subgrid_name", "tile_name", "var_name"]
# dir_tree = build_smarttree(rootdir_path, folder_hierarchy, register_file_pattern="^[^Q].*.tif")
# filepaths = dir_tree.file_register
# dim = ["time", "var_name", "tile_name"]
# grid = Equi7Grid(500).EU
# scatsar_DC = dc.EODataCube(filepaths=filepaths, smart_filename_class=SgrtFilename,
#                            dimensions=dim, grid=grid, sdim_name="tile_name")
#
# # --------------------------------
# # here define the coordinate system and coordinates of the location of interest (i.e. in-situ stations)
# sref = osr.SpatialReference()
# sref.ImportFromEPSG(4326)
#
# point = ogr.Geometry(ogr.wkbPoint)
# point.AddPoint(11.59, 48)
# point.AddPoint(11.592313, 48.0013213)
# # --------------------------------
#
# ts = scatsar_DC.filter_spatially_by_geom(point, sref=sref)
# data_point = decode_scatsar(ts.load_by_coords(point.GetX(), point.GetY(), sref=sref, dtype="dataframe"))
# print(data_point)

