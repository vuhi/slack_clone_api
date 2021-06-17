from dependency_injector.wiring import Provide, inject

from django.db import models

from .fb_oauth import FaceBookOAuth
from .gg_oauth import GoogleOAuth

from api_core.apps.type import OAuthType, IOAuthService, OAuthUser


@inject
class AuthManager(models.Manager):
    def __init__(
        self,
        google_oauth: GoogleOAuth = Provide[OAuthType.GoogleOAuth.lower()],
        facebook_oauth: FaceBookOAuth = Provide[OAuthType.FaceBookOAuth.lower()],
    ):
        super(AuthManager, self).__init__()
        self.google_oauth = google_oauth
        self.facebook_oauth = facebook_oauth
        from api_core.apps.core.db.auth.serializers import OAuthSerializer
        self.OAuthSerializer = OAuthSerializer

    """ factory method to get correct oauth service by string name"""
    def __get_oauth_service(self, oauth_type: str) -> IOAuthService:
        return getattr(self, oauth_type.lower())

    def __oauth_login(self) -> str:
        pass

    def __regular_login(self) -> str:
        pass

    def get_oauth_config(self, request_params: dict) -> dict:
        serializer = self.OAuthSerializer(data=request_params, required_fields=['oauth_type'])
        serializer.is_valid(raise_exception=True)

        oauth_service = self.__get_oauth_service(serializer.data.get('oauth_type'))
        return oauth_service.get_config()

    def exchange_code_for_oauth_user(self, request_body: dict) -> OAuthUser:
        serializer = self.OAuthSerializer(data=request_body)
        serializer.is_valid(raise_exception=True)
        oauth_service = self.__get_oauth_service(serializer.data.get('oauth_type'))

        oauth_res = oauth_service.exchange_code(
            serializer.data.get('code'),
            serializer.data.get('redirect_origin')
        )

        oauth_user = oauth_service.get_oauth_user(oauth_res['access_token'])

        return oauth_user

    def login(self, oauth_type: OAuthType = None) -> str:



        # serializer = UserLoginSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # credential = serializer.data
        # try:
        #     user = User.objects.get_active_user(email=credential.get('email'))
        #     if not user.check_password(credential.get('password')):
        #         raise Exception('password does not match')
        #     token = AccessToken().sign(str(user.id))
        #     user.last_login = timezone.now()
        #     user.save()
        #
        #     return SuccessRes('user has been logged in successfully', {'token': token})
        # except Exception as e:
        #     raise InvalidLoginCredential()
        pass

    def update_or_create_oauth_user(self):
        pass

    def register_user(self):
        # serializer = UserSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # user = serializer.save()

        pass


