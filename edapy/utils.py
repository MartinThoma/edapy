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
