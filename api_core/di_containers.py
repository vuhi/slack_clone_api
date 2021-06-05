from dependency_injector import containers, providers

from api_core.apps.utils.auth.fb_oauth import FaceBookOAuth
from api_core.apps.utils.auth.gg_oauth import GoogleOAuth
from api_core.apps.utils.auth.oauth_factory import OAuthFactory


class DIContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    google_oauth = providers.Singleton(GoogleOAuth)
    facebook_oauth = providers.Singleton(FaceBookOAuth)
    oauth_factory = providers.Singleton(OAuthFactory)
