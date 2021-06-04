import abc
import os
from abc import ABCMeta
from typing import Literal


class OAuthConfig(metaclass=ABCMeta):
    def __init__(self, oauth_type: Literal['GOOGLE_OAUTH', 'FACEBOOK_OAUTH']):
        self.oauth_type = oauth_type
        self.response_type = 'code'

    @property
    def redirect_path(self) -> str:
        return os.environ.get('OAUTH_REDIRECT_PATH')

    @property
    def secret(self) -> str:
        return os.environ.get(f'{self.oauth_type}_SECRET')

    @property
    def client_id(self) -> str:
        return os.environ.get(f'{self.oauth_type}_CLIENT_ID')

    @property
    @abc.abstractmethod
    def scopes(self) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_config(self) -> dict:
        raise NotImplementedError()
