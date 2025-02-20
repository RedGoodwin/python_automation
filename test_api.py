import requests
import pytest
from constants import (
    EMPTY_PAYLOAD,
    USER_ENDPOINT, 
    USER_1_PAYLOAD,
    USER_2_PAYLOAD,
    UPDATE_USER_1_PAYLOAD,
    UPDATE_USER_2_PAYLOAD
)

@pytest.mark.parametrize("user_id", [1, 2, 3])
def test_get_user(user_id):
    response = requests.get(f"{USER_ENDPOINT}/{user_id}")
    assert response.status_code == 200
    assert "data" in response.json()
    assert response.json()["data"]["id"]

@pytest.mark.parametrize("payload", [USER_1_PAYLOAD, USER_2_PAYLOAD])
def test_create_user(payload):
    response = requests.post(f"{USER_ENDPOINT}", json=payload)
    assert response.status_code == 201
    assert "name" in response.json()
    assert response.json()["name"] == payload["name"]
    assert "job" in response.json()
    assert response.json()["job"] == payload["job"]

@pytest.mark.parametrize("payload, updated_payload", [
    (USER_1_PAYLOAD, UPDATE_USER_1_PAYLOAD),
    (USER_2_PAYLOAD, UPDATE_USER_2_PAYLOAD)
])
def test_update_user(payload, updated_payload):
    response = requests.post(f"{USER_ENDPOINT}", json=payload)
    response.raise_for_status()
    
    user_data = response.json()
    user_id = user_data["id"]
    assert user_id is not None, f"User ID is missing in the response: {user_data}"

    updated_response = requests.put(f"{USER_ENDPOINT}/{user_id}", json=updated_payload)
    assert updated_response.status_code == 200
    assert updated_response.json()["name"] == updated_payload["name"], "Name is not updated"
    assert updated_response.json()["job"] == updated_payload["job"], "Job is not updated"
    

def test_delete_user():
    response = requests.post(f"{USER_ENDPOINT}", json=USER_1_PAYLOAD)
    response.raise_for_status()

    user_data = response.json()
    user_id = user_data["id"]
    assert user_id is not None, f"User ID is missing in the response: {user_data}"

    delete_response = requests.delete(f"{USER_ENDPOINT}/{user_id}")
    assert delete_response.status_code == 204

    deleted_response = requests.get(f"{USER_ENDPOINT}/{user_id}")
    assert deleted_response.status_code == 404

def test_get_non_existing_user():
    response = requests.get(f"{USER_ENDPOINT}/fake_123")
    assert response.status_code == 404, f"Expected 404 status code for non-existing user, but got {response.status_code}"


def create_user_with_empty_data():
    response = requests.post(f"{USER_ENDPOINT}", json=EMPTY_PAYLOAD)
    assert response.status_code == 400, f"expected status code 400 for empty user, but got {response.status_code}"
    error_response = response.json()
    assert "error" in error_response, "Expected 'error' key in the response"
    assert error_response["error"] == "Missing name or job", f"Expected specific error message, but got: {error_response['error']}"



