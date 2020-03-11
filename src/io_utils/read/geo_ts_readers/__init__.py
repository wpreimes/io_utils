# -*- coding: utf-8 -*-

"""
Collects all the GeoTsReaders that have a path implementation and work in the
same way.
"""

## CCI version readers
from io_utils.read.geo_ts_readers.esa_cci_sm.esa_cci_sm_v05 import *
from io_utils.read.geo_ts_readers.esa_cci_sm.esa_cci_sm_v04 import *
from io_utils.read.geo_ts_readers.esa_cci_sm.esa_cci_sm_v03 import *

## C3S version readers
from io_utils.read.geo_ts_readers.c3s_sm.c3s_sm_v201706 import *
from io_utils.read.geo_ts_readers.c3s_sm.c3s_sm_v201812 import *
from io_utils.read.geo_ts_readers.c3s_sm.c3s_sm_v201912 import *

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
from io_utils.read.geo_ts_readers.smap.smap import *

# ISMN version readers
from io_utils.read.geo_ts_readers.ismn.ismn_sm import *