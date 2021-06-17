from django.apps import AppConfig

from api_core import di_container


class AuthConfig(AppConfig):
    name = 'api_core.apps.auth'
    label = 'auth_route'

    def ready(self):
        from . import views
        # very important step to inject the dependencies in DI to each module
        # wire will automatically inject dependencies to @inject
        di_container.wire(modules=[views])
        print('AuthConfig ')
