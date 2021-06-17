import urllib.parse
import requests

from api_core.apps.type import OAuthType, IOAuthService, GoogleOAuthResponse, GoogleOAuthUser
from api_core.apps.core.utils.error.exceptions import OAuthError


class GoogleOAuth(IOAuthService):
    def __init__(self):
        super().__init__(OAuthType.GoogleOAuth)
        self.grant_type = 'authorization_code'

    @property
    def scopes(self) -> str:
        scopes = self.oauth_conf.get(f'{self.oauth_type}_SCOPES')
        return ' '.join(scopes.split(sep=','))

    @property
    def user_endpoint(self) -> str:
        return 'https://www.googleapis.com/oauth2/v1/userinfo?alt=json'

    def get_config(self) -> dict:
        return {
            'redirect_path': self.redirect_path,
            'client_id': self.client_id,
            'scopes': self.scopes,
            'state': self.state,
            'response_type': self.response_type
        }

    def exchange_code(self, code: str, redirect_origin: str) -> GoogleOAuthResponse:
        params = {
            'client_id': self.client_id,
            'redirect_uri': f'{redirect_origin}{self.redirect_path}',
            'client_secret': self.secret,
            'grant_type': self.grant_type,
            'code': code
        }
        encoded_params = urllib.parse.urlencode(params, safe='%')
        res = requests.post(self.exchange_endpoint, params=encoded_params)
        data: GoogleOAuthResponse = res.json()
        if res.status_code != requests.codes.ok:
            raise OAuthError('{0}. {1}'.format(data['error'], data['error_description']))
        return data

    def get_oauth_user(self, oauth_token: str) -> GoogleOAuthUser:
        headers = {
            'Authorization': f'Bearer {oauth_token}'
        }
        res = requests.get(self.user_endpoint, headers=headers)
        data: GoogleOAuthUser = res.json()
        if res.status_code != requests.codes.ok:
            raise OAuthError('{0}. {1}'.format(data['error']['status'], data['error']['message']))

        return data
