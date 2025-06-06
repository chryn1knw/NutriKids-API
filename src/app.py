import os, joblib
import tensorflow as tf
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify
from food_recommendation_model import FoodRecommendationModel
from datetime import datetime
from flask_swagger_ui import get_swaggerui_blueprint
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
API_KEY = os.getenv("API_KEY")

SWAGGER_URL = '/docs'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Nutrition API",
    }
)

app.register_blueprint(swaggerui_blueprint)

# Load classification model and preprocessor
classification_model = tf.keras.models.load_model('./artifacts/models/classification_model.h5')
scaler = joblib.load('./artifacts/preprocessors/scaler.pkl')
label_encoder = joblib.load('./artifacts/preprocessors/label_encoder.pkl')

# Load recommendation model and preprocessor
recommendation_model = tf.keras.models.load_model(
    './artifacts/models/recommendation_model.h5', custom_objects={'FoodRecommendationModel': FoodRecommendationModel}
)
child_preprocessor = joblib.load('./artifacts/preprocessors/child_preprocessor.pkl')
food_preprocessor = joblib.load('./artifacts/preprocessors/food_preprocessor.pkl')

# Load food data for recommendation
food_data = pd.read_csv('./artifacts/data/food_data.csv')

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0',
    }), 200

@app.route('/process', methods=['POST'])
def process_data():
    if not verify_api_key(request):
        return jsonify({'error': 'Unauthorized. Invalid or missing API Key.'}), 401

    try:
        data = request.get_json(force=True)

        required_fields = ['age', 'height', 'weight', 'gender', 'food_preferences', 'health_conditions']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f"Field '{field}' is required."}), 400

        valid_health_conditions = ['Sehat', 'Anemia', 'Hypertension', 'Diabetes', 'Obesity']
        health_conditions = data['health_conditions']
        if health_conditions not in valid_health_conditions:
            return jsonify({'error': 'Invalid health condition'}), 400

        age = data['age']
        height_cm = data['height']
        weight_kg = data['weight']
        gender = data['gender']
        food_preferences = data['food_preferences']
        health_conditions = data['health_conditions']

        if not (65 < height_cm < 300 and 6 < weight_kg < 200 and 0 < age < 19):
            return jsonify({'error': 'Input values for height, weight, or age are out of valid range.'}), 400
        
        bmi = round(calculate_bmi(height_cm, weight_kg), 2)
        body_fat_percentage = round(estimate_body_fat_percentage(gender, bmi, age), 2)
        bmr = round(calculate_bmr(weight_kg, height_cm, age, gender), 2)
        calories = round(calculate_bmr(weight_kg, height_cm, age, gender), 2)
        
        classification_data = np.array([[bmi, body_fat_percentage, age, gender]])
        classification_data_scaled = scaler.transform(classification_data)
        
        prediction = classification_model.predict(classification_data_scaled)
        predicted_class = np.argmax(prediction, axis=1)
        nutrition_status = label_encoder.inverse_transform(predicted_class)[0]

        child_data = pd.DataFrame([{
            'age': age,
            'height': height_cm,
            'weight': weight_kg,
            'BMI': bmi,
            'Body_Fat_Percentage': body_fat_percentage,
            'BMR': bmr,
            'Calories': calories,
            'Nutrition_Status': nutrition_status,
            'Food Preferences': food_preferences,
            'Health Conditions': health_conditions
        }])
        
        child_input = child_preprocessor.transform(child_data)
        food_input = food_preprocessor.transform(food_data)

        similarities = recommendation_model([child_input, food_input]).numpy()
        top_k = 5
        top_food_indices = np.argsort(similarities[0])[-top_k:][::-1]
        recommended_foods = food_data.iloc[top_food_indices]

        preferred_foods = recommended_foods[
            recommended_foods['label'].isin(food_preferences.split(','))
        ]

        final_recommendations = preferred_foods if not preferred_foods.empty else recommended_foods

        return jsonify({
            'Status Gizi': nutrition_status,
            'Index Masa Tubuh': bmi,
            'Persentase Lemak Tubuh': body_fat_percentage,
            'Tingkat Metabolisme Basal': bmr,
            'Makanan yang direkomendasikan': final_recommendations.to_dict(orient='records')
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def verify_api_key(request):
    key_from_header = request.headers.get("x-api-key")
    if key_from_header != API_KEY:
        return False
    return True

def calculate_bmi(height_cm, weight_kg):
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return bmi

def estimate_body_fat_percentage(gender, bmi, age):
    if gender == 1:
        body_fat_percentage = 1.20 * bmi + 0.23 * age - 16.2
    else:
        body_fat_percentage = 1.20 * bmi + 0.23 * age - 5.4
    return body_fat_percentage

def calculate_bmr(weight, height, age, gender):
    if gender == 1:
        return 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:  # Female
        return 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)