from __future__ import annotations
from datetime import datetime, timedelta

from wordle_api.user.models import User
from .models import User, UserSession
from abc import abstractmethod
from uuid import uuid4


class StoreException(Exception):
    pass


class StoreExceptionNotFound(StoreException):
    pass


class StoreExceptionUnexpected(StoreException):
    pass


class StoreExceptionAlreadyInUse(StoreException):
    pass


class UserStore:
    # aqui vamos a tener el equivalente a la base de datos donde guardaremos
    # usuarios con sus ids y contraseñas

    @abstractmethod
    def get_user(self, username: str) -> User:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> User:
        pass

    @abstractmethod
    def create_user(self, username: str, password: str) -> int:
        pass

    @abstractmethod
    def update_user(self, user: User) -> None:
        pass

    @abstractmethod
    def update_user_by_name(self, username: str, user: User) -> None:
        pass

    @abstractmethod
    def delete_user(self, username: str) -> None:
        pass

    @abstractmethod
    def delete_user_by_id(self, user_id: int) -> None:
        pass


class SessionStore:
    # sesiones activas de usuarios con sus token asociados y caducidad

    # podremos comprobar si un token esta activo y devolver el id del usuario asociado

    @abstractmethod
    def get_session(self, token: str) -> UserSession:
        pass

    @abstractmethod
    def get_session_by_id(self, session_id: int) -> UserSession:
        pass

    @abstractmethod
    def create_session(self, user_id) -> int:
        pass

    @abstractmethod
    def delete_session(self, session_id: int) -> None:
        pass


class SessionStoreDict(SessionStore):
    # sesiones activas de usuarios con sus token asociados y caducidad

    # podremos comprobar si un token esta activo y devolver el id del usuario asociado

    _instance: SessionStoreDict | None = None

    @classmethod
    def get_instance(cls) -> SessionStoreDict:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self) -> None:
        super().__init__()
        self.data: dict[int, UserSession] = {}
        self.token_index: dict[str, int] = {}
        self.last_session_id: int = 0

    def _get_new_session_id(self) -> int:
        self.last_session_id += 1
        return self.last_session_id

    def _get_new_token(self) -> str:
        return str(uuid4())

    def get_session(self, token: str) -> UserSession:
        if token not in self.token_index:
            message = f"Session expired: {token}"
            raise StoreExceptionNotFound(message)
        try:
            session_id = self.token_index[token]
            user_session = self.get_session_by_id(session_id)
            return user_session
        except Exception as e:
            raise StoreExceptionUnexpected(str(e))

    def get_session_by_id(self, session_id: int) -> UserSession:
        if session_id not in self.data:
            message = f"Session {session_id} not found"
            raise StoreExceptionNotFound(message)

        user_session = self.data[session_id]

        # if user_session.expiration_date < datetime.now():
        #    self.delete_session(session_id)
        #    message = f"Session expired: {user_session.token}"
        #    raise StoreExceptionNotFound(message)

        return user_session

    def create_session(self, user_id: int) -> int:
        try:
            new_session_id = self._get_new_session_id()
            token = self._get_new_token()
            date = datetime.now() + timedelta(days=1)  # esto lo ponemos para que el token dure 1 dia por defecto
            user_session = UserSession(session_id=new_session_id, user_id=user_id, token=token, expiration_date=date)
            self.data[new_session_id] = user_session
            self.token_index[token] = new_session_id
            return new_session_id
        except Exception as e:
            raise StoreExceptionUnexpected(str(e))

    def delete_session(self, session_id: int) -> None:
        if session_id not in self.data:
            message = f"User not found: {session_id}"
            raise StoreExceptionNotFound(message)
        try:
            user_session = self.get_session_by_id(session_id)
            self.data.pop(user_session.session_id)
            self.token_index.pop(user_session.token)
        except Exception as e:
            raise StoreExceptionUnexpected(str(e))

    def delete_session_by_token(self, token: str) -> None:
        if token not in self.token_index:
            message = f"Session expired: {token}"
            raise StoreExceptionNotFound(message)
        try:
            session_id = self.token_index[token]
            self.delete_session(session_id)
        except Exception as e:
            raise StoreExceptionUnexpected(str(e))


class UserStoreDict(UserStore):
    _instance: UserStoreDict | None = None

    @classmethod
    def get_instance(cls) -> UserStoreDict:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self) -> None:
        super().__init__()
        self.data: dict[int, User] = {}
        self.username_index: dict[str, int] = {}
        self.last_user_id = 0

    def _get_new_user_id(self) -> int:
        self.last_user_id += 1
        return self.last_user_id

    def _check_username_is_available(self, username: str) -> bool:
        return username not in self.username_index

    def create_user(self, username: str, password: str) -> int:
        if not self._check_username_is_available(username):
            message = f"Username {username} is unavailable"
            raise StoreExceptionAlreadyInUse(message)
        try:
            new_user_id = self._get_new_user_id()
            user = User(id=new_user_id, username=username, password=password)
            self.username_index[username] = new_user_id
            self.data[new_user_id] = user
            return new_user_id
        except Exception as e:
            raise StoreExceptionUnexpected(str(e))

    def get_user_by_id(self, user_id: int) -> User:
        if user_id not in self.data:
            message = f"User not found: {user_id}"
            raise StoreExceptionNotFound(message)
        try:
            return self.data[user_id]
        except Exception as e:
            raise StoreExceptionUnexpected(str(e))

    def get_user(self, username: str) -> User:
        if username not in self.username_index:
            message = f"User not found: {username}"
            raise StoreExceptionNotFound(message)
        try:
            user_id = self.username_index[username]
            user = self.get_user_by_id(user_id)
            return user
        except Exception as e:
            raise StoreExceptionUnexpected(str(e))

    def delete_user(self, user_id: int) -> None:
        if user_id not in self.data:
            message = f"User not found: {user_id}"
            raise StoreExceptionNotFound(message)
        try:
            username = self.data[user_id].username
            self.username_index.pop(username)
            self.data.pop(user_id)
        except Exception as e:
            raise StoreExceptionUnexpected(str(e))

    def update_user(self, user: User) -> None:
        old_user = self.get_user_by_id(user.id)
        if not self._check_username_is_available(user.username):
            message = f"Username {user.username} is unavailable"
            raise StoreExceptionAlreadyInUse(message)
        try:
            self.data[user.id] = user
            self.username_index.pop(old_user.username)
            self.username_index[user.username] = user.id
        except Exception as e:
            raise StoreExceptionUnexpected(str(e))


"""
metodo de instancia
metodo de clase 
metodo estatico

y todos esos metodos pueden ser concretos o abstractos.
aunque hacer un metodo estatico abstracto es un poco tonto
"""
