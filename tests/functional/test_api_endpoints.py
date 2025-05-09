import requests
from tests.conftest import BASE_URL, API_KEY
from tests.test_helpers import validate_response_structure
from datetime import datetime


def test_health_endpoint():
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    response_json = response.json()
    assert response_json.get('status') == 'ok', "Status should be 'ok'"
    timestamp = response_json.get('timestamp')
    assert timestamp is not None, "Timestamp should not be None"
    assert isinstance(timestamp, str), "Timestamp should be a string"

    try:
        datetime.fromisoformat(timestamp)
    except ValueError:
        assert False, f"Timestamp '{timestamp}' is not in valid ISO format"

    assert response_json.get('version') == '1.0.0', "Version should be '1.0.0'"

def test_process_endpoint(valid_payload):
    headers = {
        "x-api-key": API_KEY
    }

    response = requests.post(f"{BASE_URL}/process", headers=headers, json=valid_payload)
    assert response.status_code == 200
    validate_response_structure(response)

    data = response.json()
    assert 10 <= data['Index Masa Tubuh'] <= 30
    assert 5 <= data['Persentase Lemak Tubuh'] <= 40

def test_process_with_missing_api_key(valid_payload):
    response = requests.post(f"{BASE_URL}/process", json=valid_payload)
    assert response.status_code == 401
    assert 'Unauthorized' in response.text

def test_process_with_invalid_api_key(valid_payload):
    headers = {
        "x-api-key": "wrong-key"
    }
    response = requests.post(f"{BASE_URL}/process", headers=headers, json=valid_payload)
    assert response.status_code == 401
    assert 'Unauthorized' in response.text