"""Project package."""

from .di_containers import DIContainer
from . import settings

di_container = DIContainer()
di_container.config.from_dict({'JWT_TOKEN': settings.JWT_TOKEN})
di_container.config.from_dict({'OAUTH': settings.OAUTH})
