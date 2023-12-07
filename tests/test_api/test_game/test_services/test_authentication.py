# Standard Library
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, Mock, patch

# Dependencies
import pytest
from fastapi import HTTPException, status
from jose import JWTError, jwt

# From apps
from api.v1.game.services.authentication import (
    create_access_token,
    get_current_active_user,
    get_current_user,
    validate_token,
)
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


@patch.object(jwt, "decode")
@patch("api.v1.game.services.authentication.oauth2_scheme")
def test_validate_token(mock_oauth2_scheme: Mock, mock_decode: Mock, basic_app_settings: Settings):
    mock_oauth2_scheme.return_value = "123"
    mock_decode.return_value = {"sub": "test_username"}
    token = mock_oauth2_scheme.return_value
    expected_result = mock_decode.return_value["sub"]
    mock_decode_args = (token, basic_app_settings.SECRET_KEY, [basic_app_settings.TOKEN_ALGORITHM])

    result = validate_token(token)

    assert result == expected_result
    mock_decode.assert_called_once_with(*mock_decode_args)
    # mock_oauth2_scheme.assert_called_once_with()


@patch.object(jwt, "decode")
@patch("api.v1.game.services.authentication.oauth2_scheme")
def test_validate_token_invalid_credentials(mock_oauth2_scheme: Mock, mock_decode: Mock, basic_app_settings: Settings):
    mock_oauth2_scheme.return_value = "123"
    mock_decode.return_value = {}
    token = mock_oauth2_scheme.return_value
    mock_decode_args = (token, basic_app_settings.SECRET_KEY, [basic_app_settings.TOKEN_ALGORITHM])

    with pytest.raises(HTTPException) as exc:
        validate_token(token)

    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc.value.detail == "Invalid credentials"
    assert exc.value.headers == {"WWW-Authenticate": "Bearer"}
    mock_decode.assert_called_once_with(*mock_decode_args)


@patch.object(jwt, "decode")
@patch("api.v1.game.services.authentication.oauth2_scheme")
def test_validate_token_internal_server_error(
    mock_oauth2_scheme: Mock, mock_decode: Mock, basic_app_settings: Settings
):
    mock_oauth2_scheme.return_value = "123"
    mock_decode.side_effect = JWTError("Simulated unexpected error during decoding")
    token = mock_oauth2_scheme.return_value
    mock_decode_args = (token, basic_app_settings.SECRET_KEY, [basic_app_settings.TOKEN_ALGORITHM])

    with pytest.raises(HTTPException) as exc:
        validate_token(token)

    assert exc.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert exc.value.detail == "Something unexpected happened"
    mock_decode.assert_called_once_with(*mock_decode_args)


@patch.object(User, "get_or_none")
@patch("api.v1.game.services.authentication.validate_token")
async def test_get_current_user(mock_validate_token: AsyncMock, mock_get_or_none: AsyncMock, basic_user: User):
    mock_validate_token.return_value = basic_user.username
    mock_get_or_none.return_value = basic_user

    result = await get_current_user(mock_validate_token.return_value)

    assert result == mock_get_or_none.return_value
    # mock_validate_token.assert_called_once()
    mock_get_or_none.assert_called_once_with(username=basic_user.username)


@pytest.mark.skip("Must fix!")
@patch.object(User, "get_or_none")
@patch("api.v1.game.services.authentication.validate_token")
async def test_get_current_user_user_is_not_found(
    mock_validate_token: AsyncMock, mock_get_or_none: AsyncMock, basic_user: User
):
    mock_validate_token.return_value = basic_user.username
    mock_get_or_none.return_value = None

    with pytest.raises(HTTPException) as exc:
        await get_current_user(mock_validate_token.return_value)

    assert exc.value.detail == f"User with {basic_user.username} not found"
    assert exc.value.status_code == status.HTTP_404_NOT_FOUND
    # mock_validate_token.assert_called_once()
    # mock_get_or_none.assert_called_once_with(username=basic_user.username)


@patch("api.v1.game.services.authentication.get_current_user")
async def test_get_current_active_user(mock_get_current_user: AsyncMock, basic_user: User):
    mock_get_current_user.return_value = basic_user

    result = await get_current_active_user(mock_get_current_user.return_value)

    assert result == mock_get_current_user.return_value
    # mock_get_current_user.assert_called_once_with(basic_user)


@patch("api.v1.game.services.authentication.get_current_user")
async def test_get_current_active_user_inactive_user(mock_get_current_user: AsyncMock, basic_user: User):
    basic_user.disabled = True
    mock_get_current_user.return_value = basic_user

    with pytest.raises(HTTPException) as exc:
        await get_current_active_user(mock_get_current_user.return_value)

    assert exc.value.detail == "Inactive user"
    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
    # mock_get_current_user.assert_called_once_with(test_user)
