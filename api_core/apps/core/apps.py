from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api_core.apps.core'
    label = 'core'

    def ready(self):
        from api_core.apps.ioc.di_containers import di_container
        from .utils.auth import auth_class, access_token
        from .services import gg_oauth
        from .services import fb_oauth
        from .services import oauth_factory
        from .services import auth_service

        # very important step to inject the dependencies in DI to each module
        # wire will automatically inject dependencies to @inject
        di_container.wire(
            modules=[
                auth_class, access_token,
                auth_service,
                oauth_factory, fb_oauth, gg_oauth,
            ]
        )


