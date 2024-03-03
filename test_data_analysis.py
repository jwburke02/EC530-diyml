import pytest
from flask.testing import FlaskClient
from app import app

@pytest.fixture
def client():
    return app.test_client()

def test_data_analysis_get(client: FlaskClient):
    # Happy Path
    resp = client.get('/data_analysis', json={'api_token': 'token', 'project_name': 'name'})

    assert resp.status_code == 200
    assert resp.json.get('DataAnalysisResults')
    assert resp.json.get('project_name')

    # Sad Path
    resp = client.get('/data_analysis', json={'username': 'username'})
    assert resp.status_code == 400
