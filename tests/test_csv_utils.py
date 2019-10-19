# Third party
from pkg_resources import resource_filename

# First party
from edapy.csv import utils


def test_load_csv():
    csv_path = resource_filename(__name__, "data/example.csv")
    yaml_path = resource_filename(__name__, "data/example_types.yaml")
    utils.load_csv(csv_path, yaml_path)


def test_get_csv_delimiter():
    csv_path = resource_filename(__name__, "data/example.csv")
    csv_delimiter = utils.get_csv_delimiter(csv_path)
    assert csv_delimiter == ","


def test_get_quote_char():
    csv_path = resource_filename(__name__, "data/example.csv")
    quote_char = utils.get_quote_char(csv_path)
    assert quote_char == '"'
