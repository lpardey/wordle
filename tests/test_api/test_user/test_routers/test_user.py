# Dependencies
import pytest
from httpx import AsyncClient
from tortoise.transactions import in_transaction

# From apps
from api.v1.user.models import User


@pytest.mark.skip("Work in progress")
async def test_get_user(test_client: AsyncClient) -> None:
    # Create a user for testing
    user_data = {"username": "testuser", "password": "testpassword"}
    response = await test_client.post("/account/create", json=user_data)
    assert response.status_code == 201

    # Log in to get the token
    login_data = {"username": user_data["username"], "password": user_data["password"]}
    response = await test_client.post("/account/login", data=login_data)
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Make a request to the /me endpoint with the obtained token
    response = await test_client.get("/account/me", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    user_response = response.json()
    assert "user_id" in user_response
    assert user_response["username"] == user_data["username"]


@pytest.mark.skip("Work in progress")
async def test_get_user_inactive_user(test_client: AsyncClient) -> None:
    # Create an inactive user for testing
    user_data = {"username": "inactiveuser", "password": "testpassword", "disabled": True}
    response = await test_client.post("/account/create", json=user_data)
    assert response.status_code == 201

    # Log in to get the token
    login_data = {"username": user_data["username"], "password": user_data["password"]}
    response = await test_client.post("/account/login", data=login_data)
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Make a request to the /me endpoint with the obtained token
    response = await test_client.get("/account/me", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 400
    assert "Inactive user" in response.json()["detail"]


@pytest.mark.skip("Work in progress")
async def test_create_user(test_client: AsyncClient) -> None:
    test_data = {"username": "testuser", "password": "testpassword"}

    response = await test_client.post("/account/create", json=test_data)

    assert response.status_code == 201
    assert "user_id" in response.json()
    assert response.json()["username"] == test_data["username"]

    # Check if the user is created in the database
    async with in_transaction():
        user = await User.get(username=test_data["username"])
        assert user is not None
        assert user.username == test_data["username"]
