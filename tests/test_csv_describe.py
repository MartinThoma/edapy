# Core Library
from datetime import datetime

# Third party
import pandas as pd

# First party
import edapy.csv


def test_describe_pandas_df():
    df = pd.DataFrame(
        {
            "a": [1, 2, 3, 4],
            "b": [1.0, 2.0, 3.0, 3.0],
            "c": ["a", "b", "c", "b"],
            "d": [
                datetime(2018, 1, 1),
                datetime(2018, 1, 2),
                datetime(2018, 1, 3),
                datetime(2018, 1, 4),
            ],
        }
    )
    out = edapy.csv.describe_pandas_df(df, dtype=None)
    exp = {"a": "int", "b": "float", "c": "str", "d": "time"}
    assert out == exp


def test_generate_column_info():
    df = pd.DataFrame(
        {
            "a": [1, 2, 3, 4],
            "b": [1.0, 2.0, 3.0, 3.0],
            "c": ["a", "b", "c", "b"],
            "d": [
                datetime(2018, 1, 1),
                datetime(2018, 1, 2),
                datetime(2018, 1, 3),
                datetime(2018, 1, 4),
            ],
        }
    )
    column_info, column_info_meta = edapy.csv.describe._generate_column_info(
        df, dtype={}
    )
    column_info_expected = {
        "int": ["a"],
        "float": ["b"],
        "other": ["c"],
        "time": ["d"],
        "category": [],
    }
    assert column_info == column_info_expected
    assert column_info_meta["a"]["top_count_val"] == 1
    assert column_info_meta["a"]["value_count"] == 4
    assert sorted(column_info_meta["a"]["value_list"]) == sorted([1, 2, 3, 4])
    assert column_info_meta["b"]["top_count_val"] == 2
    assert column_info_meta["b"]["value_count"] == 3
    assert column_info_meta["c"]["top_count_val"] == 2
    assert column_info_meta["c"]["value_count"] == 3
