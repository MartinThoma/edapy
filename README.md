[![PyPI version](https://badge.fury.io/py/edapy.svg)](https://badge.fury.io/py/edapy)
[![Python Support](https://img.shields.io/pypi/pyversions/edapy.svg)](https://pypi.org/project/edapy/)
[![Build Status](https://travis-ci.org/MartinThoma/edapy.svg?branch=master)](https://travis-ci.org/MartinThoma/edapy)
[![Coverage Status](https://coveralls.io/repos/github/MartinThoma/edapy/badge.svg?branch=master)](https://coveralls.io/github/MartinThoma/edapy?branch=master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![GitHub last commit](https://img.shields.io/github/last-commit/MartinThoma/edapy)
![GitHub commits since latest release (by SemVer)](https://img.shields.io/github/commits-since/MartinThoma/edapy/0.3.0)
[![CodeFactor](https://www.codefactor.io/repository/github/martinthoma/edapy/badge/master)](https://www.codefactor.io/repository/github/martinthoma/edapy/overview/master)

edapy is a first resource to analyze a new dataset.

## Installation

```
$ pip install git+https://github.com/MartinThoma/edapy.git
```

For the pdf part, you also need `pdftotext`:

```
$ sudo apt-get install poppler-utils
```


## Usage

```
$ edapy --help
Usage: edapy [OPTIONS] COMMAND [ARGS]...

  edapy is a tool for exploratory data analysis with Python.

  You can use it to get a first idea what a CSV is about or to get an
  overview over a directory of PDF files.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  csv     Analyze CSV files.
  images  Analyze image files.
  pdf     Analyze PDF files.
```

The workflow is as follows:

* `edapy pdf find --path . --output results.csv` creates a `results.csv`
  for you. This `results.csv` contains meta data about all PDF files in the
  `path` directory.
* `edapy csv predict --csv_path my-new.csv --types types.yaml` will start /
  resume a process in which the user is lead through a series of questions. In
  those questions, the user has to decide which delimiter, quotechar is used
  and which types the columns have.
* `edapy` generates a `types.yaml` file which can be used to load the CSV in
  other applications with `df = edapy.load_csv(csv_path, yaml_path)`.


## Example types.yaml

For the [Titanic Dataset](https://www.kaggle.com/c/titanic/data), the resulting
`types.yaml` looks as follows:

```
columns:
- dtype: other
  name: Name
- dtype: int
  name: Parch
- dtype: float
  name: Age
- dtype: other
  name: Ticket
- dtype: float
  name: Fare
- dtype: int
  name: PassengerId
- dtype: other
  name: Cabin
- dtype: other
  name: Embarked
- dtype: int
  name: Pclass
- dtype: int
  name: Survived
- dtype: other
  name: Sex
- dtype: int
  name: SibSp
csv_meta:
  delimiter: ','
```

A sample run then would look like this:

```
$ edapy csv predict --types types_titanik.yaml --csv_path train.csv
Number of datapoints: 891
2018-04-16 21:51:56,279 WARNING Column 'Survived' has only 2 different values ([0, 1]). You might want to make it a 'category'
2018-04-16 21:51:56,280 WARNING Column 'Pclass' has only 3 different values ([3, 1, 2]). You might want to make it a 'category'
2018-04-16 21:51:56,281 WARNING Column 'Sex' has only 2 different values (['male', 'female']). You might want to make it a 'category'
2018-04-16 21:51:56,282 WARNING Column 'SibSp' has only 7 different values ([0, 1, 2, 4, 3, 8, 5]). You might want to make it a 'category'
2018-04-16 21:51:56,283 WARNING Column 'Parch' has only 7 different values ([0, 1, 2, 5, 3, 4, 6]). You might want to make it a 'category'
2018-04-16 21:51:56,285 WARNING Column 'Embarked' has only 3 different values (['S', 'C', 'Q']). You might want to make it a 'category'

## Integer Columns
Column name: Non-nan  mean   std   min   25%   50%   75%   max
PassengerId:     891  446.00  257.35     1   224   446   668   891
Survived   :     891  0.38  0.49     0     0     0     1     1
Pclass     :     891  2.31  0.84     1     2     3     3     3
SibSp      :     891  0.52  1.10     0     0     0     1     8
Parch      :     891  0.38  0.81     0     0     0     0     6

## Float Columns
Column name: Non-nan   mean    std    min    25%    50%    75%    max
Age        :     714  29.70  14.53   0.42  20.12  28.00  38.00  80.00
Fare       :     891  32.20  49.69   0.00   7.91  14.45  31.00  512.33

## Other Columns
Column name: Non-nan   unique   top (count)
Name       :     891      891   Goldschmidt, Mr. George B (1)
Sex        :     891        2   male (577)
Ticket     :     891      681   347082 (7)
Cabin      :     204      148   C23 C25 C27 (4)
Embarked   :     889        4   S (644)
```
