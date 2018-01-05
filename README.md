This package is intendet to be a first resource to go when one has a new
dataset.

## Installation

```
$ pip install git+https://github.com/MartinThoma/edapy.git
```


## Core Features

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