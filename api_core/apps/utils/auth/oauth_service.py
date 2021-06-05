import abc
from abc import ABCMeta
from typing import Literal

from dependency_injector.wiring import Provide


class OAuthService(metaclass=ABCMeta):
    def __init__(
            self,
            oauth_type: Literal['GOOGLE_OAUTH', 'FACEBOOK_OAUTH'],
            oauth_conf: dict = Provide['config.OAUTH']
    ):
        self.oauth_type = oauth_type
        self.response_type = 'code'
        self.oauth_conf = oauth_conf

    @property
    def redirect_path(self) -> str:
        return self.oauth_conf.get('OAUTH_REDIRECT_PATH')

    @property
    def secret(self) -> str:
        return self.oauth_conf.get(f'{self.oauth_type}_SECRET')

    @property
    def client_id(self) -> str:
        return self.oauth_conf.get(f'{self.oauth_type}_CLIENT_ID')

    @property
    @abc.abstractmethod
    def scopes(self) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_config(self) -> dict:
        raise NotImplementedError()
