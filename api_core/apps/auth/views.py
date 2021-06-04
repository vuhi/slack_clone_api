from dependency_injector.wiring import Provide, inject
from django.utils import timezone

from rest_framework.decorators import api_view
from rest_framework.request import Request

from api_core import DIContainer
from api_core.apps.user.models import User
from api_core.apps.user.serializers import UserSerializer, UserLoginSerializer
from api_core.apps.utils.error.exceptions import InvalidLoginCredential, RequiredParametersAbsent, MissMatchedType
from api_core.apps.utils.auth.gg_oauth import GoogleOAuth
from api_core.apps.utils.auth.oauth_type import OAuthType
from api_core.apps.utils.response import SuccessRes
from api_core.apps.utils.auth.access_token import AccessToken


@api_view(['GET'])
@inject
def get_oauth_config(request: Request):
    oauth_type: str = request.GET.get('oauth_type', None)

    if not oauth_type:
        raise RequiredParametersAbsent()

    if oauth_type not in OAuthType.values():
        raise MissMatchedType()

    # return SuccessRes(f'successfully getting ${oauth_type} config', {'config': ''})

    # config = GoogleOAuth()
    # print(config)
    return SuccessRes(f'successfully getting  config', {'config': 'config.JWT_TOKEN'})


@api_view(['POST'])
def register_user(request: Request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()

    return SuccessRes('user has been registered successfully', user)


@api_view(['POST'])
def login(request: Request):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    credential = serializer.data
    try:
        user = User.objects.get_active_user(email=credential.get('email'))
        if not user.check_password(credential.get('password')):
            raise Exception('password does not match')
        token = AccessToken().sign(str(user.id))
        user.last_login = timezone.now()
        user.save()

        return SuccessRes('user has been logged in successfully', {'token': token})
    except Exception as e:
        raise InvalidLoginCredential()
