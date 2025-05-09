import requests
from tests.conftest import BASE_URL, API_KEY


def test_food_recommendation(valid_payload):
    headers = {
        "x-api-key": API_KEY
    }
    response = requests.post(f"{BASE_URL}/process", headers=headers, json=valid_payload)
    assert response.status_code == 200

    data = response.json()
    recommendations = data['Makanan yang direkomendasikan']
    assert len(recommendations) >= 1
    assert all('label' in food for food in recommendations)


def test_preference_filtering(valid_payload):
    headers = {
        "x-api-key": API_KEY
    }
    payload = valid_payload.copy()
    payload['food_preferences'] = "Vegan"
    response = requests.post(f"{BASE_URL}/process", headers=headers, json=payload)

    data = response.json()
    recommendations = data['Makanan yang direkomendasikan']
    assert all(food['label'] in [ 'Vegan'] for food in recommendations)