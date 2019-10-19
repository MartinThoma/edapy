# Third party
import pkg_resources

# First party
import edapy.pdf


def test_make_path_absolute():
    path = "examples/book.pdf"  # always use slash
    filepath = pkg_resources.resource_filename("edapy", path)
    edapy.pdf.get_pdf_info(filepath)
