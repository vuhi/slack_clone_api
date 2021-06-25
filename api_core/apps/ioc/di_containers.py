from dependency_injector import containers, providers

from api_core import settings
from api_core.apps.core.db.auth.auth_service import AuthService
from api_core.apps.core.db.auth.fb_oauth import FaceBookOAuth
from api_core.apps.core.db.auth.gg_oauth import GoogleOAuth
from api_core.apps.core.utils.auth.access_token import AccessToken
from api_core.apps.core.db.user.model import User


class DIContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    google_oauth = providers.Factory(GoogleOAuth)
    facebook_oauth = providers.Factory(FaceBookOAuth)

    auth_service = providers.Factory(AuthService)
    token_service = providers.Factory(AccessToken)
    user_service = providers.Factory(User)


di_container: DIContainer = DIContainer()
di_container.config.from_dict({'JWT_TOKEN': settings.JWT_TOKEN})
di_container.config.from_dict({'OAUTH': settings.OAUTH})





