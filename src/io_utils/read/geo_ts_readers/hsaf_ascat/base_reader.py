# -*- coding: utf-8 -*-

from ascat.h_saf import AscatNc
import os
from pytesmo.validation_framework.adapters import BasicAdapter

# Ascat index is always exact

class HSAFAscatSSMTs(AscatNc):
    def __init__(self, ts_path, grid_path=None,
                 fn_format="H115_H116_{:04d}", **kwargs):

        if grid_path is None:
            grid_path = os.path.join(ts_path, "grid.nc")

        super(HSAFAscatSSMTs, self).__init__(path=ts_path,
                                         fn_format=fn_format,
                                         grid_filename=grid_path,
                                         **kwargs)




if __name__ == '__main__':
    ascat_path = r"R:\Projects\H_SAF_CDOP3\05_deliverables_products\H116\H115+H116r8"
    grid_path = r"R:\Projects\H_SAF_CDOP3\05_deliverables_products\auxiliary\warp5_grid\TUW_WARP5_grid_info_2_3.nc"
    ds = BasicAdapter(HSAFAscatSSMTs(ascat_path, grid_path, parameters=['sm']))
    ts = ds.read(2501225)