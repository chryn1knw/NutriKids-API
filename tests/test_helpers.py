def validate_response_structure(response):
    """Validate the structure of successful API responses"""
    data = response.json()
    required_fields = {
        'Status Gizi': str,
        'Index Masa Tubuh': (int, float),
        'Persentase Lemak Tubuh': (int, float),
        'Tingkat Metabolisme Basal': (int, float),
        'Makanan yang direkomendasikan': list
    }

    for field, field_type in required_fields.items():
        assert field in data
        assert isinstance(data[field], field_type)

def validate_error_response(response, expected_field=None):
    """Validate error response structure"""
    assert response.status_code >= 400
    data = response.json()
    assert 'error' in data
    if expected_field:
        assert expected_field.lower() in data['error'].lower()