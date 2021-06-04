from django.apps import AppConfig

from api_core import di_container


class Auth(AppConfig):
    name = 'api_core.apps.auth'
    label = 'auth_route'

    def ready(self):
        from . import views
        di_container.wire(modules=[views])
