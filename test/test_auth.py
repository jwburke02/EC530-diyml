import pytest
from flask.testing import FlaskClient
from DIYML import app

@pytest.fixture
def client():
    return app.test_client()

def test_auth_post(client: FlaskClient, mocker):
    mocker.patch('config.atlas_uri', 'example_url_atlas')
    mocker.patch('DatabaseAccess.loginUser', return_value="api_token")
    # Happy Path
    resp = client.post('/auth', json={'username': 'username', 'password': 'password'})

    assert resp.status_code == 200
    assert resp.json.get('username')
    assert resp.json.get('api_token')

    # Sad Path
    resp = client.post('/auth', json={'username': 'username'})
    assert resp.status_code == 400

def test_auth_put(client: FlaskClient, mocker):
    mocker.patch('DatabaseAccess.createUser', return_value="api_token")
    # Happy Path
    resp = client.put('/auth', json={'username': 'username', 'password': 'password'})

    assert resp.status_code == 200
    assert resp.json.get('username')
    assert resp.json.get('api_token')

    # Sad Path
    resp = client.put('/auth', json={'username': 'username'})
    assert resp.status_code == 400

def test_auth_patch(client: FlaskClient, mocker):
    mocker.patch('DatabaseAccess.deleteUser', return_value="api_token")
    # Happy Path
    resp = client.patch('/auth', json={'username': 'username', 'password': 'password', 'api_token': 'somehting'})

    assert resp.status_code == 200
    assert resp.json.get("Status")

    # Sad Path
    resp = client.patch('/auth', json={'username': 'username'})
    assert resp.status_code == 400