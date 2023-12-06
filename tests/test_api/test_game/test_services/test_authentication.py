# Standard Library
from datetime import datetime, timedelta
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
    fixed_date = datetime(2023, 12, 1)
    expire = expires_delta if expires_delta else timedelta(minutes=basic_app_settings.ACCESS_TOKEN_LIFETIME)
    with patch("api.v1.game.services.authentication.datetime") as mock_datetime:
        mock_datetime.now.return_value = fixed_date

        encoded_token = create_access_token(test_data, expires_delta)
        test_data.update({"exp": mock_datetime.now() + expire})

        assert encoded_token == mock_encode.return_value
        mock_encode.assert_called_once_with(
            test_data,
            basic_app_settings.SECRET_KEY,
            basic_app_settings.TOKEN_ALGORITHM,
        )
        mock_datetime.now.assert_called_with()


async def test_get_current_user():
    ...


@patch("api.v1.game.services.authentication.get_current_user")
async def test_get_current_active_user(mock_get_current_user: AsyncMock):
    test_user = User()  # By default disabled attribute is False
    mock_get_current_user.return_value = test_user

    result = await get_current_active_user(test_user)

    assert result == test_user
    # mock_get_current_user.assert_called_once_with(test_user)


@patch("api.v1.game.services.authentication.get_current_user")
async def test_get_current_active_user_inactive_user(mock_get_current_user: AsyncMock):
    test_user = User(disabled=True)
    mock_get_current_user.return_value = test_user

    with pytest.raises(HTTPException) as exc:
        await get_current_active_user(test_user)

    assert exc.value.detail == "Inactive user"
    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
    # mock_get_current_user.assert_called_once_with(test_user)
