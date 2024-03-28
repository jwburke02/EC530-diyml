import pytest
from flask.testing import FlaskClient
from DIYML import app

@pytest.fixture
def client():
    return app.test_client()

# TESTING PROJECT API (UPLOAD)

def test_upload_project_post(client: FlaskClient, mocker):
    mocker.patch('DatabaseAccess.getProjectInfo', return_value={"_id": "ExampleName","uid": "ExampleName","dids": []})
    # Happy Path
    resp = client.post('/upload/project', json={'project_name': 'name', 'api_token': 'token'})

    assert resp.status_code == 200
    assert resp.json.get('uid')
    assert resp.json.get('_id')
    assert resp.json.get('dids') == []

    # Sad Path
    resp = client.post('/upload/project', json={'username': 'username'})
    assert resp.status_code == 400

def test_upload_project_put(client: FlaskClient, mocker):
    mocker.patch('DatabaseAccess.createProject', return_value={})
    # Happy Path
    resp = client.put('/upload/project', json={'project_name': 'name', 'project_type': 'classification', 'api_token': 'token'})

    assert resp.status_code == 200
    assert resp.json.get('project_name')
    assert resp.json.get('project_type')

    # Sad Path
    resp = client.put('/upload/project', json={'username': 'username'})
    assert resp.status_code == 400

'''
def test_upload_project_patch(client: FlaskClient, mocker):
    mocker.patch('DatabaseAccess.deleteProject', return_value={})
    mocker.patch('utils.remove_folder_contents_and_folder', return_value={})
    # Happy Path
    resp = client.patch('/upload/project', json={'project_name': 'name', 'api_token': 'somehting'})

    assert resp.status_code == 200
    assert resp.json.get("Status")

    # Sad Path
    resp = client.patch('/upload/project', json={'username': 'username'})
    assert resp.status_code == 400
'''
# TESTING DATA API (UPLOAD)

def test_upload_data_post(client: FlaskClient, mocker):
    mocker.patch('DatabaseAccess.getDatapoint', return_value={"_id": "ExampleID", "pid": "ExampleProjectId"})
    # Happy Path
    resp = client.post('/upload/data_point', json={'data_point_name': 'name', 'project_name': 'name', 'api_token': 'token'})

    assert resp.status_code == 200
    assert resp.json.get('_id')
    assert resp.json.get('pid')

    # Sad Path
    resp = client.post('/upload/data_point', json={'username': 'username'})
    assert resp.status_code == 400

def test_upload_data_put(client: FlaskClient, mocker):
    mocker.patch('DatabaseAccess.addDatapoint', return_value={})
    # Happy Path
    resp = client.put('/upload/data_point', json={'image_data':'data','label_data':'data','project_name': 'name', 'data_point_name': 'name', 'api_token': 'token'})

    assert resp.status_code == 200
    assert resp.json.get('Status')

    # Sad Path
    resp = client.put('/upload/data_point', json={'username': 'username'})
    assert resp.status_code == 400

def test_upload_data_patch(client: FlaskClient, mocker):
    mocker.patch('DatabaseAccess.deleteDatapoint', return_value={})
    # Happy Path
    resp = client.patch('/upload/data_point', json={'data_point_name':'name', 'project_name': 'name', 'api_token': 'somehting'})

    assert resp.status_code == 200
    assert resp.json.get("Status")

    # Sad Path
    resp = client.patch('/upload/data_point', json={'username': 'username'})
    assert resp.status_code == 400
    
# TESTING CLASS API (UPLOAD)
    
def test_upload_class_post(client: FlaskClient, mocker):
    mocker.patch('DatabaseAccess.getProjectClasses', return_value=["Apple", "Banana", "Orange"])
    # Happy Path
    resp = client.post('/upload/class_info', json={'project_name': 'name', 'api_token': 'token'})

    assert resp.status_code == 200
    assert resp.json.get('class_list') == ["Apple", "Banana", "Orange"]

    # Sad Path
    resp = client.post('/upload/class_info', json={'username': 'username'})
    assert resp.status_code == 400

def test_upload_class_put(client: FlaskClient, mocker):
    mocker.patch('DatabaseAccess.addProjectClasses', return_value={})
    # Happy Path
    resp = client.put('/upload/class_info', json={'project_name': 'name', 'class_info': 'classification', 'api_token': 'token'})

    assert resp.status_code == 200

    # Sad Path
    resp = client.put('/upload/class_info', json={'username': 'username'})
    assert resp.status_code == 400


def test_upload_class_patch(client: FlaskClient, mocker):
    mocker.patch('DatabaseAccess.deleteProjectClasses', return_value={})
    # Happy Path
    resp = client.patch('/upload/class_info', json={'project_name': 'name', 'api_token': 'somehting'})

    assert resp.status_code == 200
    assert resp.json.get("Status")

    # Sad Path
    resp = client.patch('/upload/class_info', json={'username': 'username'})
    assert resp.status_code == 400