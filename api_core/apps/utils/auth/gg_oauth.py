import os

from .oauth_config import OAuthConfig
from .oauth_type import OAuthType


class GoogleOAuth(OAuthConfig):
    def __init__(self):
        super().__init__(OAuthType.GoogleOAuth.value)

    @property
    def scopes(self) -> str:
        scopes = os.environ.get(f'{self.oauth_type}_SCOPES')
        return ' '.join(scopes.split(sep=','))

    def get_config(self) -> dict:
        return {
            'redirect_path': self.redirect_path,
            'client_id': self.client_id,
            'scopes': self.scopes,
            'response_type': self.response_type
        }
