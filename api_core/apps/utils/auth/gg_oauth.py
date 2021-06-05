from .oauth_service import OAuthService
from .oauth_type import OAuthType


class GoogleOAuth(OAuthService):
    def __init__(self):
        super().__init__(OAuthType.GoogleOAuth.value)

    @property
    def scopes(self) -> str:
        scopes = self.oauth_conf.get(f'{self.oauth_type}_SCOPES')
        return ' '.join(scopes.split(sep=','))

    def get_config(self) -> dict:
        return {
            'redirect_path': self.redirect_path,
            'client_id': self.client_id,
            'scopes': self.scopes,
            'response_type': self.response_type
        }
