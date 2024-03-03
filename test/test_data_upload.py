import pytest
from flask.testing import FlaskClient
from app import app

@pytest.fixture
def client():
    return app.test_client()

# TESTING PROJECT API (UPLOAD)

def test_upload_project_get(client: FlaskClient):
    # Happy Path
    resp = client.get('/upload/project', json={'project_name': 'name', 'api_token': 'token'})

    assert resp.status_code == 200
    assert resp.json.get('project_name')
    assert resp.json.get('project_type')

    # Sad Path
    resp = client.get('/upload/project', json={'username': 'username'})
    assert resp.status_code == 400

def test_upload_project_put(client: FlaskClient):
    # Happy Path
    resp = client.put('/upload/project', json={'project_name': 'name', 'project_type': 'classification', 'api_token': 'token'})

    assert resp.status_code == 200
    assert resp.json.get('project_name')
    assert resp.json.get('project_type')

    # Sad Path
    resp = client.get('/upload/project', json={'username': 'username'})
    assert resp.status_code == 400

def test_upload_project_post(client: FlaskClient):
    # Happy Path
    resp = client.put('/upload/project', json={'project_name': 'name', 'project_type': 'classification', 'api_token': 'token'})

    assert resp.status_code == 200
    assert resp.json.get('project_name')
    assert resp.json.get('project_type')

    # Sad Path
    resp = client.get('/upload/project', json={'username': 'username'})
    assert resp.status_code == 400

def test_upload_project_delete(client: FlaskClient):
    # Happy Path
    resp = client.delete('/upload/project', json={'project_name': 'name', 'api_token': 'somehting'})

    assert resp.status_code == 200
    assert resp.json.get("Status")

    # Sad Path
    resp = client.get('/upload/project', json={'username': 'username'})
    assert resp.status_code == 400

# TESTING DATA API (UPLOAD)

def test_upload_data_get(client: FlaskClient):
    # Happy Path
    resp = client.get('/upload/data_point', json={'data_point_name': 'name', 'project_name': 'name', 'api_token': 'token'})

    assert resp.status_code == 200
    assert resp.json.get('project_name')
    assert resp.json.get('data_point_name')
    assert resp.json.get('image_data')
    assert resp.json.get('label_data')

    # Sad Path
    resp = client.get('/upload/data_point', json={'username': 'username'})
    assert resp.status_code == 400

def test_upload_data_put(client: FlaskClient):
    # Happy Path
    resp = client.put('/upload/data_point', json={'image_data':'data','label_data':'data','project_name': 'name', 'data_point_name': 'name', 'api_token': 'token'})

    assert resp.status_code == 200
    assert resp.json.get('project_name')
    assert resp.json.get('data_point_name')

    # Sad Path
    resp = client.get('/upload/data_point', json={'username': 'username'})
    assert resp.status_code == 400

def test_upload_data_post(client: FlaskClient):
    # Happy Path
    resp = client.put('/upload/data_point', json={'image_data':'data','label_data':'data','project_name': 'name', 'data_point_name': 'name', 'api_token': 'token'})

    assert resp.status_code == 200
    assert resp.json.get('project_name')
    assert resp.json.get('data_point_name')

    # Sad Path
    resp = client.get('/upload/data_point', json={'username': 'username'})
    assert resp.status_code == 400

def test_upload_data_delete(client: FlaskClient):
    # Happy Path
    resp = client.delete('/upload/data_point', json={'data_point_name':'name', 'project_name': 'name', 'api_token': 'somehting'})

    assert resp.status_code == 200
    assert resp.json.get("Status")

    # Sad Path
    resp = client.get('/upload/data_point', json={'username': 'username'})
    assert resp.status_code == 400
    
# TESTING CLASS API (UPLOAD)
    
def test_upload_class_get(client: FlaskClient):
    # Happy Path
    resp = client.get('/upload/class_info', json={'project_name': 'name', 'api_token': 'token'})

    assert resp.status_code == 200
    assert resp.json.get('project_name')
    assert resp.json.get('class_info')

    # Sad Path
    resp = client.get('/upload/class_info', json={'username': 'username'})
    assert resp.status_code == 400

def test_upload_class_put(client: FlaskClient):
    # Happy Path
    resp = client.put('/upload/class_info', json={'project_name': 'name', 'class_info': 'classification', 'api_token': 'token'})

    assert resp.status_code == 200
    assert resp.json.get('project_name')
    assert resp.json.get('class_info')

    # Sad Path
    resp = client.get('/upload/class_info', json={'username': 'username'})
    assert resp.status_code == 400

def test_upload_class_post(client: FlaskClient):
    # Happy Path
    resp = client.put('/upload/class_info', json={'project_name': 'name', 'class_info': 'classification', 'api_token': 'token'})

    assert resp.status_code == 200
    assert resp.json.get('project_name')
    assert resp.json.get('class_info')

    # Sad Path
    resp = client.get('/upload/class_info', json={'username': 'username'})
    assert resp.status_code == 400

def test_upload_class_delete(client: FlaskClient):
    # Happy Path
    resp = client.delete('/upload/class_info', json={'project_name': 'name', 'api_token': 'somehting'})

    assert resp.status_code == 200
    assert resp.json.get("Status")

    # Sad Path
    resp = client.get('/upload/class_info', json={'username': 'username'})
    assert resp.status_code == 400