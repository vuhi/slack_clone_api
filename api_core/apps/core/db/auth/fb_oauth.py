import requests
import urllib.parse

from api_core.apps.type import OAuthType, IOAuthService, FaceBookOAuthResponse, FaceBookOAuthUser
from api_core.apps.core.utils.error.exceptions import OAuthError


class FaceBookOAuth(IOAuthService):
    def __init__(self):
        super().__init__(OAuthType.FaceBookOAuth)
        self.auth_type = 'rerequest'
        self.fields = ['id', 'name', 'email']

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

