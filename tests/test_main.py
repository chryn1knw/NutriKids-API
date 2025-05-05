import pytest
import requests
import time

BASE_URL = "http://localhost:5000"

# Test Data
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


@pytest.fixture
def invalid_payloads():
    return [
        ({"height": 130, "weight": 35, "gender": 1}, "missing age"),
        ({"age": 10, "weight": 35, "gender": 1}, "missing height"),
        ({"age": 10, "height": 130, "gender": 1}, "missing weight"),
        ({"age": 10, "height": 130, "weight": 35}, "missing gender"),
        ({"age": 0, "height": 130, "weight": 35, "gender": 1}, "invalid age (low)"),
        ({"age": 19, "height": 130, "weight": 35, "gender": 1}, "invalid age (high)"),
        ({"age": 10, "height": 64, "weight": 35, "gender": 1}, "invalid height (low)"),
        ({"age": 10, "height": 301, "weight": 35, "gender": 1}, "invalid height (high)"),
        ({"age": 10, "height": 130, "weight": 5, "gender": 1}, "invalid weight (low)"),
        ({"age": 10, "height": 130, "weight": 201, "gender": 1}, "invalid weight (high)")
    ]


# Helper Functions
def validate_response_structure(response):
    """Validate the structure of successful API responses"""
    data = response.json()
    assert 'Status Gizi' in data
    assert 'Index Masa Tubuh' in data
    assert 'Persentase Lemak Tubuh' in data
    assert 'Tingkat Metabolisme Basal' in data
    assert 'Makanan yang direkomendasikan' in data
    assert isinstance(data['Makanan yang direkomendasikan'], list)


def validate_error_response(response, expected_field=None):
    """Validate error response structure"""
    assert response.status_code >= 400
    data = response.json()
    assert 'error' in data
    if expected_field:
        assert expected_field.lower() in data['error'].lower()


# Test Cases

def test_api_health_check():
    """Basic health check endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    if response.status_code != 404:  # Only test if endpoint exists
        assert response.status_code == 200
        assert response.json().get('status') == 'ok'


def test_process_endpoint_exists(valid_payload):
    """Smoke test: /process endpoint works and returns 200"""
    response = requests.post(f"{BASE_URL}/process", json=valid_payload)
    assert response.status_code == 200
    validate_response_structure(response)


def test_process_missing_field(valid_payload):
    """Test missing required fields"""
    required_fields = ['age', 'height', 'weight', 'gender']
    for field in required_fields:
        invalid_payload = valid_payload.copy()
        invalid_payload.pop(field)
        response = requests.post(f"{BASE_URL}/process", json=invalid_payload)
        assert response.status_code == 400
        validate_error_response(response, field)


@pytest.mark.parametrize("invalid_payload,description", [
    ({"age": 10, "height": 130, "weight": 35, "gender": 3}, "invalid gender value"),
    ({"age": 10, "height": 130, "weight": 35, "gender": "male"}, "invalid gender type"),
    ({"age": "ten", "height": 130, "weight": 35, "gender": 1}, "invalid age type"),
    ({"age": 10, "height": "tall", "weight": 35, "gender": 1}, "invalid height type"),
    ({"age": 10, "height": 130, "weight": "heavy", "gender": 1}, "invalid weight type")
])
def test_invalid_input_types(invalid_payload, description):
    """Test various invalid input types"""
    response = requests.post(f"{BASE_URL}/process", json=invalid_payload)
    assert response.status_code == 400
    validate_error_response(response)


def test_invalid_ranges(valid_payload):
    """Test input value boundaries"""
    # Test age boundaries
    for age in [0, 19]:
        payload = valid_payload.copy()
        payload['age'] = age
        response = requests.post(f"{BASE_URL}/process", json=payload)
        assert response.status_code == 400
        validate_error_response(response, 'age')

    # Test height boundaries
    for height in [64, 301]:
        payload = valid_payload.copy()
        payload['height'] = height
        response = requests.post(f"{BASE_URL}/process", json=payload)
        assert response.status_code == 400
        validate_error_response(response, 'height')

    # Test weight boundaries
    for weight in [5, 201]:
        payload = valid_payload.copy()
        payload['weight'] = weight
        response = requests.post(f"{BASE_URL}/process", json=payload)
        assert response.status_code == 400
        validate_error_response(response, 'weight')

def test_successful_recommendation(valid_payload):
    """Test successful food recommendation"""
    response = requests.post(f"{BASE_URL}/process", json=valid_payload)
    assert response.status_code == 200
    data = response.json()

    # Validate numeric outputs
    assert 10 <= data['Index Masa Tubuh'] <= 30  # Reasonable BMI range for test
    assert 5 <= data['Persentase Lemak Tubuh'] <= 40  # Reasonable body fat %
    assert data['Tingkat Metabolisme Basal'] > 0

    # Validate recommendations
    recommendations = data['Makanan yang direkomendasikan']
    assert len(recommendations) >= 1  # At least one recommendation
    assert all('label' in food for food in recommendations)

def test_food_preferences_filtering(valid_payload):
    """Test that food preferences are respected"""
    payload = valid_payload.copy()
    payload['food_preferences'] = "Vegan,Vegetarian"
    response = requests.post(f"{BASE_URL}/process", json=payload)
    assert response.status_code == 200
    data = response.json()

    recommendations = data['Makanan yang direkomendasikan']
    assert all(food['label'] in ['Vegan', 'Vegetarian'] for food in recommendations)


def test_performance_benchmark(valid_payload):
    """Performance test: response time should be reasonable"""
    start_time = time.time()
    response = requests.post(f"{BASE_URL}/process", json=valid_payload)
    end_time = time.time()

    assert response.status_code == 200
    assert (end_time - start_time) < 3.0  # Response should be under 3 seconds


def test_concurrent_requests(valid_payload):
    """Test handling of concurrent requests"""
    import threading

    results = []
    errors = []

    def make_request():
        try:
            response = requests.post(f"{BASE_URL}/process", json=valid_payload)
            results.append(response.status_code)
        except Exception as e:
            errors.append(str(e))

    threads = [threading.Thread(target=make_request) for _ in range(5)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert not errors, f"Errors occurred during concurrent requests: {errors}"
    assert all(code == 200 for code in results), "Not all requests succeeded"


def test_documentation_exists():
    """Check if API documentation is available"""
    response = requests.get(f"{BASE_URL}/docs")
    if response.status_code != 404:  # Only test if endpoint exists
        assert response.status_code == 200
        assert 'text/html' in response.headers['Content-Type']