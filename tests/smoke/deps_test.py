import importlib
import pytest

REQUIRED = ["weasyprint", "fitz", "matplotlib", "fontTools"]


@pytest.mark.parametrize("name", REQUIRED)
def test_import_duoc(name):
    mod = importlib.import_module(name)
    assert mod is not None, f"{name} import ve None"


def test_pymupdf_dem_duoc_xref():
    import fitz

    doc = fitz.open()
    doc.new_page()
    assert doc.xref_length() >= 1
    doc.close()


def test_matplotlib_backend_svg():
    import matplotlib

    matplotlib.use("svg")
    assert matplotlib.get_backend().lower() == "svg"
