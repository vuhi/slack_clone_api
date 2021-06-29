from dependency_injector.wiring import inject, Provide

from api_core.apps.type import OAuthType, IOAuthService


@inject
class OAuthFactory:
    def __init__(
        self,
        google_oauth=Provide[OAuthType.GoogleOAuth.lower()],
        facebook_oauth=Provide[OAuthType.FaceBookOAuth.lower()],
    ):
        self.google_oauth = google_oauth
        self.facebook_oauth = facebook_oauth

    def get_oauth_service(self, oauth_type: str) -> IOAuthService:
        return getattr(self, oauth_type.lower())
