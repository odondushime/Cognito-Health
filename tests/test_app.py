import pytest
from app import app
from flask_jwt_extended import create_access_token

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert b'healthy' in response.data

def test_login(client):
    response = client.post('/auth/login', json={
        'username': 'test_user',
        'password': 'test_password'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json
    assert 'refresh_token' in response.json

def test_protected_endpoint(client):
    # Create a test token
    access_token = create_access_token(identity='test_user')
    
    # Test dashboard endpoint
    response = client.get('/dashboard', 
                         headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200

def test_upload_endpoint(client):
    access_token = create_access_token(identity='test_user')
    
    # Test with no file
    response = client.post('/data/upload',
                          headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 400
    
    # Test with invalid file type
    response = client.post('/data/upload',
                          headers={'Authorization': f'Bearer {access_token}'},
                          data={'file': (b'content', 'test.txt')})
    assert response.status_code == 400

def test_anomalies_endpoint(client):
    access_token = create_access_token(identity='test_user')
    
    response = client.get('/analytics/anomalies',
                         headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert 'anomalies' in response.json 