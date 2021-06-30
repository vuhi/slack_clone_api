import uuid
from abc import ABCMeta, abstractmethod
from typing import Literal, TypedDict

from api_core.apps.core.db.user.model import User


class OAuthType:
    GoogleOAuth = 'GOOGLE_OAUTH'
    FaceBookOAuth = 'FACEBOOK_OAUTH'

    @classmethod
    def values(cls):
        return [cls.GoogleOAuth, cls.FaceBookOAuth]


class OAuthResponse(TypedDict):
    access_token: str
    expires_in: int
    token_type: str


class OAuthUser(TypedDict):
    id: str
    name: str
    email: str


class GoogleOAuthError(TypedDict):
    error: str
    error_description: str


class GoogleOAuthResponse(OAuthResponse, GoogleOAuthError):
    scope: str
    id_token: str


class GoogleAPIErrorDetail(TypedDict):
    code: int
    message: str
    status: str


class GoogleAPIError(TypedDict):
    error: GoogleAPIErrorDetail


class GoogleOAuthUser(OAuthUser, GoogleAPIError):
    verified_email: bool
    given_name: str
    family_name: str
    picture: str
    locale: str


class FaceBookOAuthErrorDetail(TypedDict):
    message: str
    type: str
    code: str
    error_subcode: str
    fbtrace_id: str


class FaceBookOAuthError(TypedDict):
    error: FaceBookOAuthErrorDetail


class FaceBookOAuthResponse(OAuthResponse, FaceBookOAuthError):
    auth_type: str


class FaceBookOAuthUser(OAuthUser, FaceBookOAuthError):
    pass


class IOAuthService(metaclass=ABCMeta):
    def __init__(
        self,
        oauth_type: Literal['GOOGLE_OAUTH', 'FACEBOOK_OAUTH'],
        oauth_conf: dict
    ):
        self.oauth_type = oauth_type
        self.response_type = 'code'
        self.oauth_conf = oauth_conf

    @property
    def state(self):
        return uuid.uuid4()

    @property
    def redirect_path(self) -> str:
        return self.oauth_conf.get('OAUTH_REDIRECT_PATH')

    @property
    def secret(self) -> str:
        return self.oauth_conf.get(f'{self.oauth_type}_CLIENT_SECRET')

    @property
    def client_id(self) -> str:
        return self.oauth_conf.get(f'{self.oauth_type}_CLIENT_ID')

    @property
    def exchange_endpoint(self) -> str:
        return self.oauth_conf.get(f'{self.oauth_type}_EXCHANGE_CODE_ENDPOINT')

    @property
    @abstractmethod
    def user_endpoint(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def scopes(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_config(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def exchange_code(self, code: str, redirect_origin: str) -> OAuthResponse:
        raise NotImplementedError

    @abstractmethod
    def get_oauth_user(self, oauth_token: str) -> OAuthUser:
        raise NotImplementedError

    # oauth login email always stays the same
    # the user's full name will be independence from user's full name in oauth user
    # if a person have two different social account -> 2 users will be created
    # get by oauth_id or create new record in oauth table
    @abstractmethod
    def oauth_login(self, oauth_user: OAuthUser) -> User:
        raise NotImplementedError

