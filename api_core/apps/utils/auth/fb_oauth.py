import os
import uuid

from .oauth_config import OAuthConfig
from .oauth_type import OAuthType


class FaceBookOAuth(OAuthConfig):
    def __init__(self):
        super().__init__(OAuthType.FaceBookOAuth.value)
        self.auth_type = 'rerequest'
        self.state = uuid.uuid4()

    @property
    def scopes(self) -> str:
        return os.environ.get(f'{self.oauth_type}_SCOPES')

    def get_config(self) -> dict:
        return {
            'redirect_path': self.redirect_path,
            'client_id': self.client_id,
            'scopes': self.scopes,
            'response_type': self.response_type,
            'state': self.state,
            'auth_type': self.auth_type
        }
