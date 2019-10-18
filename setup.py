#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""edapy: Exploratory data analysis in Python."""

# Core Library
import io
import os

# Third party
from setuptools import find_packages, setup


def read(file_name):
    """Read a text file and return the content as a string."""
    with io.open(
        os.path.join(os.path.dirname(__file__), file_name), encoding="utf-8"
    ) as f:
        return f.read()


requires_tests = [
    "pytest",
    "pytest-cov",
    "pytest-mccabe",
    "pytest-flake8",
    "simplejson",
]
requires_all = requires_tests

config = {
    "name": "edapy",
    "version": "0.2.3",  # keep in sync with edapy/_version.py
    "author": "Martin Thoma",
    "author_email": "info@martin-thoma.de",
    "maintainer": "Martin Thoma",
    "maintainer_email": "info@martin-thoma.de",
    "packages": find_packages(),
    # 'package_data': {'hwrt': ['templates/*', 'misc/*']},
    "extras_require": {"all": requires_all, "tests": requires_tests},
    "entry_points": {"console_scripts": ["edapy=edapy.cli:entry_point"]},
    "platforms": ["Linux"],
    "url": "https://github.com/MartinThoma/edapy",
    "license": "MIT",
    "description": "A tookit for exploratoriy data analysis.",
    "long_description": read("README.md"),
    "long_description_content_type": "text/markdown",
    # If you adjust any of the following, run `pip-compile` to update the
    # requirements.txt
    # You can find `pip-compile` in https://github.com/jazzband/pip-tools
    "install_requires": [
        "cfg_load>=0.3.1",
        "click>=6.7",
        "pandas>=0.20.3",
        "Pillow>=4.2.1",
        "PyPDF2>=1.26.0",
        "PyYAML>=3.12",
    ],
    "keywords": ["EDA", "Data Science"],
    "download_url": "https://github.com/MartinThoma/edapy",
    "classifiers": [
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development",
        "Topic :: Utilities",
    ],
    "zip_safe": False,
}

setup(**config)
