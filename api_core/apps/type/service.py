from abc import ABCMeta, abstractmethod

from .oauth import OAuthUser
from .token import RawToken
from ..core.db.user.model import User
from ..core.services.oauth_factory import OAuthFactory


class ILoginStrategy(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, request_body: dict, oauth_factory: OAuthFactory = None):
        raise NotImplementedError

    @abstractmethod
    def validate_data(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def perform_login(self) -> User:
        raise NotImplementedError


class IAuthService(metaclass=ABCMeta):
    @abstractmethod
    def get_oauth_config(self, request_params: dict) -> dict:
        raise NotImplementedError

    @abstractmethod
    def login(self, login_strategy: ILoginStrategy) -> RawToken:
        raise NotImplementedError

    @abstractmethod
    def register_user(self) -> None:
        raise NotImplementedError

