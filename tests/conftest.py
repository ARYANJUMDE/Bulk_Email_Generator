"""
Pytest configuration and fixtures.
Isolates test-generated certificate files into a temporary directory so the
production generated_certificates folder is not polluted by test runs.
"""

import pytest
from pathlib import Path
import app.models
import app.routes
import app.utils


@pytest.fixture(autouse=True)
def isolate_test_certificates_dir(tmp_path, monkeypatch):
    """Isolate certificate generation to a temporary directory for all tests."""
    temp_dir = tmp_path / "generated_certificates"
    temp_dir.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(app.utils, "CERTS_DIR", temp_dir)
    monkeypatch.setattr(app.models, "CERTS_DIR", temp_dir)
    monkeypatch.setattr(app.routes, "CERTS_DIR", temp_dir)
    yield temp_dir
