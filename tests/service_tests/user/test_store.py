# Standard Library
from unittest import mock

# Dependencies
import pytest

# From apps
from wordle_api.user.models import User
from wordle_api.user.store import StoreExceptionAlreadyInUse, StoreExceptionNotFound, UserStoreDict


@mock.patch.object(UserStoreDict, "get_user_by_id")
def test_get_user_success(m_get_user_by_id: mock.Mock, basic_user: User):
    user_storage = UserStoreDict()
    m_get_user_by_id.return_value = basic_user
    user_storage.data.update({basic_user.id: basic_user})
    user_storage.username_index.update({basic_user.username: basic_user.id})

    response = user_storage.get_user(basic_user.username)
    expected_response = m_get_user_by_id.return_value

    assert response == expected_response
    assert m_get_user_by_id.call_count == 1


def test_get_user_failure(basic_user: User):
    user_storage = UserStoreDict()
    message = f"User not found: {basic_user.username}"

    with pytest.raises(StoreExceptionNotFound) as excep_info:
        user_storage.get_user(basic_user.username)

    assert str(excep_info.value) == str(StoreExceptionNotFound(message))


@mock.patch.object(UserStoreDict, "_check_username_is_available")
@mock.patch.object(UserStoreDict, "_get_new_user_id")
def test_create_user_success(
    m__get_new_user_id: mock.Mock,
    m__check_username_is_available: mock.Mock,
    basic_user: User,
):
    user_storage = UserStoreDict()
    m__check_username_is_available.return_value = True
    m__get_new_user_id.return_value = 1

    response = user_storage.create_user(username="luis", password="123")
    expected_response = m__get_new_user_id.return_value
    user_created = user_storage.data.get(expected_response)

    assert response == expected_response
    assert user_created == basic_user
    assert m__check_username_is_available.call_count == 1
    assert m__get_new_user_id.call_count == 1


@mock.patch.object(UserStoreDict, "_check_username_is_available")
def test_create_user_already_in_use_failure(m__check_username_is_available: mock.Mock, basic_user: User):
    user_storage = UserStoreDict()
    m__check_username_is_available.return_value = False
    message = f"Username {basic_user.username} is unavailable"

    with pytest.raises(StoreExceptionAlreadyInUse) as excep_info:
        user_storage.create_user(basic_user.username, basic_user.password)

    assert str(excep_info.value) == str(StoreExceptionAlreadyInUse(message))
    assert m__check_username_is_available.call_count == 1


def test_delete_user_success(basic_user: User):
    user_storage = UserStoreDict()
    user_storage.data.update({basic_user.id: basic_user})

    response = user_storage.delete_user(basic_user.id)
    expected_response = None

    assert response == expected_response


def test_delete_user_not_found_failure(basic_user: User):
    user_storage = UserStoreDict()
    message = f"User not found: {basic_user.id}"

    with pytest.raises(StoreExceptionNotFound) as excep_info:
        user_storage.delete_user(basic_user.id)

    assert str(excep_info.value) == str(StoreExceptionNotFound(message))


@mock.patch.object(UserStoreDict, "_check_username_is_available")
@mock.patch.object(UserStoreDict, "get_user_by_id")
def test_update_user(m_get_user_by_id: mock.Mock, m__check_username_is_available: mock.Mock, basic_user: User):
    user_storage = UserStoreDict()
    user_storage.data.update({basic_user.id: basic_user})
    user_storage.username_index.update({basic_user.username: basic_user.id})
    m_get_user_by_id.return_value = basic_user
    m__check_username_is_available.return_value = True
    old_user = m_get_user_by_id.return_value
    updated_user = User(id=1, username="louis", password="12345")

    response = user_storage.update_user(updated_user)
    expected_response = None

    assert response == expected_response
    assert user_storage.data.get(basic_user.id) == updated_user
    assert old_user not in user_storage.data.values()
    assert m_get_user_by_id.call_count == 1
    assert m__check_username_is_available.call_count == 1


@mock.patch.object(UserStoreDict, "_check_username_is_available")
@mock.patch.object(UserStoreDict, "get_user_by_id")
def test_update_user_already_in_use_failure(
    m_get_user_by_id: mock.Mock,
    m_check_username_is_available: mock.Mock,
    basic_user: User,
):
    user_storage = UserStoreDict()
    m_get_user_by_id.return_value = basic_user
    m_check_username_is_available.return_value = False
    message = f"Username {basic_user.username} is unavailable"

    with pytest.raises(StoreExceptionAlreadyInUse) as excep_info:
        user_storage.update_user(basic_user)

    assert str(excep_info.value) == str(StoreExceptionAlreadyInUse(message))
