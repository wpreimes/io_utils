# -*- coding: utf-8 -*-

"""
Module description
"""
# TODO:
#   (+) 
#---------
# NOTES:
#   -

import yaml
import sys
import importlib
import os
from argparse import Namespace

def read_settings(settings_file, *args):
    """
    Parser for reading settings from the settings-yaml file.
    Parse <OS-identifiers> and <PATH> automatically to return correct path strings
    and OS dependent paths.

    Parameters
    -------
    settings_file : str
        Path to the settings yml file to read
    args: str
        Name(s) of parameter groups to read. If none are passed, all are read.

    Returns
    -------
    kwargs : dict
        Key word arguments of the argument groups that were passed.
    """
    #filedir = (os.path.dirname(os.path.realpath(__file__)))
    with open(settings_file, 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)

    # handle <OS> tag
    curr_os = sys.platform
    if 'win' in curr_os:
        for level, data in cfg.items():
            new_data = {}
            for k, v in data.items():
                if '<WIN>' in k:
                    new_key = k.replace('<WIN>', '')
                    new_data[new_key] = cfg[level][k]
                elif '<LINUX>' in k:
                    pass
                else:
                    new_data[k] = cfg[level][k]
            cfg[level] = new_data

    elif 'linux' in sys.platform:
        for level, data in cfg.items():
            new_data = {}
            for k, v in data.items():
                if '<LINUX>' in k:
                    new_key = k.replace('<LINUX>', '')
                    new_data[new_key] = cfg[level][k]
                elif '<WIN>' in k:
                    pass
                else:
                    new_data[k] = cfg[level][k]
            cfg[level] = new_data

    # handle <PATH> tag
    for level, data in cfg.items():
        new_data = {}
        for k in data.keys():
            if '<PATH>' in k:
                new_key = k.replace('<PATH>', '')
                new_v = None if data[k] == 'None' else os.path.join(*data[k])
                new_data[new_key] = new_v
            elif '<MODULE>' in k:
                if not isinstance(data[k], str):
                    raise IOError("<MODULE> expects a string, e.g. numpy.ma")
                new_key = k.replace('<MODULE>', '')
                new_v = importlib.import_module(data[k])
                new_data[new_key] = new_v
            elif '<CLASS>' in k or '<FUNCTION>' in k:
                if not isinstance(data[k], list):
                    raise IOError("<CLASS> and <FUNCTION> expect a list, e.g. [numpy.ma, unique]")
                new_key = k.replace('<CLASS>', '').replace('<FUNCTION>', '')
                # first element is the module, second is the class/function
                new_v = getattr(importlib.import_module(data[k][0]), data[k][1])
                new_data[new_key] = new_v
            else:
                new_data[k] = data[k]
        cfg[level] = new_data

    params = {}
    if not args:
        args = cfg.keys()
    for arg in args: params.update({arg: cfg[arg]})

    for level, data in params.items():
        if 'None' in data.values(): # Replace 'None' with real None
            for i, v in data.items():
                if v == 'None': params[level][i] = None

    return params


def spaceify(settings, *sections):
    """
    Read a section of settings (yaml file or dict) and create an according
    namespace containing the variables.

    EG the section GLOBAL is made into namespace GLOBAL and the variable
    var in GLOBAL is created as GLOBAL.var

    Parameters
    ----------
    settings : str or dict
        Path to the according yml file with a GLOBAL section or the dict from
        reading the file directly.
    sections : str, optionel
        Section(s) in the yaml file or the dict (2 levels) to create namespaces
        from. If None are passed, all are read.

    Returns
    -------
    namespaces : Namespaces
        Namespaces created from the passed settings for each dictionary layer
    """

    if isinstance(settings, dict):
        sets = settings
    else:
        sets = read_settings(settings)

    if len(sections) == 0:
        sections = list(sets.keys())

    nspacs = [Namespace(**sets[sec]) for sec in sections]

    if len(nspacs) == 1:
        return nspacs[0]
    else:
        return tuple(nspacs)