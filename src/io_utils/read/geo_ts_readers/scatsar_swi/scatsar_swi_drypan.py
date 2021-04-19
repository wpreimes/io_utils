# -*- coding: utf-8 -*-


from io_utils.read.path_config import PathConfig
from io_utils.read.geo_ts_readers.scatsar_swi.base_reader import ScatSarSWIDrypanReader
import numpy as np
from collections import OrderedDict
from geopathfinder.file_naming import SmartFilename
try:
    from io_utils.path_configs.scatsar.paths_scatsar_drypan import path_settings
except ImportError:
    path_settings = {}
import copy
from datetime import datetime

class SCATSARSWIDrypanAnomsFilename(SmartFilename):
    fields_def = OrderedDict([
        ('time', {'start': 29,
                  'len': 8,
                  'decoder': lambda x: datetime.strptime(x, "%Y%m%d"),
                  'encoder': lambda x: x.strftime("%Y%m%d") if isinstance(x, datetime) else x}),
    ])
    pad = "-"
    delimiter = "_"

    def __init__(self, fields, ext=".tif", convert=False):

        fields_def_ext = copy.deepcopy(SCATSARSWIDrypanAnomsFilename.fields_def)

        super(SCATSARSWIDrypanAnomsFilename, self).__init__(
            fields, fields_def_ext,
            pad=SCATSARSWIDrypanAnomsFilename.pad,
            delimiter=SCATSARSWIDrypanAnomsFilename.delimiter,
            convert=convert, ext=ext)

    @classmethod
    def from_filename(cls, filename_str, convert=False):
        return super().\
            from_filename(filename_str, SCATSARSWIDrypanAnomsFilename.fields_def,
                          pad=SCATSARSWIDrypanAnomsFilename.pad,
                          delimiter=SCATSARSWIDrypanAnomsFilename.delimiter,
                          convert=convert)


class SCATSARSWIDrypanAbsFilename(SmartFilename):
    fields_def = OrderedDict([
        ('time', {'start': 16,
                  'len': 8,
                  'decoder': lambda x: datetime.strptime(x, "%Y%m%d"),
                  'encoder': lambda x: x.strftime("%Y%m%d") if isinstance(x, datetime) else x}),
    ])
    pad = "-"
    delimiter = "_"

    def __init__(self, fields, ext=".tif", convert=False):

        fields_def_ext = copy.deepcopy(SCATSARSWIDrypanAbsFilename.fields_def)

        super(SCATSARSWIDrypanAbsFilename, self).__init__(
            fields, fields_def_ext,
            pad=SCATSARSWIDrypanAbsFilename.pad,
            delimiter=SCATSARSWIDrypanAbsFilename.delimiter,
            convert=convert, ext=ext)

    @classmethod
    def from_filename(cls, filename_str, convert=False):
        return super().\
            from_filename(filename_str, SCATSARSWIDrypanAbsFilename.fields_def,
                          pad=SCATSARSWIDrypanAbsFilename.pad,
                          delimiter=SCATSARSWIDrypanAbsFilename.delimiter,
                          convert=convert)

class GeoScatSarSWIDrypanAnomsReader(ScatSarSWIDrypanReader):

    _ds_implemented = [('SCATSAR', 'SWI', 'Drypan', 'Anoms')]

    def __init__(self, dataset_or_path, force_path_group=None, switchflip=False):

        if isinstance(dataset_or_path, list):
            dataset_or_path = tuple(dataset_or_path)

        self.dataset = dataset_or_path
        path_config = path_settings[self.dataset] if self.dataset in path_settings.keys() else None
        self.path_config = PathConfig(self.dataset, path_config)
        path = self.path_config.load_path(force_path_group=force_path_group)

        super(GeoScatSarSWIDrypanAnomsReader, self).__init__(
            path, smart_filename_class=SCATSARSWIDrypanAnomsFilename,
            switchflip=switchflip)


class GeoScatSarSWIDrypanAbsReader(ScatSarSWIDrypanReader):

    _ds_implemented = [('SCATSAR', 'SWI', 'Drypan', 'Abs')]

    def __init__(self, dataset_or_path, force_path_group=None):

        if isinstance(dataset_or_path, list):
            dataset_or_path = tuple(dataset_or_path)

        self.dataset = dataset_or_path
        path_config = path_settings[self.dataset] if self.dataset in path_settings.keys() else None
        self.path_config = PathConfig(self.dataset, path_config)
        path = self.path_config.load_path(force_path_group=force_path_group)

        super(GeoScatSarSWIDrypanAbsReader, self).__init__(
            path=path, smart_filename_class=SCATSARSWIDrypanAbsFilename)

    def read(self, *args, **kwargs):
        ts_point = super(GeoScatSarSWIDrypanAbsReader, self).read(*args, **kwargs)
        ts_point.values[ts_point.values >= 127] = np.nan
        return ts_point

if __name__ == '__main__':

    for anoms in [True, False]:
        if anoms:
            Reader = GeoScatSarSWIDrypanAnomsReader
            dataset = ['SCATSAR', 'SWI', 'Drypan', 'Anoms']
        else:
            Reader = GeoScatSarSWIDrypanAbsReader
            dataset = ['SCATSAR', 'SWI', 'Drypan', 'Abs']

        #root_path = os.path.join(rsroot.r, "Projects", "DryPan", "07_data", name)
        lon, lat = 19.1222, 47.201232
        ds = Reader(dataset)

        # single point time series reading
        ts_point = ds.read(lon, lat)
        print('DONE! (', datetime.now(), ')')
        print(ts_point)
        #äts_point.plot(grid=True, rot=90)
        #print(ts_point.dropna())