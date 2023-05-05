from parse import *
import yaml
import re
import click

def find_post_release_package(item):
    """
    Checks whether the string refers to a post release of a package.

    Parameters
    ----------
    item: str
        A package string from a yaml file

    Returns
    -------
    is_post: bool
        True if the string refers to a post release
    named: dict
        A dictionary of the named elements of the string.
        One element is called "name" and contains the name of the package.
    """
    r = parse("{name}=={version}.post{x}.dev{rest}", item)
    if r is not None:
        r = r.named
        r['original'] = item
        return True, r
    else:
        return False, None

def find_git_url_package(item):
    """
    Checks if the string refers to a git url of a package of the passed name.
    The URL looks like this git+https://blable.com/path/to/package@tag

    Parameters
    ----------
    item: str
        A package string from a yaml file

    Returns
    -------
    is_git: bool
        True if the string refers to a git url
    named: dict
        A dictionary of the named elements of the string.
        One element is called "name" and contains the name of the package.

    """
    pattern = r"^git\+.*\/([^/]+)$"
    r = re.search(pattern, item)

    if r is not None:
        r = {'nametag': r.group(1)}
        if "@" in r["nametag"]:
            name, tag = r["nametag"].split("@")
            r["name"] = name
            r["tag"] = tag
        else:
            r["name"] = r["nametag"]
        r["original"] = item
        return True, r
    else:
        return False, None


def replace_string_in_dict(data, old_str, new_str):
    """
    Recursively searches through a nested dictionary and replaces all
    occurrences of `old_str` with `new_str`.

    Parameters:
    data : dict or list or str
        The nested dictionary to search through.
    old_str : str
        The string to replace.
    new_str : str
        The string to replace `old_str` with.

    Returns:
    dict or list or str
        The modified nested dictionary with all occurrences of `old_str`
        replaced by `new_str`.
    """
    if isinstance(data, dict):
        for k, v in data.items():
            data[k] = replace_string_in_dict(v, old_str, new_str)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            data[i] = replace_string_in_dict(item, old_str, new_str)
    elif isinstance(data, str):
        data = data.replace(old_str, new_str)

    return data

class YmlMerger:
    def __init__(self, source_file, target_file):
        with open(source_file, 'r') as f:
            self.source_cont = yaml.load(f, Loader=yaml.FullLoader)
        with open(target_file, 'r') as f:
            self.target_cont = yaml.load(f, Loader=yaml.FullLoader)

    def parse_cont(self, cont, condition, **kwargs) -> dict:
        """
        Apply condition function to parse content of row and find lines
        to replace.

        Parameters
        ----------
        cont: dict or list or str
            Content of the yaml file (or a sublevel)
        condition: function
            Function to parse the content of a row
        kwargs:
            Additional arguments to pass to the condition function

        Returns
        -------
        ret: dict
            Dictionary of parsed lines
        """
        ret = dict()

        if isinstance(cont, str):
            satisfied, named = condition(cont, **kwargs)
            if satisfied:
                name = named.pop('name')
                return {name: named}
            else:
                return dict()
        else:
            if isinstance(cont, list):
                cont = {0: cont}
            for key, row in cont.items():
                if isinstance(row, str):
                    row = [row]
                for e in row:
                    ret.update(self.parse_cont(e, condition, **kwargs))

        return ret

    def transfer_to_target(
            self,
            source_condition=find_git_url_package,
            target_condition=find_post_release_package,
    ):
        """
        Merge the source file into the target file.

        Parameters
        ----------
        source_condition: function
            Validate and parse the name from the source file (with URL)
        target_condition: function
            Validate and parse the name from the target file (with ...post1...)

        Returns
        -------

        """

        source_replacements = self.parse_cont(
            self.source_cont, source_condition)
        target_to_replace = self.parse_cont(
            self.target_cont, target_condition)

        for name, target in target_to_replace.items():
            if name in source_replacements:
                # self.target_cont['dependencies'][-1]['pip'][38]
                self.target_cont = replace_string_in_dict(
                    self.target_cont,
                    target_to_replace[name]['original'],
                    source_replacements[name]['original'])

    def dump_target(self, target_file):
        with open(target_file, 'w') as f:
            yaml.dump(self.target_cont, f, sort_keys=False)

@click.command("merge_yml", short_help="Replace post build packages with URL in yml.")
@click.argument('source_file',
                type=click.Path())
@click.argument('target_file',
                type=click.Path())
def run(source_file, target_file):
    """
    Replace post build packages in target_file with URL in source_file.

    \b
    Parameters
    ----------
    SOURCE_FILE: string
        Path to the source yaml file
    TARGET_FILE: string
        Path to the target yaml file
    """
    # the docstring here is a little bit different because of click
    # integration, proper help on the command line seems more important than
    # the python docstring in this case.

    merger = YmlMerger(source_file, target_file)
    merger.transfer_to_target(source_condition=find_git_url_package,
                              target_condition=find_post_release_package)
    merger.dump_target(target_file)

