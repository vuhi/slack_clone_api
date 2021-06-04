from dependency_injector import containers, providers


class DIContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
