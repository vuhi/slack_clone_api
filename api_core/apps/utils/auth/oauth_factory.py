from dependency_injector.wiring import Provide

from .fb_oauth import FaceBookOAuth
from .gg_oauth import GoogleOAuth
from .oauth_service import OAuthService


class OAuthFactory:
    def __init__(
            self,
            google_oauth: GoogleOAuth = Provide['google_oauth'],
            facebook_oauth: FaceBookOAuth = Provide['facebook_oauth']
    ):
        self.google_oauth = google_oauth
        self.facebook_oauth = facebook_oauth

    def get_service(self, oauth_type: str) -> OAuthService:
        return getattr(self, oauth_type.lower())
