"""edapy: Exploratory data analysis in Python."""

# Third party
from setuptools import setup

requires_tests = [
    "pytest",
    "pytest-black",
    # coverage is a transitive requirement of pytest-cov;
    # it is pinned due to https://github.com/nedbat/coveragepy/issues/883
    "coverage<5.0.0",
    "pytest-cov",
    "pytest-flake8",
    "pytest-mccabe",
    "simplejson",
]
requires_all = requires_tests


# If you adjust any of the following, run `pip-compile` to update the
# requirements.txt
# You can find `pip-compile` in https://github.com/jazzband/pip-tools

setup(
    extras_require={"all": requires_all, "tests": requires_tests},
    install_requires=[
        "cfg_load>=0.3.1",
        "click>=6.7",
        "pandas>=0.20.3",
        "Pillow>=4.2.1",
        "PyPDF2>=1.26.0",
        "PyYAML>=3.12",
    ],
)
