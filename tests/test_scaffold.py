"""Smoke test del esqueleto del proyecto."""

from sat_xml import __version__


def test_version():
    assert __version__ == "0.1.0"
