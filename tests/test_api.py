import pytest
from app.main import app, ITEMS
#Test of new codes
# Test 1: Check correct stock filtering
def test_low_stock(client):
    threshold = 5
    response = client.get(f'/api/items/low-stock?threshold={threshold}')

    expected = [item for item in ITEMS if item['stock'] < threshold]

    assert response.status_code == 200
    assert response.get_json()['items'] == expected


# Test 2: Check minimum threshold
def test_minimum_threshold(client):
    response = client.get('/api/items/low-stock?threshold=0')

    assert response.status_code == 200
    assert response.get_json()['items'] == []


# Test 3: Check maximum threshold
def test_maximum_threshold(client):
    response = client.get('/api/items/low-stock?threshold=100')

    expected = [item for item in ITEMS if item['stock'] < 100]

    assert response.status_code == 200
    assert response.get_json()['items'] == expected


# Test 4: Check invalid threshold
def test_invalid_threshold(client):
    for value in [-1, 101, 'abc']:
        response = client.get(f'/api/items/low-stock?threshold={value}')

        assert response.status_code == 400


# Test 5: Check missing threshold
def test_missing_threshold(client):
    response = client.get('/api/items/low-stock')

    assert response.status_code == 400


from app.main import app

@pytest.fixture
def client():
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client

def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'ok'

def test_items(client):
    response = client.get('/api/items')
    assert response.status_code == 200
    assert len(response.get_json()['items']) == 2

def test_item_not_found(client):
    response = client.get('/api/items/999')
    assert response.status_code == 404
    assert response.get_json()['error'] == 'item not found'

#Test for threshod below
def test_equal_threshold(client):
    for item in ITEMS:
        threshold = item['stock']

        response = client.get(
            f'/api/items/low-stock?threshold={threshold}'
        )

        result = response.get_json()['items']

        assert response.status_code == 200
        assert item not in result
