from api_core.apps.type.service import ILoginStrategy
from ..db.auth.serializers import RegularLoginSerializer, OAuthSerializer
from ..db.user.model import User
from ..services.oauth_factory import OAuthFactory
from ..utils.error.exceptions import InvalidLoginCredential


class RegularLoginStrategy(ILoginStrategy):
    def __init__(self, request_body: dict, *args):
        self.request_body = request_body
        self.serializer = RegularLoginSerializer(data=request_body)

    def validate_data(self) -> None:
        self.serializer.is_valid(raise_exception=True)

    def perform_login(self) -> User:
        credential = self.serializer.data
        try:
            user = User.service.get_active_user(email=credential.get('email'))
            if not user.check_password(credential.get('password')):
                raise Exception('password does not match')
            return user
        except Exception as e:
            raise InvalidLoginCredential


class OAuthLoginStrategy(ILoginStrategy):
    def __init__(self, request_body: dict, oauth_factory: OAuthFactory):
        self.request_body = request_body
        self.serializer = OAuthSerializer(data=request_body)
        self.oauth_factory = oauth_factory

    def validate_data(self) -> None:
        self.serializer.is_valid(raise_exception=True)

    def perform_login(self) -> User:
        oauth_type = self.serializer.data.get('oauth_type')
        code = self.serializer.data.get('code')
        redirect_origin = self.serializer.data.get('redirect_origin')

        oauth_service = self.oauth_factory.get_oauth_service(oauth_type)
        oauth_res = oauth_service.exchange_code(code, redirect_origin)

        oauth_user = oauth_service.get_oauth_user(oauth_res['access_token'])
        user = oauth_service.oauth_login(oauth_user)
        return user
