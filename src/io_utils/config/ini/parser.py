from configparser import ConfigParser

import numpy as np
import pandas as pd
from ast import literal_eval
import re
import warnings
from io_utils.config.ini.conversion import (
    convert_tag_bool,
    convert_tag_datetime,
    convert_tag_dict,
    convert_tag_import,
    convert_tag_path,
    convert_tag_list,
    convert_tag_exec,
    convert_tag_eval,
)

default_tag_converters = {
    'bool': convert_tag_bool,
    'datetime': convert_tag_datetime,
    'dict': convert_tag_dict,
    'import': convert_tag_import,
    'path': convert_tag_path,
    'list': convert_tag_list,
    'exec': convert_tag_exec,
    'eval': convert_tag_eval,
}

class TemplateConfigParser:
    def __init__(
            self, cfg_file, cfg_template=None,
            tag_converters=default_tag_converters,
            allow_no_value=True,
        ):
        """
        Wrapper around ConfigParser to support tags to convert ini entries
        on-the-fly and template files to provide default values and help
        descriptions.

        Parameters
        ----------
        cfg_file: str or list
            Path to config file(s) to try to read. IF multiple are passed,
            any sections in later files will override those in earlier files.
            Files for which reading fails, are ignored.
        cfg_template: str or None, optional
            Path to config file with default values. These will be read first
            and then overwritten by values in cfg_file if included.
        tag_converters: dict or None, optional
            List of functions to apply to items with tags <TAGS> (dict keys).
            The functions (values) should take a key and value as input and
            return a tuple with the new key and value.
        allow_no_value: bool, optional
            Passed to ConfigParser.
        """
        self.cfg_file = cfg_file

        self.tag_converters = tag_converters
        self.parser = ConfigParser(
            converters={},
            inline_comment_prefixes=('#',),
            allow_no_value=allow_no_value,
        )

        if cfg_template is not None:
            self.defaults = TemplateConfigParser(
                cfg_template,
                cfg_template=None,
                allow_no_value=True,
                tag_converters=tag_converters,
            )
            if sorted(list(self.defaults.items.keys())) \
                    != ['DESCRIPTION', 'OPTIONAL', 'REQUIRED']:
                raise ValueError(
                    "cfg_template must contain sections: REQUIRED, OPTIONAL, "
                    "DESCRIPTION."
                )
        else:
            self.defaults = None

        self.items = self.parse()

    @property
    def sections(self) -> list:
        # List sections in config file after applying [DEFAULT]
        return list(self.items.keys())

    def get_all_keys(self, section=None) -> list:
        """
        Get all keys in the config file(s). If chosen, limited to a section.
        Duplicates are ignored.
        """
        keys = []
        if section is None:
            sections = self.items.keys()
        else:
            sections = np.atleast_1d(section)
        for section in sections:
            if section not in self.items.keys():
                raise ValueError(f"Section {section} not found.")
            keys += list(self.items[section].keys())
        return list(dict.fromkeys(keys))

    def apply_tags(self, items: dict):
        """
        Looks for <TAGS> in items replaces the items with converted versions.
        Recursively (in case of tags in sub-dicts).
        """
        pattern = r'<([^>]+)>'  # Match anything between < and > (TAGS)

        filtered_items = {}

        for key, value in items.items():
            has_tag = re.search(pattern, str(key))
            if has_tag:
                tag = has_tag.group(1)
                try:
                    value = literal_eval(value)
                except Exception:
                    pass
                new_key, new_value = self.tag_converters[tag](key, value)
                try:
                    new_value = literal_eval(new_value)
                except Exception:
                    pass
                if isinstance(new_value, dict):
                    new_value = self.apply_tags(new_value)
                if tag in new_key:
                    new_key = new_key.replace(f'<{tag}>', '')
                filtered_items[new_key] = new_value
            else:
                try:
                    value = literal_eval(value)
                except Exception:
                    pass
                if isinstance(value, dict):
                    value = self.apply_tags(value)
                filtered_items[key] = value

        return filtered_items

    @staticmethod
    def create_groups(items: dict) -> (dict, list):
        """
        Takes items from ini file and looks for {GROUPS} in the keys. If found,
        puts those group elements in a sub-dictionary.
        TODO: deprecate?
        """
        pattern = r'{([^>]+)}'  # Match anything between { and } {GROUPS}
        groups = {}
        filtered_items = {}
        for key, value in items.items():
            has_group = re.search(pattern, key)
            if has_group:
                group = has_group.group(1)
                if group not in groups:
                    groups[group] = {}
                new_key = key.replace(f'{{{group}}}', '')
                groups[group][new_key] = value
            else:
                filtered_items[key] = value

        filtered_items.update(groups)

        return filtered_items, list(groups.keys())

    def parse(self, sections=None, tags=True,
              override_settings=None):
        """
        Read config sections from file(s) and parse content based on <TAGS> and
        {GROUPS}. If a config_template file is provided, then the user config
        is validated against the template. Optional, missing fields are taken
        from the template. For fields that are not in the template, a warning
        is printed (unless their name starts with __).

        Parameters
        ----------
        sections: list, optional
            List of sections to read. If None, all sections are read.
        defaults: str, optional
            Path to file with default values. If None, no defaults are read.
        tags: bool, optional
            If True, apply <TAGS> conversions to items.
        override_settings: dict, optional
            Dictionary with settings to override. These will be applied before
            tags or grouping.

        Returns
        -------
        parsed_content: dict
            Dictionary with content read from ini files and (if selected) with
            <TAG> and {GROUP} functions applied.
        """
        _ = self.parser.read(self.cfg_file)
        if sections is None:
            sections = self.parser.sections()
        else:
            sections = np.atleast_1d(sections)

        if self.defaults is not None:
            required_keys = list(self.defaults.items['REQUIRED'].keys())
            optional_keys = list(self.defaults.items['OPTIONAL'].keys())
        else:
            optional_keys, required_keys = [], []

        parsed_content = {}

        for section in sections:

            parsed_content[section] = {}
            items = dict(self.parser[section])

            if override_settings is not None:
                items.update(override_settings)

            if tags:
                items = self.apply_tags(items)

            # Try parsing all strings to python types, if it fails keep string

            for key, value in items.items():
                if self.defaults is not None:
                    if not key.startswith('__') and \
                            (key not in optional_keys + required_keys):
                        warnings.warn(
                            f"Unexpected config field `{key}` in section [{section}]. "
                            f"Not found in process config template: "
                            f"{self.defaults.cfg_file}. "
                        )

                if isinstance(value, str):
                    try:
                        value = literal_eval(value)
                    except Exception:
                        pass
                    items[key] = value

            # if groups:
            #     items, groups = self.create_groups(items)

            parsed_content[section] = items

        self.items = parsed_content

        return self.items

    def get(self, key, section=None, ignore_defaults=False):
        """
        Read a single item from the config file. If a template is provided,
        and the field is not found in the user config, then the fallback value
        from the template is used.

        Parameters
        ----------
        key: str
            Key to read.
        section: str or int
            Section to read from. Only required if more than 1 section was
            found. Note: specify a section using _read_parsed first.
        ignore_defaults: bool, optional
            If True, ignore any default values from the template.
        """
        sections = list(self.items.keys())

        if section is None:
            if len(sections) > 1:
                raise ValueError("More than 1 section found. Please specify "
                                 "a section to read from.")
            else:
                section = sections[0]

        if isinstance(section, int):
            section = sections[section]

        if not ignore_defaults:
            required = self.defaults.items['REQUIRED'].keys()
            optional = self.defaults.items['OPTIONAL']
            description = self.defaults.items['DESCRIPTION']
        else:
            required, optional, description = [], dict(), dict()
        try:
            value = self.items[section][key]
        except KeyError:
            error = [f"No field `{key}` found in config section [{section}] "
                     f"at {self.cfg_file}. "]
            if ignore_defaults:
                raise ValueError(' '.join(error))
            try:
                description = "\n" + "Description: " + self.defaults.items['DESCRIPTION'][key]
            except KeyError:
                description = "\n" + "No description found."
            if key in self.defaults.items['REQUIRED'].keys():
                error.append(f"Field '{key}' is required and must be defined.")
                error.append(description)
                raise ValueError(' '.join(error))
            elif key in self.defaults.items['OPTIONAL'].keys():
                value = self.defaults.items['OPTIONAL'][key]
                error.append(f"Using found fallback value: {value}")
            else:
                error.append(f"No fallback value was found.")
                raise ValueError(' '.join(error))
        else:
            if not ignore_defaults:
                if key not in list(required) + list(optional.keys()) \
                        + list(description.keys()):
                    warnings.warn(f"Unexpected entry `{key}`. "
                                  f"Not found in template file. "
                                  f"Probably won't be used in process.")
        return value

