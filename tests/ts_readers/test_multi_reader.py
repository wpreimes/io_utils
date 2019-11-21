# -*- coding: utf-8 -*-

"""
Module description
"""
# TODO:
#   (+) 
#---------
# NOTES:
#   -

from io_data.time_series import GeoDsTsReader
import pandas as pd

def test_multi_reader():
    ds = GeoDsTsReader(
        ds_params={
            ('ESA_CCI_SM', 'v045', 'COMBINED'): ['sm', 'sm_uncertainty', 'flag'],
            ('ERA5', 'core'): ['swvl1'],
            ('ERA5-Land', 'temperature'): ['stl1'],
            ('C3S', 'v201706', 'COMBINED'): ['sm', 'flag'],
            ('GLDAS21', 'core'): ['SoilMoi0_10cm_inst'],
            ('MERRA2', 'core'): ['SFMC'],
            ('ERA5-Land', 'sm_precip_lai'): ['swvl1']},
        ds_reader_kwargs={
            ('ESA_CCI_SM', 'v045', 'COMBINED'):
                dict(ioclass_kws=dict(read_bulk= True)),
            ('ERA5', 'core'):
                dict(ioclass_kws=dict(read_bulk=True)),
            ('ERA5-Land', 'temperature'):
                dict(ioclass_kws=dict(read_bulk=True)),
            ('C3S', 'v201706', 'COMBINED') :
                dict(ioclass_kws=dict(read_bulk=True)),
            ('GLDAS21', 'core') :
                dict(ioclass_kws=dict(read_bulk=True), scale_factors={'SoilMoi0_10cm_inst': 0.01}),
            ('MERRA2', 'core') :
                dict(ioclass_kws=dict(read_bulk=True)),
            ('ERA5-Land', 'sm_precip_lai') :
                dict(ioclass_kws = dict(read_bulk=True))},
        ds_params_names={
            (('ESA_CCI_SM', 'v045', 'COMBINED'), 'sm'): 'CCI_SM',
            (('ESA_CCI_SM', 'v045', 'COMBINED'), 'sm_uncertainty'): 'CCI_SM_uncert',
            (('ESA_CCI_SM', 'v045', 'COMBINED'), 'flag'): 'CCI_flag',
            (('ERA5', 'core'), 'swvl1'): 'ERA5_SM',
            (('C3S', 'v201706', 'COMBINED'), 'sm'): 'C3S_SM',
            (('C3S', 'v201706', 'COMBINED'), 'flag'): 'c3s_flag',
            (('GLDAS21', 'core'), 'SoilMoi0_10cm_inst'): 'GLDAS_SM',
            (('MERRA2', 'core'), 'SFMC'): 'MERRA2_SM',
            (('ERA5-Land', 'sm_precip_lai'), 'swvl1'): 'ERA5Land_SM'},
        ds_maskadapter_kwargs={
            # masks the cci data when loading it
            ('ESA_CCI_SM', 'v045', 'COMBINED'): dict(op='==', threshold=0, column_name='flag'),
            # masks the era temp data when loading it
            ('ERA5-Land', 'temperature'): dict(op='>=', threshold=277.15, column_name='stl1')},
        temp_res=('D', pd.DataFrame.mean)
    )

    ts = ds.read_all(15, 45)

if __name__ == '__main__':
    test_multi_reader()