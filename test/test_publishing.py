import pytest
from flask.testing import FlaskClient
from DIYML import app

@pytest.fixture
def client():
    return app.test_client()

def test_publishing_put(client: FlaskClient):
    # Happy Path
    resp = client.put('/publish', json={'api_token': 'token', 'project_name': 'name'})

    assert resp.status_code == 200
    assert resp.json.get('Status')

    # Sad Path
    resp = client.put('/publish', json={'username': 'username'})
    assert resp.status_code == 400
