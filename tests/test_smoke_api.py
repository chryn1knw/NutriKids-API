import pytest
import requests

BASE_URL = "http://localhost:5000"

@pytest.fixture
def valid_payload():
    return {
        "age": 10,
        "height": 130,
        "weight": 35,
        "gender": 1,
        "food_preferences": "Vegan",
        "health_conditions": "Sehat"
    }

def test_process_endpoint_exists(valid_payload):
    """Smoke test: /process endpoint works and returns 200"""
    response = requests.post(f"{BASE_URL}/process", json=valid_payload)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

def test_process_missing_field(valid_payload):
    """Smoke test: /process should return 400 if required field is missing"""
    invalid_payload = valid_payload.copy()
    invalid_payload.pop("age")  # intentionally remove required field
    response = requests.post(f"{BASE_URL}/process", json=invalid_payload)
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    assert "age" in response.text
