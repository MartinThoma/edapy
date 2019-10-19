# Core Library
from datetime import datetime

# Third party
import pandas as pd

# First party
import edapy.csv


def test_make_path_absolute():
    df = pd.DataFrame(
        {
            "a": [1, 2, 3],
            "b": [1.0, 2.0, 3.0],
            "c": ["a", "b", "c"],
            "d": [datetime(2018, 1, 1), datetime(2018, 1, 2), datetime(2018, 1, 3)],
        }
    )
    out = edapy.csv.describe_pandas_df(df, dtype=None)
    exp = {"a": "int", "b": "float", "c": "str", "d": "time"}
    assert out == exp
