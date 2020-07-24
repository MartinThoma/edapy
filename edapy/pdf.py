#!/usr/bin/env python

"""Utility functions for exploratory data analysis of PDF files."""

# Core Library
import csv
import logging
import os
import shutil
from collections import OrderedDict
from difflib import SequenceMatcher
from tempfile import mkstemp
from typing import Any, Dict, List

# Third party
import click
import pkg_resources
import PyPDF2.utils
from PyPDF2 import PdfFileReader

logger = logging.getLogger(__name__)


###############################################################################
# CLI                                                                         #
###############################################################################
@click.group(name="pdf")
def entry_point():
    """Analyze PDF files."""


###############################################################################
# CLI                                                                         #
###############################################################################
@entry_point.command(name="find")
@click.option(
    "--path",
    help="Path in which all PDF files are analyzed",
    required=True,
    type=click.Path(exists=True),
)
@click.option(
    "--output",
    help="Path in which all PDF files are analyzed",
    required=True,
    type=click.File("w"),
)
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
    info["path"] = pdf_path

    keys = get_flat_cfg_file(path="~/.edapy/pdf_keys.csv")
    ignore_keys = get_flat_cfg_file(path="~/.edapy/pdf_ignore_keys.csv")

    for key in keys:
        info[key] = None
    info["is_errornous"] = False
    info["is_encrypted"] = False
    info["nb_pages"] = -1
    info["nb_toc_top_level"] = -1
    info["nb_characters"] = 0

    with open(pdf_path, "rb") as fp:
        try:
            pdf_toread = PdfFileReader(fp, strict=False)
        except PyPDF2.utils.PdfReadError:
            info["is_errornous"] = True
            return info
        except KeyError as e:
            logger.warning(
                "https://github.com/mstamy2/PyPDF2/issues/388 for "
                f" PDF '{pdf_path}': {e}"
            )
            return info
        except OSError as e:
            logger.warning(f"OSError for PDF '{pdf_path}': {e}")
            return info
        except AssertionError as e:
            logger.warning(f"AssertionError for PDF '{pdf_path}': {e}")
            return info
        except TypeError as e:
            logger.warning(f"TypeError for PDF '{pdf_path}': {e}")
            return info

        try:
            tl_toc = [el for el in pdf_toread.outlines if not isinstance(el, list)]
            info["nb_toc_top_level"] = len(tl_toc)
        except PyPDF2.utils.PdfReadError as e:
            logger.error(f"{pdf_path}: PyPDF2.utils.PdfReadError {e}")
        except ValueError as e:
            logger.error(f"{pdf_path}: ValueError {e}")
        except TypeError as e:
            logger.error(f"{pdf_path}: TypeError {e}")

        info = enhance_pdf_info(info, pdf_toread, pdf_path, keys, ignore_keys)
    return info


def enhance_pdf_info(
    info: Dict[str, Any], pdf_toread, pdf_path: str, keys: List[str], ignore_keys
) -> Dict[str, Any]:
    """
    Add information about a PDF.

    Examples this can add:

        /CreationDate
        /Creator
        /ModDate
        /Producer
        nb_characters
        nb_pages

    Parameters
    ----------
    info : Dict[str, Any]
    pdf_toread:
    pdf_path: str
    keys:
    ignore_keys:

    Returns
    -------
    info : Dict[str, Any]
    """
    try:
        pdf_info = pdf_toread.getDocumentInfo()

        info["nb_pages"] = pdf_toread.getNumPages()
        text_content = get_text_pdftotextbin(pdf_path)
        info["nb_characters"] = len(text_content)

        if pdf_info is not None:
            for key in pdf_info:
                log = (
                    key not in keys
                    and key not in ignore_keys
                    and not key.startswith("/FL#")
                )
                if log:
                    logger.error(
                        "Unknown key '{key}' "
                        "(Value: {value}) for PDF '{pdf}'".format(
                            pdf=pdf_path, key=key, value=pdf_info[key]
                        )
                    )
            for key in keys:
                info[key] = pdf_info.get(key, None)
    except PyPDF2.utils.PdfReadError:
        info["is_encrypted"] = True
    return info


def get_watermark(pdf_filename, nb_pages):
    """
    Find potential watermark.

    Parameters
    ----------
    pdf_filename : str
    nb_pages : int

    Returns
    -------
    watermark : str
    """
    last_watermark = None
    last_text = None
    text = None
    for page in range(nb_pages):
        last_text = text
        text = get_text_pdftotextbin(pdf_filename, page=page)
        if last_text is None:
            continue
        match = SequenceMatcher(None, text, last_text).find_longest_match(
            0, len(text), 0, len(last_text)
        )
        possible_watermark = text[match.a : match.a + match.size]
        if last_watermark is None:
            last_watermark = possible_watermark
        elif possible_watermark in last_watermark:
            last_watermark = possible_watermark
        else:
            last_watermark = ""
    return last_watermark


def get_text_pdftotextbin(pdf_filename: str, page=None):
    """
    Extract text from PDF with pdftotext.

    Parameters
    ----------
    pdf_filename : str

    Returns
    -------
    str
    """
    # Core Library
    import codecs
    import subprocess

    _, tmp_filename = mkstemp(prefix="edapy_file_pdf_batch_analyze_", suffix=".txt")
    with codecs.open(os.devnull, "wb", encoding="utf8") as devnull:
        if page is None:
            subprocess.check_call(
                ["pdftotext", pdf_filename, tmp_filename],
                stdout=devnull,
                stderr=subprocess.STDOUT,
            )
        else:
            subprocess.check_call(
                [
                    "pdftotext",
                    f"{pdf_filename}",
                    "-f",
                    str(page),
                    "-l",
                    str(page),
                    tmp_filename,
                ],
                stdout=devnull,
                stderr=subprocess.STDOUT,
            )
    with codecs.open(tmp_filename, "r", encoding="utf8") as f:
        contents = f.read()
    os.remove(tmp_filename)
    return contents


def get_flat_cfg_file(path="~/.edapy/pdf_ignore_keys.csv"):
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
        path_inside = "/".join(["static", filename])
        src = pkg_resources.resource_filename("edapy", path_inside)
        shutil.copyfile(src, path)
    with open(path) as f:
        ignore_keys = [line.strip() for line in f.readlines()]
    return ignore_keys


def write_csv(data, output_filepointer, delimiter=";"):
    """
    Write data to a CSV file.

    Parameters
    ----------
    data : list of dict
    output_filepointer : filepointer
    delimiter : str, optional (default: ';')
    """
    boolean_columns = ["is_encrypted", "is_errornous"]
    for i in range(len(data)):
        for col in boolean_columns:
            data[i][col] = int(data[i][col])
    writer = csv.DictWriter(
        output_filepointer, fieldnames=data[0].keys(), delimiter=delimiter
    )
    writer.writeheader()
    writer.writerows(data)
