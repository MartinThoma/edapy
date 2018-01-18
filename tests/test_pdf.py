# core modules
import pkg_resources
import unittest

# internal modules
import edapy.pdf


class PdfTest(unittest.TestCase):

    def test_make_path_absolute(self):

        path = 'examples/book.pdf'  # always use slash
        filepath = pkg_resources.resource_filename('edapy', path)
        edapy.pdf.get_pdf_info(filepath)
