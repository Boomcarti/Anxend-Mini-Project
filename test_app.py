# tests/test_app.py
import pytest
from flask import template_rendered
from contextlib import contextmanager

from app import app 

# Setup a context manager to capture templates rendered.
@contextmanager
def captured_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))
    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)

@pytest.fixture
def client():
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,  # Disabled thrCSRF tokens m for testing purposes.
    })

    with app.test_client() as client:
        yield client

def test_index_page(client):
    """Test that the index page shows correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Add School" in response.data

def test_form_submission(client):
    """Test submitting the school form."""
    with captured_templates(app) as templates:
        response = client.post('/', data={
            'name': 'Test School',
            'address': '123 Test Lane',
            'town': 'Testville'
        }, follow_redirects=True)
        
        assert response.status_code == 200

        
        # Check if the correct template was used and if the form data is in the context.
        assert len(templates) > 0
        template, context = templates[0]
        assert 'schools' in context 
