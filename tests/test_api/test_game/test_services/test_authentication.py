# Standard Library
from datetime import timedelta
from unittest.mock import AsyncMock, Mock, patch

# Dependencies
import pytest
from fastapi import HTTPException, status
from jose import jwt

# From apps
from api.v1.game.services.authentication import create_access_token, get_current_active_user
from api.v1.settings import Settings
from api.v1.user.models.user import User


@pytest.mark.parametrize(
    "expires_delta",
    [
        pytest.param(None, id="Default expire delta"),
        pytest.param(timedelta(minutes=10), id="Custom expire delta"),
    ],
)
@patch.object(jwt, "encode")
def test_create_access_token(mock_encode: Mock, expires_delta: timedelta | None, basic_app_settings: Settings):
    mock_encode.return_value = "test_encoded_token"
    test_data = {"sub": "test_username"}

    encoded_token = create_access_token(test_data, expires_delta)

    assert encoded_token == mock_encode.return_value
    mock_encode.assert_called_once()


@patch("api.v1.game.services.authentication.get_current_user")
async def test_get_current_active_user(mock_get_current_user: AsyncMock):
    test_user = User()  # By default disabled attribute is False
    mock_get_current_user.return_value = test_user

    result = await get_current_active_user(test_user)

    assert result == test_user
    # await mock_get_current_user.assert_called_once_with(test_user)


@patch("api.v1.game.services.authentication.get_current_user")
async def test_get_current_active_user_inactive_user(mock_get_current_user: AsyncMock):
    test_user = User(disabled=True)
    mock_get_current_user.return_value = test_user

    with pytest.raises(HTTPException) as exc:
        await get_current_active_user(test_user)

    assert exc.value.detail == "Inactive user"
    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
    # mock_get_current_user.assert_awaited_once_with(test_user)
