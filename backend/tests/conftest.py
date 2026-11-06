import os
import pytest
from evidencetwin_backend import create_app

@pytest.fixture(autouse=True)
def isolate_environment(monkeypatch):
    for key in list(os.environ):
        if key.startswith("EVIDENCETWIN_"):
            monkeypatch.delenv(key)
    # Existing structural tests intentionally exercise the retained contract-only mode.
    monkeypatch.setenv("EVIDENCETWIN_RUNTIME", "0")

@pytest.fixture
def app():
    return create_app({"TESTING": True})

@pytest.fixture
def client(app):
    return app.test_client()
