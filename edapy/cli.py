#!/usr/bin/env python

"""
edapy is a tool for exploratory data analysis with Python.

You can use it to get a first idea what a CSV is about or to get an overview
over a directory of PDF files.
"""

# Core Library
import collections
import logging
import sys

# Third party
import click
import yaml

# First party
import edapy.csv
import edapy.images
import edapy.pdf

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.DEBUG,
    stream=sys.stdout,
)


def setup_yaml() -> None:
    """
    Make yaml.dump print collections.OrderedDict the right way.

    https://stackoverflow.com/a/8661021
    """
    yaml.add_representer(collections.OrderedDict, _represent_dict_order)


def _represent_dict_order(self, data):
    return self.represent_mapping("tag:yaml.org,2002:map", data.items())


setup_yaml()


@click.group(help=__doc__)
@click.version_option(version=edapy.__version__)
def entry_point() -> None:
    """Exploratory data analysis tool."""


entry_point.add_command(edapy.csv.entry_point)
entry_point.add_command(edapy.pdf.entry_point)
entry_point.add_command(edapy.images.entry_point)


if __name__ == "__main__":
    entry_point()
