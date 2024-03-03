import pytest
from flask.testing import FlaskClient
from app import app

@pytest.fixture
def client():
    return app.test_client()

def test_inference_get(client: FlaskClient):
    # Happy Path
    resp = client.get('/reporting', json={'api_token': 'token', 'project_name': 'name', 'image_data':'data'})

    assert resp.status_code == 200
    assert resp.json.get('ReportResults')
    assert resp.json.get('project_name')

    # Sad Path
    resp = client.get('/reporting', json={'username': 'username'})
    assert resp.status_code == 400
