import requests

BASE_URL = "http://127.0.0.1:8000"


def test_products_returns_200():
    response = requests.get(f"{BASE_URL}/api/products")
    assert response.status_code == 200


def test_products_returns_correct_data():
    response = requests.get(f"{BASE_URL}/api/products")
    assert response.json() == {
        "products": ["Laptop", "Phone", "Tablet"]
    }


def test_unknown_route_returns_404():
    response = requests.get(f"{BASE_URL}/api/unknown")
    assert response.status_code == 404

def test_slow_endpoint_timeout():
    import pytest

    with pytest.raises(requests.exceptions.Timeout):
        requests.get(f"{BASE_URL}/api/slow", timeout=1)