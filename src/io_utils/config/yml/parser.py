# -*- coding: utf-8 -*-

"""
Recursively reads content of a yml file as a dictionary.
Supports custom <tags> to transform elements while reading.
    <PATH>: turns a string/list into a python path object with os.path.join
    <WIN> or <LINUX>: Marks elements for inclusion only for certain OS
                      Elements from other OS are DROPPED
    <IMPORT>: Marks element to be imported
        str: import as module (e.g. `numpy.ma`)
        [str, str]: import function or class (e.g. [`np.ma`,`masked_array`])
"""

import numpy as np
import yaml
import sys
import importlib
import os
from argparse import Namespace
import warnings


def kwargs_to_csv(path, kwargs):
    with open(os.path.join(path, 'proc_override_kwargs.csv'), 'w') as f:
        for key, v in kwargs.items():
            f.write("%s,%s\n" % (key, kwargs[key]))

# A list of strings that are ALWAYS replaced
_replace_str_lut = \
    {
    'None': None,
}

supported_platforms = ['WIN', 'LINUX']

if 'win' in sys.platform:
    current_platform = 'WIN'
elif sys.platform == 'linux':
    current_platform = 'LINUX'
else:
    warnings.warn(f"Unexpected platform name {sys.platform.upper()}. Using LINUX now.")
    current_platform = 'LINUX'

def read_level(data: dict):
    """
    Read CDF file level, apply tags, transform some strings etc recursively.

    Parameters
    ----------
    data : dict
        Level data as a dict of yml keys and values
        Sub levels in yml are again dicts (recursive call)

    Returns
    -------
    parsed_level_data : dict
        The transformed/parsed data for this level.
    """

    not_current_platform = [p for p in supported_platforms
                            if p.upper() != current_platform]

    new_data = {}

    for k, v in data.items():

        # recursion in case of sub-levels
        if isinstance(v, dict):
            new_data[k] = read_level(v)
        else:
            # select values for current OS, drop others
            if f"<{current_platform}>" in k:
                k = k.replace(f"<{current_platform}>", "")
            elif any([f"<{p.upper()}>" in k for p in not_current_platform]):
                continue

            # replace elements
            if isinstance(v, str) and (v in _replace_str_lut.keys()):
                v = _replace_str_lut[v]

            # handle other tags
            if ('<PATH>' in k) and (k is not None):
                k = k.replace('<PATH>', '')
                v = os.path.join(*v) if not isinstance(v, str) else v
                if '~' in v:
                    v = v.replace('~', f"/home/{os.environ['USER']}")
            if ('<IMPORT>' in k ) and (k is not None):
                k = k.replace('<IMPORT>', '')
                # Modules are strings.separated.by.dots:
                if isinstance(v, str):
                    v = importlib.import_module(v)
                elif isinstance(v, list):
                    # the first element is the module, then attributes
                    # of the module and attributes of the attributes (classes,
                    # and functions.
                    m = importlib.import_module(v[0])
                    for el in v[1:]:
                        m = getattr(m, el)
                    v = m
                else:
                    raise IOError(
                        "The <IMPORT> tag expects either a string to import"
                        "a module (e.g 'np.ma') or a list with 2 elements"
                        "['module.string', 'function_name'] to import a "
                        "class/function from a module "
                        "(e.g. ['np.ma', 'masked_array'] )")

            new_data[k] = v

    return new_data


def read_settings(settings_file, groups=None):
    """
    Parser for reading settings from the settings-yaml file.
    Parse <OS-identifiers> and <PATH> automatically to return correct path strings
    and OS dependent paths.

    Parameters
    -------
    settings_file : str
        Path to the settings yml file to read
    groups: list
        Name(s) of parameter groups to read. If none are passed, all are read.
        Groups are the names of the first level.

    Returns
    -------
    settings : dict
        Settings as parsed from the file.
    """

    with open(settings_file, 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.Loader)

    for level, data in cfg.items():
        cfg[level] = read_level(data)

    if groups is None:
        settings = cfg
    else:
        settings = {g: cfg[g] for g in groups}

    return settings


def spaceify(settings, sections=None):
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
    sections : str or list, optional (default: None)
        Name of sections in the settings (first level) to create Namespaces
        for. None creates Namespaces for all sections.

    Returns
    -------
    namespaces : Namespace or tuple[Namespace]
        Namespaces created from the passed settings for each dictionary layer.
        For a single section, the namespace is returned directly, otherwise
        a list is returned
    """

    if isinstance(settings, dict):
        sets = settings
    else:
        sets = read_settings(settings)

    if sections is None:
        sections = list(sets.keys())
    else:
        sections = np.atleast_1d(sections)

    nspacs = [Namespace(**sets[sec]) for sec in sections]

    if len(nspacs) == 1:
        return nspacs[0]
    else:
        return tuple(nspacs)


