# -*- coding: utf-8 -*-

import pytest
from io_utils.data.read.geo_ts_readers.ts_reader import GeoTsReader
from io_utils.data.read.geo_ts_readers import (
    GeoCCISMv6Ts,
    GeoGLDAS21Ts,
    GeoISMNTs,
    GeoHsafAscatSsmTs,
    GeoEra5LandTs,
    GeoCglsNcTs,
    GeoSpl3smpTs,
)
import numpy as np
from datetime import datetime
import os
import io_utils.root_path as root_path
import pandas as pd

test_loc = (15, 45)

@pytest.mark.geo_test_data
def test_smap_sat_data():
    """
    Read ESA CCI SM 45 data, mask based on goodl-flags soil and create
    sm anomalies based on 1991-2010 clim.
    """
    """
    Read SMAP data, mask based on good-flags and create
    sm anomalies based on clim.
    """

    reader_kwargs = {
        "dataset_or_path": ('SMAP', 'SP3SMPv6', 'ASC'),
        "force_path_group": "climers",
        'parameters': ['surface_temperature', 'retrieval_qual_flag', 'soil_moisture'],
        'exact_index': True,
        "ioclass_kws": {"read_bulk": True},
    }

    adapters = {
        "01-SelfMaskingAdapter":
            # Usually one would read SMAP values where retrieval flag is 0 or 8
            # (no bit active, or only the freeze thaw bit active)
            {"op": np.isin, "threshold": [0,1,8], "column_name": "retrieval_qual_flag"},
        "02-SelfMaskingAdapter":
            {"op": ">=", "threshold": 273, "column_name": "surface_temperature"},
        "03-AnomalyClimAdapter":
            {
                "columns": ["soil_moisture"],
                "wraparound": True,
                "timespan": ["1900-01-01", "2099-12-31"],
            },
    }

    resample = None
    params_rename = {"sm": "smap_sm"}

    fancyreader = GeoTsReader(
        GeoSpl3smpTs,
        reader_kwargs,
        adapters=adapters,
        resample=resample,
        filter_months=None,
        params_rename=params_rename,
    )

    assert list(fancyreader.adapters.keys()) == \
           ['01-SelfMaskingAdapter', '02-SelfMaskingAdapter', '03-AnomalyClimAdapter']

    ts = fancyreader.read(*test_loc)

    ts = ts.dropna(how="all")
    for c in ['surface_temperature', 'retrieval_qual_flag', 'soil_moisture']:
        assert c in ts.columns

    assert np.all(np.isin(ts["retrieval_qual_flag"].dropna().values, [0,1,8]))
    assert np.all(ts["surface_temperature"].dropna().values >= 273)
    assert not ts["soil_moisture"].dropna().empty
    assert not ts.empty

@pytest.mark.geo_test_data
def test_ascat_sat_data():
    """
    Read ESA CCI SM 45 data, mask based on goodl-flags soil and create
    sm anomalies based on 1991-2010 clim.
    """
    """
    Read ASCAT data, mask based on good-flags soil and create
    sm anomalies based on clim.
    """
    grid_path = os.path.join(
        root_path.r,
        "Projects",
        "H_SAF_CDOP4",
        "05_deliverables_products",
        "cdop3",
        "auxiliary",
        "warp5_grid",
        "TUW_WARP5_grid_info_2_3.nc",
    )

    reader_kwargs = {
        "dataset_or_path": ("HSAF_ASCAT", "SSM", "H115+H116"),
        "force_path_group": "radar",
        "grid_path": grid_path,
        'fn_format': 'H115_H116_{:04d}',
        "parameters": ["sm", "proc_flag", "conf_flag"],
        "ioclass_kws": {"read_bulk": True},
    }

    adapters = {
            "01-SelfMaskingAdapter":
            {"op": "==", "threshold": 0, "column_name": "proc_flag"},
            "02-SelfMaskingAdapter":
            {"op": "==", "threshold": 0, "column_name": "conf_flag"},
            "03-SelfMaskingAdapter":
            {"op": "<=", "threshold": 50, "column_name": "sm"},
            "04-AnomalyClimAdapter":
            {
                "columns": ["sm"],
                "wraparound": True,
                "timespan": ["1900-01-01", "2099-12-31"],
            },
            "05-ColumnCombineAdapter":
            {
                "func": np.nanmean,
                "columns": ["sm", "proc_flag"],
                "func_kwargs": {},
                "new_name": "mean_sm_procflag",
            }
    }

    resample = ("1D", "mean")
    params_rename = {"sm": "ascat_sm"}

    fancyreader = GeoTsReader(
        GeoHsafAscatSsmTs,
        reader_kwargs,
        adapters=adapters,
        resample=resample,
        filter_months=None,
        params_rename=params_rename,
    )

    assert list(fancyreader.adapters.keys()) == \
           ['01-SelfMaskingAdapter', '02-SelfMaskingAdapter', '03-SelfMaskingAdapter',
            '04-AnomalyClimAdapter', '05-ColumnCombineAdapter']

    ts = fancyreader.read(*test_loc)

    ts = ts.dropna(how="all")
    assert np.all(
        ts.columns.values
        == ["ascat_sm", "proc_flag", "conf_flag", "mean_sm_procflag"]
    )
    assert np.all(ts["proc_flag"].dropna().values == 0.0)
    assert np.all(ts["conf_flag"].dropna().values == 0.0)
    assert np.all(ts["ascat_sm"].dropna().values <= 50.0)
    assert not ts["mean_sm_procflag"].dropna().empty
    assert not ts.empty


@pytest.mark.geo_test_data
def test_cci_sat_data():
    """
    Read ESA CCI SM 45 data, mask based on goodl-flags soil and create
    sm anomalies based on 1991-2010 clim.
    """
    reader_kwargs = {
        "dataset_or_path": ("ESA_CCI_SM", "v061", "COMBINED"),
        "force_path_group": "climers",
        "exact_index": True,
        "parameters": ["sm", "flag", "t0", "sm_uncertainty"],
        "ioclass_kws": {"read_bulk": True},
    }

    adapters = {
            "01-SelfMaskingAdapter":
            {"op": "==", "threshold": 0, "column_name": "flag"},
            "02-AnomalyClimAdapter":
            {
                "columns": ["sm"],
                "wraparound": True,
                "moving_avg_clim": 30,
                "timespan": [datetime(1991, 1, 1), datetime(2010, 12, 31)],
            }
    }

    resample = ("10D", "mean")
    params_rename = {"sm": "esa_cci_sm"}

    fancyreader = GeoTsReader(
        GeoCCISMv6Ts,
        reader_kwargs,
        adapters=adapters,
        resample=resample,
        filter_months=None,
        params_rename=params_rename,
    )
    assert list(fancyreader.adapters.keys()) == \
           ['01-SelfMaskingAdapter', '02-AnomalyClimAdapter']

    ts = fancyreader.read(*test_loc)

    ts = ts.dropna(how="all")
    assert np.all(
        ts.columns.values == ["esa_cci_sm", "flag", "sm_uncertainty"]
    )
    assert np.all(ts["flag"].dropna().values == 0.0)
    assert np.all(ts["esa_cci_sm"].dropna().values <= 0.1)
    assert not ts.dropna().empty
    print(ts)


@pytest.mark.geo_test_data
def test_gldas_model_data():
    """
    Read GLDAS 21 Sm and temp data, mask based on frozen soil and create
    sm anomalies based on 2000-2010 clim.
    """
    reader_kwargs = {
        "dataset_or_path": ("GLDAS21", "core"),
        "force_path_group": "climers",
        "parameters": ["SoilMoi0_10cm_inst", "SoilTMP0_10cm_inst"],
        "ioclass_kws": {"read_bulk": True},
    }

    adapters = {
            "01-SelfMaskingAdapter":
            {
                "op": ">=",
                "threshold": 277.15,
                "column_name": "SoilTMP0_10cm_inst",
            },
            "02-AnomalyClimAdapter":
            {
                "columns": ["SoilMoi0_10cm_inst"],
                "wraparound": True,
                "moving_avg_clim": 30,
                "timespan": [datetime(2000, 1, 1), datetime(2010, 12, 31)],
            },
    }

    resample = ("1D", "mean")
    params_rename = {"SoilMoi0_10cm_inst": "sm", "SoilTMP0_10cm_inst": "tmp"}

    fancyreader = GeoTsReader(
        GeoGLDAS21Ts,
        reader_kwargs,
        adapters=adapters,
        resample=resample,
        filter_months=None,
        params_rename=params_rename,
    )

    assert list(fancyreader.adapters.keys()) == \
        ['01-SelfMaskingAdapter', '02-AnomalyClimAdapter']

    ts = fancyreader.read(*test_loc)

    ts = ts.dropna(how="all")
    assert np.all(ts.columns.values == ["sm", "tmp"])
    assert np.all(ts["tmp"].dropna().values >= 277.15)
    assert not ts.empty
    print(ts)


@pytest.mark.geo_test_data
def test_era5land_rean_data():
    reader_kwargs = {
        "group_vars": {
            ("ERA5-Land", "sm_precip_lai"): ["swvl1"],
            ("ERA5-Land", "temperature"): ["stl1"],
        },
        "ioclass_kws": {"read_bulk": True},
    }

    adapters = {
            "01-SelfMaskingAdapter":
            {"op": ">=", "threshold": 277.15, "column_name": "stl1"},
            "02-AnomalyClimAdapter":
            {
                "columns": ["swvl1"],
                "wraparound": True,
                "moving_avg_clim": 30,
                "timespan": [datetime(2000, 1, 1), datetime(2010, 12, 31)],
            }
    }

    resample = None
    params_rename = {"swvl1": "swvl1", "stl1": "stl1"}

    fancyreader = GeoTsReader(
        GeoEra5LandTs,
        reader_kwargs,
        adapters=adapters,
        resample=resample,
        filter_months=None,
        params_rename=params_rename,
    )
    assert list(fancyreader.adapters.keys()) == \
        ['01-SelfMaskingAdapter', '02-AnomalyClimAdapter']

    ts = fancyreader.read(*test_loc)

    ts = ts.dropna(how="all")
    assert np.all(ts.columns.values == ["swvl1", "stl1"])
    assert np.all(ts["stl1"].dropna().values >= 277.15)
    assert not ts.empty
    print(ts)


def test_insitu_data():
    """
    Read GLDAS 21 Sm and temp data, mask based on frozen soil and create
    sm anomalies based on 2000-2010 clim.
    """
    reader_kwargs = {
        "dataset_or_path": ("ISMN", "v20191211"),
        "network": "COSMOS",
        "force_path_group": "__test",
    }

    adapters = {
            "01-SelfMaskingAdapter":
            {
                "op": "==",
                "threshold": "G",
                "column_name": "soil_moisture_flag",
            },
            "02-AnomalyClimAdapter":
            {
                "columns": ["soil_moisture"],
                "wraparound": True,
                "moving_avg_clim": 30,
                "timespan": [datetime(2010, 1, 1), datetime(2019, 12, 31)],
            },
    }
    resample = None
    params_rename = {"soil_moisture": "initu_sm"}

    # with the default read function:
    fancyreader = GeoTsReader(
        GeoISMNTs,
        reader_kwargs,
        adapters=adapters,
        resample=resample,
        filter_months=None,
        params_rename=params_rename,
    )

    assert list(fancyreader.adapters.keys()) == \
        ['01-SelfMaskingAdapter', '02-AnomalyClimAdapter']

    fancyreader.base_reader.rebuild_metadata()

    nearest, dist = fancyreader.base_reader.find_nearest_station(
        -155.5, 19.9, return_distance=True
    )
    assert nearest.name == "SilverSword"
    ids = fancyreader.base_reader.get_dataset_ids(
        "soil_moisture", min_depth=0, max_depth=0.17
    )
    ts = fancyreader.read(ids[0])  # read and mask
    assert all(ts["soil_moisture_flag"].values == "G")
    df_drop = ts["initu_sm"].dropna()
    assert not df_drop.empty


def test_other_function_than_read():
    class ReaderWithTestFunct(GeoCglsNcTs):
        def test_read_ts(self, *args, **kwargs):
            return super().read(*args, **kwargs)

    dataset = ("CSAR", "CGLS", "SWI", "1km", "V1.0")

    reader_kwargs = {
        "dataset_or_path": dataset,
        "parameters": "SWI_005",
        "force_path_group": "__test",
    }

    adapters = {
            "01-AnomalyClimAdapter":
            {
                "columns": ["SWI_005"],
                "wraparound": True,
                "moving_avg_clim": 30,
                "timespan": [datetime(2010, 1, 1), datetime(2019, 12, 31)],
            },
    }
    # with a different read function
    fancyreader = GeoTsReader(
        ReaderWithTestFunct,
        reader_kwargs,
        read_func_name="test_read_ts",
        adapters=adapters,
        resample=("MS", "mean"),
        filter_months=None,
        params_rename={"SWI_005": "swi5"},
    )

    assert list(fancyreader.adapters.keys()) == ['01-AnomalyClimAdapter']

    data = fancyreader.test_read_ts(-155.4776781090898, 19.80803588124469)
    assert not data.dropna().empty
    assert data.freq == "MS"
    assert np.any(data["swi5"] < 0)  # make sure it's an anom


if __name__ == "__main__":
    test_other_function_than_read()
    test_ascat_sat_data()
    test_cci_sat_data()
    test_era5land_rean_data()
    test_gldas_model_data()
    test_insitu_data()
