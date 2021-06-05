from django.apps import AppConfig

from api_core import di_container


class Utils(AppConfig):
    name = 'api_core.apps.utils'
    label = 'utils'

    def ready(self):
        from .auth import auth_class, access_token, oauth_service, oauth_factory
        di_container.wire(modules=[access_token, auth_class, oauth_service, oauth_factory])
