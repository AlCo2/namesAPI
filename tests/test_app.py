from ..main import create_app
import pytest

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()
    yield client


def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200

def test_getOneName(client):
    response = client.get('/api/randomname')
    assert response.status_code == 200

def test_getMultipleName(client):
    response = client.get('/api/randomname/5')
    assert response.status_code == 200

def test_getAllNames(client):
    response = client.get('/api/names')
    assert response.status_code == 200

def test_getARandomName(client):
    response = client.get('/api/names/1')
    assert response.status_code == 200

