from django.apps import AppConfig


class IocConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api_core.apps.ioc'

    # def ready(self):
    #     from api_core import settings
    #     from .di_containers import di_container
    #
    #     di_container.config.from_dict({'JWT_TOKEN': settings.JWT_TOKEN})
    #     di_container.config.from_dict({'OAUTH': settings.OAUTH})
    #     print('di_container.config.from_dict run!!!!!!!!!!')
