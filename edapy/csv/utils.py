"""Utility functions for edapy."""

# Third party
import pandas as pd
import yaml


def load_csv(csv_path: str, yaml_path: str) -> pd.DataFrame:
    """
    Load a CSV file as a Pandas dataframe.

    Parameters
    ----------
    csv_path : str
    yaml_path : str

    Returns
    -------
    df : pd.DataFrame
    """
    with open(yaml_path) as stream:
        csv_info = yaml.safe_load(stream)
    dtype_list = [(col["name"], col["dtype"]) for col in csv_info["columns"]]
    dtype = dict(dtype_list)
    delimiter = csv_info["csv_meta"]["delimiter"]
    df = pd.read_csv(csv_path, delimiter=delimiter, dtype=dtype)
    return df


def get_csv_delimiter(csv_path: str) -> str:
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
    reader = pd.read_csv(csv_path, sep=None, iterator=True, engine="python")
    inferred_delimiter = reader._engine.data.dialect.delimiter
    return inferred_delimiter


def get_quote_char(csv_path: str) -> str:
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
    reader = pd.read_csv(csv_path, sep=None, iterator=True, engine="python")
    inferred_quote_char = reader._engine.data.dialect.quotechar
    return inferred_quote_char
