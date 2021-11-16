# -*- coding: utf-8 -*-

"""
Collects all the GeoTsReaders that have a path implementation and work in the
same way.
"""

# ASCAT readers
from io_utils.read.geo_ts_readers.hsaf_ascat.hsaf_ascat_ssm import *
from io_utils.read.geo_ts_readers.hsaf_ascat.hsaf_ascat_smdas import *
from io_utils.read.geo_ts_readers.ascat_direx.base_reader import *

# AMSR2 readers
from io_utils.read.geo_ts_readers.amsr2.lprm_amsr2 import *

# CCI SWI readers
from io_utils.read.geo_ts_readers.smecv_swi_rzsm.smecv_swi_rzsm_v0 import *

## CCI version readers
from io_utils.read.geo_ts_readers.esa_cci_sm.esa_cci_sm_v07 import *
from io_utils.read.geo_ts_readers.esa_cci_sm.esa_cci_sm_v06 import *
from io_utils.read.geo_ts_readers.esa_cci_sm.esa_cci_sm_v06_genio import *
from io_utils.read.geo_ts_readers.esa_cci_sm.esa_cci_sm_v05 import *
from io_utils.read.geo_ts_readers.esa_cci_sm.esa_cci_sm_v04 import *
from io_utils.read.geo_ts_readers.esa_cci_sm.esa_cci_sm_v03 import *

## C3S version readers
from io_utils.read.geo_ts_readers.c3s_sm.c3s_sm_v201706 import *
from io_utils.read.geo_ts_readers.c3s_sm.c3s_sm_v201812 import *
from io_utils.read.geo_ts_readers.c3s_sm.c3s_sm_v201912 import *
from io_utils.read.geo_ts_readers.c3s_sm.c3s_sm_v202012 import *

## ERA version readers
from io_utils.read.geo_ts_readers.era.eraint_land import *
from io_utils.read.geo_ts_readers.era.era5_land import *
from io_utils.read.geo_ts_readers.era.era5 import *

## GLDAS version readers
from io_utils.read.geo_ts_readers.gldas.gldas21 import *
from io_utils.read.geo_ts_readers.gldas.gldas20 import *

# MERRA version readers
from io_utils.read.geo_ts_readers.merra.merra2 import *

# SMOS version readers
from io_utils.read.geo_ts_readers.smos.smos_ic import *

## SMAP version readers
from io_utils.read.geo_ts_readers.smap.spl3smp import *
from io_utils.read.geo_ts_readers.smap.smap_lprm import *

# ISMN version readers
from io_utils.read.geo_ts_readers._ismn.ismn_sm import *

# CGLS HR time series readers
from io_utils.read.geo_ts_readers.csar_cgls.csar_cgls_nc import *
# Optional readers (using packages that are difficult to install)

try:
    from io_utils.read.geo_ts_readers.esa_cci_sm.esa_cci_sm_v06_genio import *
    from io_utils.read.geo_ts_readers.amsr2.ccids_amsr2 import *
    pygenio_available = True
except ImportError:
    pygenio_available = False
    warnings.warn('Could not import pygenio. Pygenio is a TUW internal package (deprecated).')


try:
    # SCATSAR reading uses many other packages, therefore it's optional here
    from io_utils.read.geo_ts_readers.scatsar_swi.scatsar_cgls_equi7 import \
        GeoScatSarCglsSwiReader
    from io_utils.read.geo_ts_readers.scatsar_swi.scatsar_swi_drypan import \
        GeoScatSarSWIDrypanAbsReader, GeoScatSarSWIDrypanAnomsReader

    from io_utils.read.geo_ts_readers.csar_cgls.csar_cgls_ssm import \
        GeoCSarSsmTiffReader
    from io_utils.read.geo_ts_readers.csar_cgls.csar_cgls_swi import \
        GeoCSarSwiTiffReader
    hr_available = True
except ImportError:
    hr_available = False
    warnings.warn('Could not import SAR reader. One of the following packages is not installed:'
                  'geopathfinder, yeoda'
                  ' - Sentinel SM product reading not available.')
