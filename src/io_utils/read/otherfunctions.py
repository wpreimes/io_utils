# -*- coding: utf-8 -*-
from src.io_utils.utils import split, split_cells_gpi_equal
from src.io_utils.yml.read import read_settings

try:
    from rsroot import root_path
except:
    pass

import os
import getpass
import platform



# def regress(data, testdata_col_name, refdata_col_name):
#     '''
#     Perform regression of column refdata on column testdata
#     '''
#     dataframe = data.copy()
#     out = dataframe[refdata_col_name]
#     dataframe = dataframe.dropna()
#     R, pval = stats.pearsonr(dataframe[refdata_col_name], dataframe[testdata_col_name]) # Correlation between Refdata and Testdata
#
#
#     if R < 0 or np.isnan(R):
#         ress = [np.nan]
#         return out, R, pval, ress
#
#     testdata = dataframe[testdata_col_name].values
#     refdata = dataframe[refdata_col_name].values
#     refdata_ones = np.vstack([refdata, np.ones(len(refdata))]).T
#
#     ress = np.linalg.lstsq(refdata_ones, testdata)[0][::-1]
#     dataframe['ones'] = 1
#     xm = np.matrix(dataframe.as_matrix(columns=['ones', refdata_col_name]))
#     out = np.dot(xm, np.matrix(ress).transpose())
#
#     return pd.Series(index=dataframe.index, data=np.squeeze(np.asarray(out))), R, pval, ress


def smart_import(gpi, can_prod, ref_prod):
    '''
    Import from csv files or use the reader if necessary, chooses accordingly
    #todo: test data must be updated to allow reading from csvs for testing.

    Returns
    -------

    '''
    import pandas as pd
    from smecv_grid.grid import SMECV_Grid_v042

    user = getpass.getuser()

    if platform.system() == 'Windows':
        path = os.path.join('H:\\', 'code', 'CCIBreakAdjustment', 'tests',
                            'test-data', 'csv_ts')
        plotpath = os.path.join(root_path.c, 'Temp', 'model_figures', str(gpi))

    elif user == 'wpreimes':
        path = os.path.join('/', 'home', 'wpreimes', 'shares', 'home', 'code',
                            'CCIBreakAdjustment', 'tests', 'test-data', 'csv_ts')
        plotpath = os.path.join('/tmp', 'model_figures', str(gpi))

    else:
        path = os.path.join('/', 'home', 'wolfgang', 'code', 'CCIBreakAdjustment',
                            'tests', 'test-data', 'csv_ts')
        plotpath = os.path.join('/tmp', 'model_figures', str(gpi))

    try:
        readfile = os.path.join(path, 'data_%i.csv' % gpi)

        ts_full = pd.read_csv(os.path.join(path, readfile), index_col=0, parse_dates=True)

    except:
        from old.ts_readers import load_ts_reader, col_scalef
        import pandas as pd
        grid = SMECV_Grid_v042()
        lon, lat = grid.gpi2lonlat(gpi)

        can_sm_col = list(col_scalef(can_prod).keys())[0]
        ref_sm_col = list(col_scalef(ref_prod).keys())[0]

        can_reader = load_ts_reader(can_prod, dropna=True, force_r=False)
        ref_reader = load_ts_reader(ref_prod, force_r=False)
        #adj_sm_col_name = col_scalef('CCI_44_COMBINED_ADJUSTED')

        can = can_reader.read_ts(lon, lat)
        ref = ref_reader.read_ts(lon, lat)

        #adj = adj_reader.read_ts(lon, lat)

        ts_full = pd.DataFrame(data={can_prod: can[can_sm_col],
                                     'flags': can['flag'],
                                     'sm_uncertainty': can['sm_uncertainty'],
                                     ref_prod: ref[ref_sm_col]})


    return ts_full, plotpath


if __name__ == '__main__':
    from smecv_grid.grid import SMECV_Grid_v042
    from io_data import cells_for_identifier
    read_settings(r"D:\data-write\paper_results\iter2\v1\settings.yml")
    grid = SMECV_Grid_v042('land')
    n=8
    cells = cells_for_identifier('Australia', grid)
    parts = split_cells_gpi_equal(cells, n, grid)
    otherparts = split(cells, n)