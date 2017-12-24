#!/usr/bin/env python

"""Utility functions for edapy."""

# 3rd party modules
import yaml
import pandas as pd


def load_csv(csv_path, yaml_path):
    """
    Load a CSV file as a Pandas dataframe.

    Parameters
    ----------
    csv_path : str
    yaml_path : str
    """
    # Read YAML file
    with open(yaml_path, 'r') as stream:
        csv_info = yaml.load(stream)
    dtype = [(col['name'], col['dtype']) for col in csv_info['columns']]
    dtype = dict(dtype)
    df = pd.read_csv(csv_path,
                     delimiter=csv_info['csv_meta']['delimiter'],
                     dtype=dtype)
    return df


def get_csv_delimiter(csv_path):
    """
    Find which delimiter was used in a CSV file.

    Parameters
    ----------
    csv_path : str

    Returns
    -------
    inferred_delimiter : str
        e.g. ';'
    """
    inferred_delimiter = None
    reader = pd.read_csv(csv_path, sep=None, iterator=True, engine='python')
    inferred_delimiter = reader._engine.data.dialect.delimiter
    return inferred_delimiter


def get_quote_char(csv_path):
    """
    Find which quotation character was used in a CSV file.

    Parameters
    ----------
    csv_path : str

    Returns
    -------
    inferred_quote_char : str
        e.g. '"'
    """
    inferred_quote_char = None
    reader = pd.read_csv(csv_path, sep=None, iterator=True, engine='python')
    inferred_quote_char = reader._engine.data.dialect.quotechar
    return inferred_quote_char
