from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api_core.apps.core'
    label = 'core'

    def ready(self):
        from api_core.apps.ioc.di_containers import di_container
        from .utils.auth import auth_class, access_token
        from .db.auth import fb_oauth, gg_oauth

        # very important step to inject the dependencies in DI to each module
        # wire will automatically inject dependencies to @inject
        print('di_container wire!!!!!!!!!!!!!!!!!!')
        di_container.wire(modules=[auth_class, access_token, fb_oauth, gg_oauth])


