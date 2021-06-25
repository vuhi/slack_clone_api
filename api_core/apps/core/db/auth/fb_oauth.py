import requests
import urllib.parse

from dependency_injector.wiring import inject, Provide

from api_core.apps.type import OAuthType, IOAuthService, FaceBookOAuthResponse, FaceBookOAuthUser, OAuthUser
from api_core.apps.core.utils.error.exceptions import OAuthError
from .model import FaceBookAuth
from ..user.model import User


@inject
class FaceBookOAuth(IOAuthService):
    def __init__(self, oauth_conf: dict = Provide['config.OAUTH']):
        super().__init__(OAuthType.FaceBookOAuth, oauth_conf)
        self.auth_type = 'rerequest'
        self.fields = ['id', 'name', 'email']
        self.FaceBookAuth = FaceBookAuth
        self.User = User

    @property
    def scopes(self) -> str:
        return self.oauth_conf.get(f'{self.oauth_type}_SCOPES')

    @property
    def user_endpoint(self) -> str:
        return 'https://graph.facebook.com/me'

    def get_config(self) -> dict:
        return {
            'redirect_path': self.redirect_path,
            'client_id': self.client_id,
            'scopes': self.scopes,
            'state': self.state,
            'response_type': self.response_type,
            'auth_type': self.auth_type
        }

    def exchange_code(self, code: str, redirect_origin: str) -> FaceBookOAuthResponse:
        params = {
            'client_id': self.client_id,
            'redirect_uri': f'{redirect_origin}{self.redirect_path}',
            'client_secret': self.secret,
            'code': code
        }
        encoded_params = urllib.parse.urlencode(params, safe='%')
        res = requests.get(self.exchange_endpoint, params=encoded_params)
        data: FaceBookOAuthResponse = res.json()
        if res.status_code != requests.codes.ok:
            raise OAuthError(data['error']['message'])
        return data

    def get_oauth_user(self, oauth_token: str) -> FaceBookOAuthUser:
        params = {
            'access_token': oauth_token,
            'fields': ','.join(self.fields),
        }
        res = requests.get(self.user_endpoint, params=params)
        data: FaceBookOAuthUser = res.json()
        if res.status_code != requests.codes.ok:
            raise OAuthError(data['error']['message'])

        return data

    def oauth_login(self, oauth_user: OAuthUser) -> User:
        # oauth login email always stays the same
        # if a person have two different social account -> 2 users will be created
        # get by oauth_id or create new record in oauth table
        facebook_auth, created = self.FaceBookAuth.service.get_or_create(
            oauth_id=oauth_user['id'],
            defaults={'oauth_id': oauth_user['id']}
        )

        # if created=true -> create a new user & associate with facebook_auth
        if created:
            user = self.User.service.create_user(
                email=oauth_user['email'],
                full_name=oauth_user['name'],
                password=None
            )
            user.facebook_auth = facebook_auth
            user.facebook_auth.save()
            return user

        return facebook_auth.user


