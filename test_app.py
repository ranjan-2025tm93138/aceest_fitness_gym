import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'online'

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'healthy'

def test_get_programs(client):
    response = client.get('/api/programs')
    assert response.status_code == 200
    data = response.get_json()
    assert "Fat Loss (FL)" in data['programs']

def test_calculate_calories_success(client):
    payload = {
        "program": "Fat Loss (FL)",
        "weight": 70
    }
    response = client.post('/api/calculate-calories', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data['estimated_calories'] == 1540  # 70 * 22

def test_calculate_calories_missing_data(client):
    payload = {"program": "Fat Loss (FL)"}
    response = client.post('/api/calculate-calories', json=payload)
    assert response.status_code == 400