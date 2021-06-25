from django.apps import AppConfig


class AuthConfig(AppConfig):
    name = 'api_core.apps.auth'
    label = 'auth_route'

    def ready(self):
        from . import views
        from api_core.apps.ioc.di_containers import di_container

        # very important step to inject the dependencies in DI to each module
        # wire will automatically inject dependencies to @inject
        di_container.wire(modules=[views])
