#!/usr/bin/env python

"""Utility functions for exploratory data analysis of image files."""

# Core Library
import csv
import logging
import os
from collections import OrderedDict
from typing import Any, Dict, List

# Third party
import cfg_load
import click
import PIL.ExifTags
import PIL.Image
import pkg_resources

# First party
import edapy.images.exif

logger = logging.getLogger(__name__)


@click.group(name="images")
def entry_point() -> None:
    """Analyze image files."""


@entry_point.command(name="find")
@click.option(
    "--path",
    help="Path in which all image files are analyzed",
    required=True,
    type=click.Path(exists=True),
)
@click.option(
    "--output",
    help="Where to store the result of the analysis",
    required=True,
    type=click.File("w"),
)
def find(path: str, output) -> None:
    """
    Find all image files in a directory and get metadata of them.

    Parameters
    ----------
    path : str
    output : filepointer
    """
    data: List[Dict] = []

    filepath = pkg_resources.resource_filename("edapy", "config/images.yaml")
    cfg = cfg_load.load(filepath)

    for dirpath, _dirnames, filenames in os.walk("."):
        files_in_dir = [
            f
            for f in filenames
            for ext in cfg["file_extensions"]
            if f.lower().endswith("." + ext)
        ]
        for filename in files_in_dir:
            image_path = os.path.abspath(os.path.join(dirpath, filename))
            data.append(get_image_info(image_path))
    write_csv(data, output)


def get_image_info(image_path: str) -> Dict:
    """
    Get meta information of a image file.

    Parameters
    ----------
    image_path : str

    Returns
    -------
    info : OrderedDict
    """
    info: Dict[str, Any] = OrderedDict()
    info["path"] = image_path

    img = PIL.Image.open(image_path)
    info["width"], info["height"] = img.size
    info["area"] = info["width"] * info["height"]
    info["file_extension"] = os.path.splitext(info["path"])[1].lower()

    filepath = pkg_resources.resource_filename("edapy", "config/images.yaml")
    cfg = cfg_load.load(filepath)
    for key in cfg["keys"]:
        info[key] = None

    exif = edapy.images.exif.get_exif_data(img)
    for key in exif:
        if key in cfg["keys"]:
            info[key] = exif[key]
        elif key in cfg["ignore_keys"]:
            continue
        else:
            logger.debug(f"Key '{key}' is unknown.")

    return info


def write_csv(data: List[Dict], output_filepointer, delimiter: str = ";") -> None:
    """
    Write data to a CSV file.

    Parameters
    ----------
    data : List[Dict]
    output_filepointer : filepointer
    delimiter : str, optional (default: ';')
    """
    writer = csv.DictWriter(
        output_filepointer, fieldnames=data[0].keys(), delimiter=delimiter
    )
    writer.writeheader()
    writer.writerows(data)
