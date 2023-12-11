# Standard Library
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, Mock, patch

# Dependencies
import pytest
from fastapi import HTTPException, status
from jose import JWTError

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
@patch("api.v1.game.services.authentication.jwt.encode", return_value="test_encoded_token")
@patch("api.v1.game.services.authentication.datetime")
def test_create_access_token(
    mock_datetime: Mock, mock_encode: Mock, expires_delta: timedelta | None, basic_app_settings: Settings
):
    test_data = {"sub": "test_username"}
    fixed_date = datetime(2023, 12, 1)
    expires_delta = expires_delta if expires_delta else timedelta(minutes=basic_app_settings.ACCESS_TOKEN_LIFETIME)
    mock_datetime.now.return_value = fixed_date

    encoded_token = create_access_token(test_data, expires_delta)
    test_data.update({"exp": mock_datetime.now() + expires_delta})

    assert encoded_token == mock_encode.return_value
    mock_encode.assert_called_once_with(
        test_data,
        basic_app_settings.SECRET_KEY,
        basic_app_settings.TOKEN_ALGORITHM,
    )
    mock_datetime.now.assert_called_with()
    mock_datetime.now.call_count == 2


@patch("api.v1.game.services.authentication.jwt.decode", return_value={"sub": "test_username"})
@patch("api.v1.game.services.authentication.oauth2_scheme", return_value="123")
def test_validate_token(mock_oauth2_scheme: Mock, mock_decode: Mock, basic_app_settings: Settings):
    token = mock_oauth2_scheme.return_value
    expected_result = mock_decode.return_value["sub"]
    mock_decode_args = (token, basic_app_settings.SECRET_KEY, [basic_app_settings.TOKEN_ALGORITHM])

    result = validate_token(token)

    assert result == expected_result
    mock_decode.assert_called_once_with(*mock_decode_args)
    # mock_oauth2_scheme.assert_called_once_with()


@pytest.mark.parametrize(
    "payload, side_effect, expected_exc_status_code, expected_exc_detail, expected_exc_headers",
    [
        pytest.param(
            {},
            None,
            status.HTTP_401_UNAUTHORIZED,
            "Invalid credentials",
            {"WWW-Authenticate": "Bearer"},
            id="Invalid Credentials",
        ),
        pytest.param(
            None,
            JWTError("Simulated unexpected error during decoding"),
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Something unexpected happened",
            None,
            id="Internal Server Error",
        ),
    ],
)
@patch("api.v1.game.services.authentication.jwt.decode")
@patch("api.v1.game.services.authentication.oauth2_scheme", return_value="123")
def test_validate_token_raise_exc(
    mock_oauth2_scheme: Mock,
    mock_decode: Mock,
    payload: dict | None,
    side_effect: JWTError | None,
    expected_exc_status_code: status,
    expected_exc_detail: str,
    expected_exc_headers: dict[str, str] | None,
    basic_app_settings: Settings,
):
    token = mock_oauth2_scheme.return_value
    mock_decode.return_value = payload
    mock_decode.side_effect = side_effect
    mock_decode_args = (token, basic_app_settings.SECRET_KEY, [basic_app_settings.TOKEN_ALGORITHM])

    with pytest.raises(HTTPException) as exc:
        validate_token(token)

    assert exc.value.status_code == expected_exc_status_code
    assert exc.value.detail == expected_exc_detail
    assert exc.value.headers == expected_exc_headers
    mock_decode.assert_called_once_with(*mock_decode_args)


@patch("api.v1.game.services.authentication.User.get_or_none")
@patch("api.v1.game.services.authentication.validate_token")
async def test_get_current_user(mock_validate_token: AsyncMock, mock_get_or_none: AsyncMock, basic_user: User):
    mock_validate_token.return_value = basic_user.username
    mock_get_or_none.return_value = basic_user
    username = mock_validate_token.return_value
    expected_result = mock_get_or_none.return_value

    result = await get_current_user(username)

    assert result == expected_result
    # mock_validate_token.assert_called_once()
    mock_get_or_none.assert_called_once_with(username=username)


@patch("api.v1.game.services.authentication.User.get_or_none", new_callable=AsyncMock, return_value=None)
@patch("api.v1.game.services.authentication.validate_token")
async def test_get_current_user_user_is_not_found(
    mock_validate_token: AsyncMock, mock_get_or_none: AsyncMock, basic_user: User
):
    mock_validate_token.return_value = basic_user.username
    username = mock_validate_token.return_value

    with pytest.raises(HTTPException) as exc:
        await get_current_user(username)

    assert exc.value.detail == f"User with {username=} not found"
    assert exc.value.status_code == status.HTTP_404_NOT_FOUND
    # mock_validate_token.assert_called_once()
    mock_get_or_none.assert_called_once_with(username=username)


@patch("api.v1.game.services.authentication.get_current_user")
async def test_get_current_active_user(mock_get_current_user: AsyncMock, basic_user: User):
    mock_get_current_user.return_value = basic_user
    current_user = mock_get_current_user.return_value
    expected_result = current_user

    result = await get_current_active_user(current_user)

    assert result == expected_result
    # mock_get_current_user.assert_called_once()


@patch("api.v1.game.services.authentication.get_current_user")
async def test_get_current_active_user_inactive_user(mock_get_current_user: AsyncMock, basic_user: User):
    basic_user.disabled = True
    mock_get_current_user.return_value = basic_user
    current_user = mock_get_current_user.return_value

    with pytest.raises(HTTPException) as exc:
        await get_current_active_user(current_user)

    assert exc.value.detail == "Inactive user"
    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
    # mock_get_current_user.assert_called_once_with(username)
