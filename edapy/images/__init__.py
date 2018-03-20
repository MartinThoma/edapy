#!/usr/bin/env python

"""Utility functions for exploratory data analysis of image files."""

# core modules
from collections import OrderedDict
import csv
import logging
import os
import pkg_resources

# 3rd party modules
import click
import cfg_load
import PIL.Image
import PIL.ExifTags

# internal modules
import edapy.images.exif


###############################################################################
# CLI                                                                         #
###############################################################################
@click.group(name='images')
def entry_point():
    """Analyze image files."""


###############################################################################
# CLI                                                                         #
###############################################################################
@entry_point.command(name='find')
@click.option('--path',
              help='Path in which all image files are analyzed',
              required=True,
              type=click.Path(exists=True))
@click.option('--output',
              help='Where to store the result of the analysis',
              required=True,
              type=click.File('w'))
def find(path, output):
    """
    Find all image files in a directory and get metadata of them.

    Parameters
    ----------
    path : str
    output : filepointer
    """
    data = []

    filepath = pkg_resources.resource_filename('edapy', 'config/images.yaml')
    cfg = cfg_load.load(filepath)

    for dirpath, dirnames, filenames in os.walk("."):
        files_in_dir = [f for f in filenames for ext in cfg['file_extensions']
                        if f.lower().endswith('.' + ext)]
        for filename in files_in_dir:
            image_path = os.path.abspath(os.path.join(dirpath, filename))
            data.append(get_image_info(image_path))
    write_csv(data, output)


def get_image_info(image_path):
    """
    Get meta information of a image file.

    Parameters
    ----------
    image_path : str

    Returns
    -------
    info : OrderedDict
    """
    info = OrderedDict()
    info['path'] = image_path

    img = PIL.Image.open(image_path)
    info['width'], info['height'] = img.size
    info['area'] = info['width'] * info['height']
    info['file_extension'] = os.path.splitext(info['path'])[1].lower()

    filepath = pkg_resources.resource_filename('edapy', 'config/images.yaml')
    cfg = cfg_load.load(filepath)
    for key in cfg['keys']:
        info[key] = None

    exif = edapy.images.exif.get_exif_data(img)
    for key in exif:
        if key in cfg['keys']:
            info[key] = exif[key]
        elif key in cfg['ignore_keys']:
            continue
        else:
            logging.debug('Key \'{}\' is unknown.'.format(key))

    return info


def write_csv(data, output_filepointer, delimiter=';'):
    """
    Write data to a CSV file.

    Parameters
    ----------
    data : list of dict
    output_filepointer : filepointer
    delimiter : str, optional (default: ';')
    """
    writer = csv.DictWriter(output_filepointer,
                            fieldnames=data[0].keys(),
                            delimiter=delimiter)
    writer.writeheader()
    writer.writerows(data)
