# -*- coding: utf-8 -*-

import os
from configparser import SafeConfigParser, RawConfigParser
from datetime import datetime

from pygenio.genio import GenericIO
from rsdata.root_path import root
from collections import OrderedDict
import sys

"""
Modified ESA CCI soil moisture interface module.

Modified from rsdata readers to add the ioclass_kws option
"""

def create_cci_cfg(product_name, product_path, cfg_path,
                   product_class='pynetcf.time_series.GriddedNcOrthoMultiTs'):
    '''
    Create a new (temporal) config file for a new product.

    Parameters
    ----------
    product_name : str
        Name of the new (adjused) product
    product_path : str
        Path to the new (adjusted) product
    product_class : str, optional (default: 'pynetcf.time_series.GriddedNcOrthoMultiTs')
        class for reading the new (adjusted) product

    Returns
    ---------
    cfg_file: str
        Path to the file that was created.
    '''

    parser = RawConfigParser()

    info_default = OrderedDict(
                    [('path', 'r, datasets, CCI_41_D, 042_combined_MergedProd'),
                     ('path_active', 'u, datasets, CCI_41_D, 022_active_MergedProd'),
                     ('path_passive', 'u, datasets, CCI_41_D, 034_passive_MergedProd'),
                     ('cell_format', '{:04d}'),
                     ('fn_format', '%(cell_format)s'),
                     ('grid_class', 'smecv_grid.grid.SMECV_Grid_v042')])

    for key in info_default.keys():
        parser.set('DEFAULT', key, info_default[key])

    path = os.path.normpath(product_path).split(os.path.sep)
    if 'win' in sys.platform and ':' in path[0]:
        path[0] = path[0].split(':')[0].lower()
    elif 'linux' in sys.platform and (path[0]==''):
        path[0] = '/'
    else:
        raise IOError(sys.platform, "Unknown platform")
    info_new = OrderedDict([('path', ',  '.join(path)),
                            ('class', product_class)])
    parser.add_section(product_name)
    for key in info_new.keys():
        parser.set(product_name, key, info_new[key])

    cfg_file = os.path.join(cfg_path, 'temp_config.cfg')
    with open(cfg_file, 'w') as f:
        parser.write(f)

    return cfg_file


def read_cfg(cfg_file, include_default=True):

    config = SafeConfigParser()
    config.read(cfg_file)

    ds = {}
    for section in config.sections():

        ds[section] = {}
        for item, value in config.items(section):

            if 'path' in item:
                value = value.replace(' ', '')
                path = value.split(',')
                path.append('')
                if path[0][0] == '/':
                    value = os.path.join(*path[0:])
                else:
                    value = os.path.join(root[path[0]], *path[1:])

            if 'filename' in item:
                value = value.replace(' ', '')
                path = value.split(',')
                value = os.path.join(*path)

            if 'class' in item:
                module_name = value[:value.rfind('.')]
                class_name = value[value.rfind('.') + 1:]
                module = __import__(module_name, fromlist=[class_name])
                value = getattr(module, class_name)

            if item.startswith('kws'):
                if item[4:] == 'custom_dtype':
                    value = {item[4:]: eval(value)}
                else:
                    value = {item[4:]: value}
                item = 'kws'

            if 'kws' not in ds[section]:
                ds[section]['kws'] = {}

            if include_default or item not in config.defaults().keys():
                if item == 'kws':
                    ds[section][item].update(value)
                else:
                    ds[section][item] = value

    return ds


def get_settings(version, parameter, cfg_path=None):

    if cfg_path is None:
        cfg_file = os.path.join(os.path.dirname(__file__), 'datasets',
                                '{:}.cfg'.format(version))
    else:
        cfg_file = os.path.join(cfg_path, '{:}.cfg'.format(version))

    ds = read_cfg(cfg_file, False)

    if "temp_ids" in ds:
        for k, v in ds['temp_ids'].items():
            ds['temp_ids'][k] = GenericIO.get_template(v)[0]

    if parameter not in ds:
        return {}

    for k, v in ds[parameter].items():
        if k.endswith('_float'):
            del ds[parameter][k]
            ds[parameter][k[:-6]] = float(v)
        if k.endswith('_int'):
            del ds[parameter][k]
            ds[parameter][k[:-4]] = int(v)
        if k.endswith('_date'):
            del ds[parameter][k]
            ds[parameter][k[:-5]] = datetime.strptime(v, '%Y-%m-%d %H:%M:%NcRegGridStack')

    return ds[parameter]


class ESA_CCI_SM_cfg(object):
    # Modified vresion of the ESA_CCI_SM class

    """
    Class factory for the interface to the ESA CCI soil moisture parameters.

    Parameters
    ----------
    version : str
        Version identifier. Looking for a file with the version identifier as a
        name. This argument is ignored if a config file (cfg_file) is specified.
    product : str
        Name of the product (ACTIVE, PASSIVE, COMBINED).
    mode : str, optional (default: r)
        Mode used for file processing
    grid : pygeogrids.CellGrid, optional (default: None)
        Grid to use for reading, if None is passed the one from the cfg file is
        used.
    cfg_file : str, optional (default: None)
        Path to the config file to use for reading.
        If None is passed, we look for one in
    ioclass_kws : dict
        Keywords to pass to the reader class
    """

    def __new__(cls, version, product, mode='r', grid=None, cfg_file=None,
                **kwargs):

        if cfg_file is None:
            curr_os = 'win' if 'win' in sys.platform else 'linux'
            cfg_file = os.path.join(os.path.dirname(__file__), 'cci_cfg_local',
                                    curr_os, '{:}.cfg'.format(version))

        ds = read_cfg(cfg_file)

        if product not in ds:
            raise KeyError('parameter not found {:}'.format(product))

        if 'class' not in ds[product]:
            raise KeyError('interface class not found {:}'.format(product))

        if grid is None:
            grid = ds[product]['grid_class']()

        if not os.path.exists(ds[product]['path']):
            raise IOError('Path to data does not exist')

        return ds[product]['class'](path=ds[product]['path'], grid=grid,
                                    fn_format=ds[product]['fn_format'],
                                    mode=mode, **kwargs)
