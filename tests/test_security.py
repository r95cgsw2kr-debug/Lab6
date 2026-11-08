import requests

BASE_URL = "http://127.0.0.1:8000"

USER_A = {"Authorization": "Bearer token_user_a"}
USER_B = {"Authorization": "Bearer token_user_b"}
ADMIN = {"Authorization": "Bearer token_admin"}


def test_profile_without_token_returns_401():
    response = requests.get(f"{BASE_URL}/api/profile")
    assert response.status_code == 401


def test_profile_with_invalid_token_returns_401():
    headers = {"Authorization": "Bearer wrong_token"}
    response = requests.get(f"{BASE_URL}/api/profile", headers=headers)
    assert response.status_code == 401


def test_valid_user_can_access_profile():
    response = requests.get(f"{BASE_URL}/api/profile", headers=USER_A)
    assert response.status_code == 200
    assert response.json()["name"] == "User A"


def test_regular_user_cannot_access_admin():
    response = requests.get(f"{BASE_URL}/api/admin", headers=USER_A)
    assert response.status_code == 403


def test_admin_can_access_admin():
    response = requests.get(f"{BASE_URL}/api/admin", headers=ADMIN)
    assert response.status_code == 200


def test_user_can_access_own_order():
    response = requests.get(f"{BASE_URL}/api/orders/1001", headers=USER_A)
    assert response.status_code == 200


def test_user_cannot_access_another_users_order():
    response = requests.get(f"{BASE_URL}/api/orders/1002", headers=USER_A)
    assert response.status_code == 403


def test_admin_can_access_another_users_order():
    response = requests.get(f"{BASE_URL}/api/orders/1002", headers=ADMIN)
    assert response.status_code == 200


def test_unknown_order_returns_404():
    response = requests.get(f"{BASE_URL}/api/orders/9999", headers=USER_A)
    assert response.status_code == 404