import pytest
from flask.testing import FlaskClient
from DIYML import app

@pytest.fixture
def client():
    return app.test_client()

def test_train_put(client: FlaskClient, mocker):
    mocker.patch('Training.setUpFileSystem', return_value="/fake/file/returnlocation.txt")
    mocker.patch('Training.trainModel', return_value={})
    mocker.patch('Training.cleanupFileSystem', return_value={})
    # Happy Path
    resp = client.put('/train', json={'api_token': 'token', 'project_name': 'name', 'train_split':'0.8', "epochs":"12"})

    assert resp.status_code == 200
    assert resp.json.get('RequestResult')

    # Sad Path
    resp = client.put('/train', json={'username': 'username'})
    assert resp.status_code == 400
