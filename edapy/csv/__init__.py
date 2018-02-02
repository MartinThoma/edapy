#!/usr/bin/env python

"""Module for exploratory data analysis of CSV files."""

# core modules
import os
import sys
import collections
import io
import yaml

# 3rd party modules
import click
import pandas as pd

# internal modules
from edapy.csv.utils import get_quote_char, get_csv_delimiter
from edapy.csv.describe import describe_pandas_df
from edapy.csv.interactive_type_finder import find_type
from edapy.csv.utils import load_csv  # noqa


###############################################################################
# CLI                                                                         #
###############################################################################
@click.group(name='csv')
def entry_point():
    """Analyse CSV files."""
    pass


###############################################################################
# Logic                                                                       #
###############################################################################
@entry_point.command(name='predict')
@click.option('--csv_path',
              help='CSV file to read',
              required=True,
              type=click.Path(exists=True))
@click.option('--types',
              help='YAML file to read / write',
              required=True,
              type=click.Path())
@click.option('--nrows',
              help='Number of rows to read. By default, read all lines',
              type=int)
def main(csv_path, types, nrows=None):
    """
    Start the CSV recognizing.

    Parameters
    ----------
    csv_path : str
    types : str
    nrows : int (default: all rows)
    """
    csv_path = os.path.abspath(csv_path)
    types = os.path.abspath(types)
    if not os.path.isfile(csv_path):
        print("Could not find '{}'.".format(csv_path))
        sys.exit(1)
    if not os.path.isfile(types):
        df = pd.read_csv(csv_path, sep=None, engine='python', nrows=nrows)
        data = collections.OrderedDict()
        data['csv_meta'] = {'delimiter': get_csv_delimiter(csv_path),
                            'quotechar': get_quote_char(csv_path)}
        data['columns'] = find_type(df)
        _write_yaml(types, data)
    else:
        df = pd.read_csv(csv_path, sep=None, engine='python', nrows=nrows)
        data = _read_yaml(types)
    describe_pandas_df(df)
    _write_yaml(types, data)


def _write_yaml(yaml_path, data):
    with io.open(yaml_path, 'w', encoding='utf8') as outfile:
        yaml.dump(data, outfile, default_flow_style=False, allow_unicode=True)


def _read_yaml(yaml_path):
    with open(yaml_path, 'r') as stream:
        data_loaded = yaml.load(stream)
    return data_loaded


def _load_dtype(data):
    dtype = {}
    for el in data['columns']:
        print(el)
        if 'type' in el:
            dtype[el['name']] = el['type']
        elif 'dtype' in el:
            dtype[el['name']] = el['dtype']
    return dtype
