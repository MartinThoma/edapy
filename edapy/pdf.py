#!/usr/bin/env python

"""Utility functions for exploratory data analysis of PDF files."""

# core modules
from collections import OrderedDict
import csv
import logging
import os
import pkg_resources
import shutil
import sys

# 3rd party modules
from PyPDF2 import PdfFileReader
import click
import PyPDF2.utils

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)


###############################################################################
# CLI                                                                         #
###############################################################################
@click.group(name='pdf')
def entry_point():
    """Analyse PDF files."""
    pass


###############################################################################
# CLI                                                                         #
###############################################################################
@entry_point.command(name='find')
@click.option('--path',
              help='Path in which all PDF files are analyzed',
              required=True,
              type=click.Path(exists=True))
@click.option('--output',
              help='Path in which all PDF files are analyzed',
              required=True,
              type=click.File('w'))
def find(path, output):
    """
    Find all PDF files in a directory and get metadata of them.

    Parameters
    ----------
    path : str
    output : filepointer
    """
    data = []
    for dirpath, dirnames, filenames in os.walk("."):
        for filename in [f for f in filenames if f.lower().endswith(".pdf")]:
            pdf_path = os.path.abspath(os.path.join(dirpath, filename))
            data.append(get_pdf_info(pdf_path))
    write_csv(data, output)


def get_pdf_info(pdf_path):
    """
    Get meta information of a PDF file.

    Parameters
    ----------
    pdf_path : str

    Returns
    -------
    info : OrderedDict
    """
    info = OrderedDict()
    info['path'] = pdf_path

    keys = get_flat_cfg_file(path='~/.edapy/pdf_keys.csv')
    ignore_keys = get_flat_cfg_file(path='~/.edapy/pdf_ignore_keys.csv')

    for key in keys:
        info[key] = None
    info['is_errornous'] = False
    info['is_encrypted'] = False
    info['pages'] = -1
    info['nb_characters'] = 0

    with open(pdf_path, 'rb') as fp:
        try:
            pdf_toread = PdfFileReader(fp)
        except PyPDF2.utils.PdfReadError:
            info['is_errornous'] = True
            return info
        except KeyError as e:
            logging.warning('https://github.com/mstamy2/PyPDF2/issues/388 for '
                            ' PDF \'{}\': {}'
                            .format(pdf_path, e))
            return info
        except OSError as e:
            logging.warning('OSError for '
                            ' PDF \'{}\': {}'
                            .format(pdf_path, e))
            return info
        except AssertionError as e:
            logging.warning('AssertionError for '
                            ' PDF \'{}\': {}'
                            .format(pdf_path, e))
            return info
        except TypeError as e:
            logging.warning('TypeError for '
                            ' PDF \'{}\': {}'
                            .format(pdf_path, e))
            return info
        try:
            pdf_info = pdf_toread.getDocumentInfo()

            info['pages'] = pdf_toread.getNumPages()
            text_content = get_text_pdftotextbin(pdf_path)
            info['nb_characters'] = len(text_content)

            if pdf_info is not None:
                for key in pdf_info:
                    log = (key not in keys and
                           key not in ignore_keys and
                           not key.startswith('/FL#'))
                    if log:
                        logging.info('Unknown key \'{key}\' '
                                     '(Value: {value}) for PDF \'{pdf}\''
                                     .format(pdf=pdf_path,
                                             key=key,
                                             value=pdf_info[key]))
                for key in keys:
                    info[key] = pdf_info.get(key, None)
        except PyPDF2.utils.PdfReadError:
            info['is_encrypted'] = True
    return info


def get_text_pdftotextbin(pdf_filename):
    """
    Extract text from PDF with pdftotext.

    Parameters
    ----------
    pdf_filename : str

    Returns
    -------
    str
    """
    import codecs
    import subprocess
    tmp_filename = "out_tmp_file_pdf_batch_analyze.txt"
    with codecs.open(os.devnull, 'wb', encoding='utf8') as devnull:
        subprocess.check_call(["pdftotext",
                               "{filename}".format(filename=pdf_filename),
                               tmp_filename],
                              stdout=devnull, stderr=subprocess.STDOUT)
    with codecs.open(tmp_filename, 'r', encoding='utf8') as f:
        contents = f.read()
    return contents


def get_flat_cfg_file(path='~/.edapy/pdf_ignore_keys.csv'):
    """
    Get a list of strings from a config file.

    Create this if it doesn't exist

    Parameters
    ----------
    path : str

    Returns
    -------
    ignore_keys : list of str
    """
    path = os.path.expanduser(path)
    path = os.path.abspath(path)
    directory, filename = os.path.split(path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    if not os.path.isfile(path):
        path_inside = '/'.join(['static', filename])
        src = pkg_resources.resource_filename('edapy', path_inside)
        shutil.copyfile(src, path)
    with open(path) as f:
        ignore_keys = [line.strip() for line in f.readlines()]
    return ignore_keys


def write_csv(data, output_filepointer, delimiter=';'):
    """
    Write data to a CSV file.

    Parameters
    ----------
    data : list of dict
    output_filepointer : filepointer
    delimiter : str, optional (default: ';')
    """
    boolean_columns = ['is_encrypted', 'is_errornous']
    for i in range(len(data)):
        for col in boolean_columns:
            data[i][col] = int(data[i][col])
    writer = csv.DictWriter(output_filepointer,
                            fieldnames=data[0].keys(),
                            delimiter=delimiter)
    writer.writeheader()
    writer.writerows(data)
