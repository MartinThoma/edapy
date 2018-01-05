#!/usr/bin/env python

"""Utility functions for exploratory data analysis of PDF files."""

# core modules
from collections import OrderedDict
import csv
import logging
import os
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
    keys = ['/doi', '/Title', '/Subject', '/Keywords', '/AAPL:Keywords',
            '/Language', '/Description',
            '/Creator', '/Producer', '/Application',
            '/Author', '/Authors', '/Editors', '/Publisher', '/Company',
            '/AuthoritativeDomain#5B1#5D',
            '/CrossMarkDomains#5B1#5D', '/CrossMarkDomains#5B2#5D',
            '/Published', '/Date', '/CreationDate', '/Created', '/ModDate',
            '/LastSaved', '/CrossmarkMajorVersionDate',
            '/Trapped', '/PTEX.Fullbanner', '/SourceModified',
            '/GTS_PDFXVersion', '/Type', '/Book', '/Style', '/firstpage',
            '/lastpage', '/robots']

    ignore_keys = ['/CrossmarkDomainExclusive',
                   '/Description-Abstract',
                   '/Appligent',
                   '/AuthoritativeDomain#5B2#5D']

    for key in keys:
        info[key] = None
    info['is_errornous'] = False
    info['is_encrypted'] = False

    with open(pdf_path, 'rb') as fp:
        try:
            pdf_toread = PdfFileReader(fp)
        except PyPDF2.utils.PdfReadError:
            info['is_errornous'] = True
            return info
        try:
            pdf_info = pdf_toread.getDocumentInfo()
            if pdf_info is not None:
                for key in pdf_info:
                    if key not in keys and key not in ignore_keys:
                        logging.info('PDF \'{pdf}\' has unknown key \'{key}\' '
                                     '(Value: {value})'
                                     .format(pdf=pdf_path,
                                             key=key,
                                             value=pdf_info[key]))
                for key in keys:
                    info[key] = pdf_info.get(key, None)
        except PyPDF2.utils.PdfReadError:
            info['is_encrypted'] = True
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
    boolean_columns = ['is_encrypted', 'is_errornous']
    for i in range(len(data)):
        for col in boolean_columns:
            data[i][col] = int(data[i][col])
    writer = csv.DictWriter(output_filepointer,
                            fieldnames=data[0].keys(),
                            delimiter=delimiter)
    writer.writeheader()
    writer.writerows(data)
