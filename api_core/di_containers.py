from dependency_injector import containers, providers
from django.db import models

from api_core.apps.core.db.auth.fb_oauth import FaceBookOAuth
from api_core.apps.core.db.auth.gg_oauth import GoogleOAuth


class DIContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    google_oauth = providers.Singleton(GoogleOAuth)
    facebook_oauth = providers.Singleton(FaceBookOAuth)
    # logger = logging.get
    auth_service = providers.Dependency(instance_of=models.Model)
    # user_service = providers.Singleton(UserService)

