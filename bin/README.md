This package is intendet to be a first resource to go when one has a new
dataset.

## Core Features

The workflow is as follows:

* `edapy --csv my-new.csv --types types.yaml` will start / resume a process in which
  the user is lead through a series of questions. In those questions, the user
  has to decide which delimiter, quotechar is used and which types the columns
  have.
* `edapy` generates a `types.yaml` file which can be used to load the CSV in
  other applications with `df = edapy.load_csv(csv_path, yaml_path)`.
*