
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    assert client.get('/api/health').json()['status'] == 'ok'


def test_forecast():
    response = client.post(
        '/api/forecast',
        json={'available_staff': 9, 'hours_per_staff': 8}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data['forecast']) == 7
    assert all(item['required_hours'] >= 0 for item in data['forecast'])
    assert all(
        item['risk'] in ('Low', 'Moderate', 'High')
        for item in data['forecast']
    )
    assert 'synthetic' in data['disclaimer'].lower()


def test_no_staff_is_high_risk():
    result = client.post(
        '/api/forecast',
        json={'available_staff': 0}
    ).json()
    assert all(
        item['risk'] == 'High'
        for item in result['forecast']
    )
    assert all(
        item['utilization_pct'] is None
        for item in result['forecast']
    )


def test_invalid_staff_rejected():
    assert client.post(
        '/api/forecast',
        json={'available_staff': -1}
    ).status_code == 422


def test_cors_allows_frontend():
    response = client.options(
        '/api/forecast',
        headers={
            'Origin': 'http://localhost:5173',
            'Access-Control-Request-Method': 'POST',
        }
    )

    assert response.status_code == 200
    assert (
        response.headers['access-control-allow-origin']
        == 'http://localhost:5173'
    )
    assert 'POST' in response.headers['access-control-allow-methods']






def test_invalid_hours_rejected():
    response = client.post(
        '/api/forecast',
        json={'available_staff': 9, 'hours_per_staff': -1}
    )
    assert response.status_code == 422


def test_staff_boundary_zero():
    response = client.post(
        '/api/forecast',
        json={'available_staff': 0, 'hours_per_staff': 8}
    )
    assert response.status_code == 200
    assert len(response.json()['forecast']) == 7


def test_forecast_response_fields():
    response = client.post(
        '/api/forecast',
        json={'available_staff': 9, 'hours_per_staff': 8}
    )
    assert response.status_code == 200

    data = response.json()
    required_fields = {
        'date',
        'patients',
        'required_hours',
        'capacity_hours',
        'utilization_pct',
        'risk',
    }

    for item in data['forecast']:
        assert required_fields.issubset(item.keys())
