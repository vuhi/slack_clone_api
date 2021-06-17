from django.apps import AppConfig

from api_core import di_container


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api_core.apps.core'
    label = 'core'

    def ready(self):
        pass
        # from .user import user_service
        # from api_core.apps.core.service.auth import fb_oauth
        # from api_core.apps.core.service.auth import gg_oauth
        # from api_core.apps.core.service.auth import auth_service
        from .utils.auth import auth_class, access_token

        # very important step to inject the dependencies in DI to each module
        # wire will automatically inject dependencies to @inject
        di_container.wire(modules=[auth_class, access_token])

    # from django.apps import AppConfig
    #
    # from api_core import di_container
    #
    # class UtilsConfig(AppConfig):
    #     name = 'api_core.apps.core.utils'
    #     label = 'utils'
    #
    #     def ready(self):
    #         from .auth import auth_class, access_token
    #         # very important step to inject the dependencies in DI to each module
    #         # wire will automatically inject dependencies to @inject
    #         di_container.wire(modules=[access_token, auth_class])

