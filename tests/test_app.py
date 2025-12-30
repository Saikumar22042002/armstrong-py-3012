import pytest
from app import app

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test the /health endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {"status": "healthy"}

def test_root_endpoint(client):
    """Test the root endpoint."""
    response = client.get('/')
    assert response.status_code == 200
    assert "Welcome" in response.json['message']

@pytest.mark.parametrize("number, expected_result", [
    (153, True),   # Classic Armstrong number
    (370, True),   # 3-digit Armstrong number
    (9, True),     # 1-digit Armstrong number
    (1634, True),  # 4-digit Armstrong number
    (10, False),   # Not an Armstrong number
    (154, False),  # Not an Armstrong number
    (0, True),     # 0 is considered an Armstrong number
])
def test_is_armstrong_endpoint(client, number, expected_result):
    """Test the /is_armstrong/<number> endpoint with various numbers."""
    response = client.get(f'/is_armstrong/{number}')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['number'] == number
    assert json_data['is_armstrong'] == expected_result

def test_is_armstrong_non_integer(client):
    """Test the endpoint with a non-integer, expecting a 404."""
    response = client.get('/is_armstrong/abc')
    assert response.status_code == 404
