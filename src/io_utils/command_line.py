import click
from io_utils.yml.dependency_merger import run as merge_yml


@click.group(short_help="io_utils programs")
def io_utils():
    pass

io_utils.add_command(merge_yml)
