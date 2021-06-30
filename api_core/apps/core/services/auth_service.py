from typing import Type

from dependency_injector.wiring import Provide, inject

from django.utils import timezone

from api_core.apps.type import IOAuthService, IAuthService, RawToken

from .oauth_factory import OAuthFactory
from .login_strategies import RegularLoginStrategy, OAuthLoginStrategy
from ..db.auth.serializers import OAuthSerializer
from ..db.auth.model import Auth
from ..utils.auth.access_token import AccessToken
from ...type.service import ILoginStrategy, StrategyType


@inject
class AuthService(IAuthService):
    def __init__(self, oauth_factory: OAuthFactory = Provide['oauth_factory']):
        self.oauth_factory = oauth_factory
        self.Auth = Auth
        self.token = AccessToken()
        self.OAuthSerializer = OAuthSerializer
        self.RegularLoginStrategy = RegularLoginStrategy
        self.OAuthLoginStrategy = OAuthLoginStrategy

    def __get_oauth_service(self, oauth_type: str) -> IOAuthService:
        return self.oauth_factory.get_oauth_service(oauth_type)

    def __get_login_strategy_cls(self, oauth_type: str) -> Type[ILoginStrategy]:
        return self.RegularLoginStrategy if oauth_type is None else self.OAuthLoginStrategy

    def get_oauth_config(self, request_params: dict) -> dict:
        serializer = self.OAuthSerializer(data=request_params, required_fields=['oauth_type'])
        serializer.is_valid(raise_exception=True)

        oauth_service = self.__get_oauth_service(serializer.data.get('oauth_type'))
        return oauth_service.get_config()

    def login(self, request_body: dict) -> (RawToken, StrategyType):
        oauth_type = request_body.get('oauth_type', None)
        login_strategy_cls = self.__get_login_strategy_cls(oauth_type)

        login_strategy = login_strategy_cls(request_body, self.oauth_factory)
        login_strategy.validate_data()
        user = login_strategy.perform_login()

        user.last_login = timezone.now()
        user.save()

        return self.token.sign(str(user.id)), login_strategy.strategy_type

    def register_user(self):
        # serializer = UserSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # user = serializer.save()

        pass
