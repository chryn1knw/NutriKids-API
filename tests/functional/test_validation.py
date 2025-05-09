import pytest
import requests
from tests.conftest import BASE_URL, API_KEY
from tests.test_helpers import validate_error_response


@pytest.mark.parametrize("invalid_payload,description", [
    ({"age": 10, "height": 130, "weight": 35, "gender": 3}, "invalid gender value"),
    ({"age": "ten", "height": 130, "weight": 35, "gender": 1}, "invalid age type"),
    ({"age": 10, "height": "tall", "weight": 35, "gender": 1}, "invalid height type")
])
def test_invalid_input_types(invalid_payload, description):
    headers = {
        "x-api-key": API_KEY
    }
    response = requests.post(f"{BASE_URL}/process", headers=headers, json=invalid_payload)
    assert response.status_code == 400
    validate_error_response(response)

def test_missing_fields(invalid_payloads):
    headers = {
        "x-api-key": API_KEY
    }
    for payload, description in invalid_payloads:
        response = requests.post(f"{BASE_URL}/process", headers=headers, json=payload)
        assert response.status_code == 400
        validate_error_response(response)

def test_invalid_health_condition(valid_payload):
    headers = {
        "x-api-key": API_KEY
    }
    payload = valid_payload.copy()
    payload['health_conditions'] = "UnknownCondition"
    response = requests.post(f"{BASE_URL}/process", headers=headers, json=payload)
    assert response.status_code == 400
    validate_error_response(response)
