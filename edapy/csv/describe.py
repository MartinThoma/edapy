#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging


def describe_pandas_df(df, dtype=None):
    """
    Show basic information about a pandas dataframe.

    Parameters
    ----------
    df : Pandas Dataframe object
    dtype : dict
        Maps column names to types

    Returns
    -------
    column_types : dict
        Maps column names to type names
    """
    if dtype is None:
        dtype = {}
    print("Number of datapoints: {datapoints}".format(datapoints=len(df)))
    column_info = {'int': [], 'float': [], 'category': [], 'other': []}
    float_types = ['float64']
    integer_types = ['int64', 'uint8']
    other_types = ['object', 'category']
    column_info_meta = {}
    for column_name in df:
        column_info_meta[column_name] = {}
        counter_obj = df[column_name].groupby(df[column_name]).count()
        value_list = list(counter_obj.keys())
        value_count = len(value_list)
        is_suspicious_cat = (value_count <= 50 and
                             str(df[column_name].dtype) != 'category' and
                             column_name not in dtype)
        if is_suspicious_cat:
            logging.warning("Column '{}' has only {} different values ({}). "
                            "You might want to make it a 'category'"
                            .format(column_name,
                                    value_count,
                                    value_list))
        if len(value_list) > 0:
            top_count_val = counter_obj[value_list[0]]
        else:
            top_count_val = None
        column_info_meta[column_name]['top_count_val'] = top_count_val
        column_info_meta[column_name]['value_list'] = value_list
        column_info_meta[column_name]['value_count'] = value_count
        is_int_type = (df[column_name].dtype in integer_types or
                       column_name in dtype and
                       dtype[column_name] in integer_types)
        is_float_type = (df[column_name].dtype in float_types or
                         column_name in dtype and
                         dtype[column_name] in float_types)
        is_cat_type = (str(df[column_name].dtype) == 'category' or
                       column_name in dtype and
                       dtype[column_name] == 'category')
        is_other_type = (str(df[column_name].dtype) in other_types or
                         column_name in dtype and
                         dtype[column_name] in other_types)
        if is_int_type:
            column_info['int'].append(column_name)
        elif is_float_type:
            column_info['float'].append(column_name)
        elif is_cat_type:
            column_info['category'].append(column_name)
        elif is_other_type:
            column_info['other'].append(column_name)
        else:
            print("!!! describe_pandas_df does not know type '{}'"
                  .format(df[column_name].dtype))

    column_name_len = max(len(column_name) for column_name in df)

    print("\n## Integer Columns")
    print("{column_name:<{column_name_len}}: Non-nan  mean   std   min   25%  "
          " 50%   75%   max"
          .format(column_name_len=column_name_len,
                  column_name="Column name"))
    for column_name in column_info['int']:
        print("{column_name:<{column_name_len}}: {non_nan:>7}  "
              "{mean:0.2f}  {std:>4.2f}  "
              "{min:>4.0f}  {q25:>4.0f}  {q50:>4.0f}  {q75:>4.0f}  {max:>4.0f}"
              .format(column_name_len=column_name_len,
                      column_name=column_name,
                      non_nan=sum(df[column_name].notnull()),
                      mean=df[column_name].mean(),
                      std=df[column_name].std(),
                      min=df[column_name].min(),
                      q25=df[column_name].quantile(0.25),
                      q50=df[column_name].quantile(0.50),
                      q75=df[column_name].quantile(0.75),
                      max=max(df[column_name])))

    print("\n## Float Columns")
    print("{column_name:<{column_name_len}}: Non-nan   mean    std    min    "
          "25%    50%    75%    max"
          .format(column_name_len=column_name_len,
                  column_name="Column name"))
    for column_name in column_info['float']:
        print("{column_name:<{column_name_len}}: {non_nan:>7}  "
              "{mean:5.2f}  {std:>4.2f}  "
              "{min:>5.2f}  {q25:>5.2f}  {q50:>5.2f}  {q75:>5.2f}  {max:>5.2f}"
              .format(column_name_len=column_name_len,
                      column_name=column_name,
                      non_nan=sum(df[column_name].notnull()),
                      mean=df[column_name].mean(),
                      std=df[column_name].std(),
                      min=df[column_name].min(),
                      q25=df[column_name].quantile(0.25),
                      q50=df[column_name].quantile(0.50),
                      q75=df[column_name].quantile(0.75),
                      max=max(df[column_name])))

    if len(column_info['category']) > 0:
        print("\n## Category Columns")
        print("{column_name:<{column_name_len}}: Non-nan   unique   "
              "top (count)  rest"
              .format(column_name_len=column_name_len,
                      column_name="Column name"))
    for column_name in column_info['category']:
        # print(df[column_name].describe())
        rest_str = str(column_info_meta[column_name]['value_list'][1:])[:40]
        print("{column_name:<{column_name_len}}: {non_nan:>7}   {unique:>6}   "
              "{top} ({count})  {rest}"
              .format(column_name_len=column_name_len,
                      column_name=column_name,
                      non_nan=sum(df[column_name].notnull()),
                      unique=len(df[column_name].unique()),
                      top=column_info_meta[column_name]['value_list'][0],
                      count=column_info_meta[column_name]['top_count_val'],
                      rest=rest_str))

    print("\n## Other Columns")
    print("{column_name:<{column_name_len}}: Non-nan   unique   top (count)"
          .format(column_name_len=column_name_len,
                  column_name="Column name"))
    for column_name in column_info['other']:
        rest_str = str(column_info_meta[column_name]['value_list'][1:])[:40]
        print("{column_name:<{column_name_len}}: {non_nan:>7}   {unique:>6}   "
              "{top} ({count})"
              .format(column_name_len=column_name_len,
                      column_name=column_name,
                      non_nan=sum(df[column_name].notnull()),
                      unique=len(df[column_name].unique()),
                      top=column_info_meta[column_name]['value_list'][0],
                      count=column_info_meta[column_name]['top_count_val']))

    column_types = {}
    for column_type, columns in column_info.items():
        for column_name in columns:
            if column_type == 'other':
                column_type = 'str'
            column_types[column_name] = column_type
    return column_types
