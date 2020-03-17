"""
Find which feature type a CSV has.

When analyzing features, you can distinguish the following:

categorical (nominal):
    - dtype: str
    - Not orderable
    - Meaningful statistics:
        - most frequent element (mode)
        - Frequency plot
    - NOT meaningful statistics:
        - Histogram
    - Examples:
        - Colors: Red, green, blue
        - Sex: male, female
ordinal:
    - dtype: str or int
    - orderable
    - Meaningful statistics:
        - most frequent element
        - Median value
    - Not meaningful:
        - arithmetic mean (average)
    - Examples:
        - Grades: 1, 2, 3, 4, 5, 6 or A, B, C, D
interval:
    - dtype: int or float
    - orderable
    - Addition and subtraction makes sense
    - Meaningful statistics:
        - arithmetic mean
        - Deviation
    - Examples:
        - Temperature in C
ratio:
    - dtype: float
    - orderable, addition and subtractoin makes sense
    - A ratio scale possesses a meaningful (unique and non-arbitrary) zero
      value.
    - multiplication and division makes sense
    - Meaningful statistics
        - mode, median, and arithmetic mean
        - Geometric Mean
        - harmonic mean
        - studentized range, Coeff. of Variation
    - Examples:
        - Length in cm
        - Temperature in K
datetime:
    - in principle an interval scale variable, but important enough the be
      treated by its own
coordinate:
    - in principle an interval scale variable, but important enough the be
      treated by its own


To be considered:

* Cyclical ratio: Hours
"""

# Core Library
import collections
import numbers
import operator
from typing import Any, Dict, List

# Third party
import numpy as np
import pandas as pd

types = ["int", "float", "category", "date", "bool", "text", "identifier"]


def find_type(df) -> List[Dict]:
    """
    Figure out the types of a pandas dataframe.

    Parameters
    ----------
    df : Pandas dataframe

    Returns
    -------
    columns : List[Dict]
        One dict for each column
    """
    columns = []
    for column_name in df:
        examples = df[column_name].value_counts().head(3).index.tolist()
        processed_examples = []
        for el in examples:
            if isinstance(el, bool):
                el = el  # do nothing
            if isinstance(el, (float, int, np.float32, np.float64, np.int64)):
                try:
                    el = el.item()
                except Exception:
                    pass
            elif not isinstance(el, (bool,)):
                el = str(el)
            processed_examples.append(el)
        entry: Dict[str, Any] = collections.OrderedDict()
        entry["name"] = column_name
        probabilities = get_type_probabilities(df[column_name], column_name)
        entry["type"] = argmax(probabilities)
        entry["dtype"] = str(df[column_name].dtype)
        entry["examples"] = processed_examples
        if np.issubdtype(df[column_name].dtype, np.number):
            entry["min"] = float(df[column_name].min())
            entry["max"] = float(df[column_name].max())
        columns.append(entry)
    return columns


def argmax(dict_: Dict):
    """
    Get the argmax.

    Parameters
    ----------
    dict_ : dict

    Returns
    -------
    argmax : tuple

    Example
    -------
    >>> argmax({'a': 10, 'b': 70, 'c': 20})
    'b'
    """
    return max(dict_.items(), key=operator.itemgetter(1))[0]


def normalize(dict_: Dict) -> Dict:
    """
    Normalize the values of a dict.

    Parameters
    ----------
    dict_ : Dict

    Returns
    -------
    argmax : Dict

    Example
    -------
    >>> sorted(normalize({'a': 10, 'b': 70, 'c': 20}).items())
    [('a', 0.1), ('b', 0.7), ('c', 0.2)]
    """
    sum_ = sum(value for key, value in dict_.items())
    dict_ = {key: value / float(sum_) for key, value in dict_.items()}
    return dict_


def has_frac(df_column: pd.Series) -> bool:
    """
    Check if one of the values is a fraction.

    Parameters
    ----------
    df_column : pd.Series

    Returns
    -------
    has_fraction : bool

    Examples
    --------
    >>> has_frac(pd.Series([1.0, 2.0]))
    False
    >>> has_frac(pd.Series([1.0, 2.1]))
    True
    """
    epsilon = 10 ** -4
    for el in df_column.tolist():
        if not isinstance(el, numbers.Number):
            return False
        rounded = round(el)  # type: ignore
        if abs(el - rounded) > epsilon:
            return True
    return False


def get_type_probabilities(column: pd.Series, column_name: str) -> Dict[str, float]:
    """
    Estimate how likely the different types are.

    Parameters
    ----------
    column : pd.Series
    column_name : str

    Returns
    -------
    type_probabilites : Dict[str, float]
        maps (type name => probability)
    """
    type_probs = {type_name: 1.0 / len(types) for type_name in types}
    unique_values = len(column.value_counts())
    if unique_values > 2:
        type_probs["bool"] = 0
    else:
        type_probs["bool"] *= 2
    if np.issubdtype(column.dtype, np.number):
        if has_frac(column):
            type_probs["int"] = 0
            type_probs["category"] /= 2
            type_probs["date"] /= 2
        if np.issubdtype(column.dtype, np.int64):
            type_probs["int"] *= 2
    else:
        type_probs["float"] = 0
        type_probs["int"] = 0
        column_lower = column_name.lower()
        if "date" in column_lower or "time" in column_lower:
            type_probs["date"] *= 2
        if "_id" in column_lower or "id" == column_lower:
            type_probs["identifier"] *= 2
        if "description" in column_lower:
            type_probs["text"] *= 2
    return normalize(type_probs)


def _get_scores(df, column_name):
    pass
