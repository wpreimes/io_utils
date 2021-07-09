from pytesmo.validation_framework.results_manager import PointDataResults
import pandas as pd
import warnings
import numpy as np
import os

def netcdf_results_manager(results, filename, save_path, ts_vars:list=None, zlib=True,
                           attr=None, global_attr=None):
    """
    Write validation results to netcdf file.
    This is taken from pytesmo, but allows setting a specific file name.

    Parameters
    ----------
    results : dict
        Validation results as returned by the metrics calculator.
        Keys are tuples that define the dataset names that were used.
        Values contains 'lon' and 'lat' keys for defining the points, and optionally
        'time' which sets the time stamps for each location (if there are metrics
        over time in the results - e.g due to RollingMetrics)
    save_path : str
        Directory where the netcdf file(s) are are created, filenames follow
        from the results keysS
    ts_vars : list, optional (default: None)
        List of variables in results that are treated as time series
    zlib : bool, optional (default: True)
        Activate compression
    attr : dict, optional (default: None)
        Variable attributes, variable names as keys, attributes as another
        dict in values.
    global_attr : dict, optional (default: None)
        Global attributes as a dict.
    """

    if len(results) == 0:
        warnings.warn(f"Empty results, {save_path} will not be created.")

    filename = os.path.join(save_path, filename)

    for ds_names, res in results.items():

        with PointDataResults(filename, zlib=zlib) as writer:
            lons = res.pop('lon')
            lats = res.pop('lat')
            if ts_vars is not None:
                for i, (lon, lat) in enumerate(zip(lons, lats)):
                    data = {}
                    for k, v in res.items():
                        if k.lower() == 'time':
                            time = pd.DatetimeIndex(res['time'][i])
                        elif k in ts_vars:
                            data[k] = v[i]
                        else:
                            if not isinstance(v[i], np.ndarray):
                                data[k] = np.array([v[i]])
                            else:
                                data[k] = v[i]

                    writer.add_result(lon, lat, data=data, ts_vars=ts_vars,
                                      times=time, attr=attr)

            else:
                writer.add_metrics_results(lons, lats, results=res, attr=attr)

            for name, val in global_attr.items():
                writer.add_global_attr(name, val)