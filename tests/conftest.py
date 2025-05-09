import os
import pytest
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

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
        ({"age": 10, "height": 130, "gender": 1}, "missing weight")
    ]

BASE_URL = "http://localhost:5000"