import pytest
from flask.testing import FlaskClient
from DIYML import app

@pytest.fixture
def client():
    return app.test_client()

def test_analyze_model_post(client: FlaskClient):
    # Happy Path
    resp = client.post('/analyze_model', json={'api_token': 'token', 'project_name': 'name'})

    assert resp.status_code == 200
    assert resp.json.get('AnalyzeModelResults')
    assert resp.json.get('project_name')

    # Sad Path
    resp = client.post('/analyze_model', json={'username': 'username'})
    assert resp.status_code == 400
