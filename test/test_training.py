import pytest
from flask.testing import FlaskClient
from DIYML import app

@pytest.fixture
def client():
    return app.test_client()

def test_train_put(client: FlaskClient):
    # Happy Path
    resp = client.put('/train', json={'api_token': 'token', 'project_name': 'name', 'train_split':'splt', "epochs":"12"})

    assert resp.status_code == 200
    assert resp.json.get('TrainResults')
    assert resp.json.get('Status')

    # Sad Path
    resp = client.put('/train', json={'username': 'username'})
    assert resp.status_code == 400
