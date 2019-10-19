# Core Library
import os
import tempfile

# Third party
from click.testing import CliRunner
from pkg_resources import resource_filename

# First party
from edapy import cli


def test_cli_csv_predict():
    runner = CliRunner()
    csv_path = resource_filename(__name__, "data/example.csv")
    csv_types_path = resource_filename(__name__, "data/example_types.yaml")
    command = ["csv", "predict", "--csv_path", csv_path, "--types", csv_types_path]
    result = runner.invoke(cli.entry_point, command)
    assert result.exit_code == 0, "edapy " + " ".join(command)


def test_cli_images_find():
    runner = CliRunner()
    data_directory = resource_filename(__name__, "data/")
    _, out_file = tempfile.mkstemp(prefix="edapy_images_", suffix=".csv")
    command = ["images", "find", "--path", data_directory, "--output", out_file]
    result = runner.invoke(cli.entry_point, command)
    assert result.exit_code == 0, "edapy " + " ".join(command)
    os.remove(out_file)
