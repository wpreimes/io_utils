"""
This module contains a collection of predefined conversion functions to
handle <TAGS> in config files. A selection of functions can be passed to the

"""
from datetime import datetime
import pandas as pd
from ast import literal_eval
from typing import Callable, Any
import os
import warnings
import importlib

class TagConversionError(ValueError):
    pass

def str2bool(s):
    """
    Convert passed string to boolean type.
    """
    _true = ['yes', 'on', 'true', '1']
    _false = ['no', 'off', 'false', '0']
    if s.lower() in _true:
        return True
    elif s.lower() in _false:
        return False
    else:
        raise ValueError(f"Invalid boolean string: {s}",
                         f"Allowed values are: {_true + _false}")

def str2dict(s):
    """
    Convert passed string to dict type.
    """
    if s[0] != '{':
        s = '{' + s
    if s[-1] != '}':
        s += '}'
    return literal_eval(s)

def convert_tag_exec(key: str, value:str) -> (str, None):
    try:
        exec(value)
    except Exception as e:
        raise TagConversionError(f"Invalid exec string at {key}: {value}. "
                                 f"Raised: {e}")
    return key, None

def convert_tag_eval(key: str, value: str) -> (str, Any):
    """
    Apply eval to the passed string
    """
    if not isinstance(value, str):
        return key, value
    try:
        value = literal_eval(value)
    except Exception:
        try:
            value = eval(value)
        except Exception as e:
            raise TagConversionError(f"Invalid eval string: {value}: {e}")

    return key, value


def convert_tag_list(key, value) -> (str, list):
    """
    Converts the passed string to list type, numbers and bools in the list
    are also converted to their appropriate types.
    """
    elements = value.strip('[]').split(',')
    elements = [element.strip() for element in elements]

    # Convert elements to their appropriate types
    converted_elements = []
    for element in elements:
        try:
            converted_element = literal_eval(element)
        except ValueError:
            # If the element is not a valid literal, keep it as a string
            converted_element = element
        converted_elements.append(converted_element)

    return key, converted_elements

def convert_tag_dict(key: str, value: str) -> (str, dict):
    """
    Converts the passed string to dict type, numbers and bools, etc. in the
    dict are also converted to their appropriate types.
    """
    # Evaluate the string using ast.literal_eval
    try:
        result_dict = str2dict(value)
    except (SyntaxError, ValueError):
        raise TagConversionError(f"Invalid dictionary string: {value}")

    # Check if the result is a dictionary
    if not isinstance(result_dict, dict):
        raise TagConversionError(f"Invalid dictionary string: {value}")

    # Return the dictionary object
    return key, result_dict

def convert_tag_path(key: str, value: str) -> (str, str):
    """
    Converts the passed string to a path.

    - Remove any white spaces in path strings
    - Commas can be used to separate path elements (os independent)
    - Expand ~ to home directory (on linux)
    - Windows: Drive letters are followed up with \\

    Parameters:
    -----------
    item: str
        String to be converted to a path object.
        Can either be a absolute windows or linux path.
        e.g. '/tmp/test' or 'C:\Temp\test' or comma separated path elements
        e.g. '/tmp, test' or 'C:, Temp, test'
    """
    # Here we apply special rules to the path elements
    # Remove any white spaces in path strings
    path = value.replace(' ', '')
    # Commas can be used to separate path elements (os independent)
    path = path.split(',')

    # Expand ~ to home directory (on linux)
    if path[0].startswith('~'):
        path[0] = path[0].replace('~', f"/home/{os.environ['USER']}")
    # Windows: Drive letters are followed up with \\
    elif path[0][-1] == ':':
        path[0] += '\\'

    path = os.path.join(*path[0:])

    return key, path


def convert_tag_import(key: str, value: str) -> (str, Callable):
    """
    Converts the passed value to an imported Callable (class or function).
    """
    try:
        if ',' in value:
            value = value.replace(' ', '').split(',')
        if isinstance(value, list):
            m = importlib.import_module(value[0])
            for el in value[1:]:
                m = getattr(m, el)
            value = m
        else:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                module_name = value[:value.rfind('.')]
                class_name = value[value.rfind('.') + 1:]
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    module = __import__(module_name, fromlist=[class_name])
                    value = getattr(module, class_name)
    except Exception as e:
        raise TagConversionError(f"Could not import '{key}: {value}': {e}.")

    return key, value

def convert_tag_datetime(key: str, value: str) -> (str, datetime):
    """
    Uses pandas to convert value to datetime.
    This can by default handle a large variety of strings, e.g.
    "1.1.2020", "1 Jan 2020", "2020-01-01", "2020-01-01 00:00:00", ...
    """
    try:
        dt = pd.to_datetime(value).to_pydatetime()
    except Exception as e:
        raise TagConversionError(f"Could not convert '{key}: {value}' to datetime: "
                                 f"{e}")

    return key, dt


def convert_tag_bool(key: str, value: str) -> (str, bool):
    """
    Handle the <BOOL> tag, same as the getboolean method. I.e. bool for
    'yes'/'no', 'on'/'off', 'true'/'false' and '1'/'0
    """
    try:
        value = str2bool(value)
    except ValueError as e:
        TagConversionError(f"Could not convert '{value}' to boolean "
                           f"for key '{key}': {e}")
    return key, value
