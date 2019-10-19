# Core Library
import datetime as dt

# Third party
import pandas as pd
import pytest

# First party
from edapy.csv.interactive_type_finder import find_type, get_type_probabilities


def example_df():
    """Create an example dataframe."""
    country_names = ["Germany", "France", "Indonesia", "Ireland", "Spain", "Vatican"]
    population = [82521653, 66991000, 255461700, 4761865, 46549045, None]
    population_time = [
        dt.datetime(2016, 12, 1),
        dt.datetime(2017, 1, 1),
        dt.datetime(2017, 1, 1),
        None,  # Ireland
        dt.datetime(2017, 6, 1),  # Spain
        None,
    ]
    euro = [True, True, False, True, True, True]
    df = pd.DataFrame(
        {
            "country": country_names,
            "population": population,
            "population_time": population_time,
            "EUR": euro,
        }
    )
    df = df[["country", "population", "population_time", "EUR"]]
    return df


def test_get_type_probabilities():
    df = example_df()
    type_probabilities = get_type_probabilities(df.country, "Country")
    assert type_probabilities["int"] == 0.0
    assert type_probabilities["float"] == 0.0
    assert type_probabilities["bool"] == 0.0
    assert type_probabilities["text"] > 0.0
    assert type_probabilities["category"] > 0.0
    assert type_probabilities["identifier"] > 0.0
    assert pytest.approx(sum(type_probabilities.values())) == 1.0


@pytest.mark.xfail(reason="Bug in find_type")
def test_find_type():
    df = example_df()
    types = find_type(df)
    assert len(types) == len(df.columns)
    # expected_types = [
    #     OrderedDict(
    #         [
    #             ("name", "country"),
    #             ("type", "category"),
    #             ("dtype", "object"),
    #             ("examples", ["Indonesia", "France", "Ge...-06-01 00:00:00"]),
    #         ]
    #     ),
    #     OrderedDict(
    #         [
    #             ("name", "EUR"),
    #             ("type", "bool"),
    #             ("dtype", "bool"),
    #             ("examples", [True, False]),
    #         ]
    #     ),
    # ]
    # assert types == expected_types
