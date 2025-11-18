import os
import sys
import pytest

# Path to project root (parent of Tests/)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add project root to sys.path → lets tests import APIs.Prediction
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

@pytest.fixture
def app():
    #Create and return the Flask test app.
    from APIs.Prediction import create_app
    app = create_app()
    app.config.update({"TESTING": True})
    return app


@pytest.fixture
def client(app):
    #Return test client for the Flask app
    return app.test_client()