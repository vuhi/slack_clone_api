from dependency_injector.wiring import Provide, inject

from rest_framework.decorators import api_view
from rest_framework.request import Request

# from api_core.apps.core.services.auth_service import AuthService
from api_core.apps.core.utils.res.success import SuccessRes
from api_core.apps.type import IAuthService


@api_view(['GET'])
@inject
def get_oauth_config(
    request: Request,
    auth_service: IAuthService = Provide['auth_service']
):
    """
    [GET]: api/auth/login/config
    :param  request[oauth_type]
    :param  auth_service injected by DI
    :return { config: dict } -> to construct oauth2 login url
    """
    # https://docs.djangoproject.com/en/3.2/ref/request-response/#django.http.QueryDict.dict
    config = auth_service.get_oauth_config(request.GET.dict())
    return SuccessRes(f'successfully getting config', {'config': config})


@api_view(['POST'])
@inject
def register_user(request: Request):
    # serializer = UserSerializer(data=request.data)
    # serializer.is_valid(raise_exception=True)
    # user = serializer.save()
    #
    # return SuccessRes('user has been registered successfully', user)
    pass


@api_view(['POST'])
@inject
def login(
    request: Request,
    auth_service: IAuthService = Provide['auth_service']
):
    """
    [POST]: api/auth/login
    :param  request.data[email], request.data[password] --> normal flow
            or
            request.data[oauth_type], request.data[code], request.data[redirect_origin] --> oauth flow
    :param  auth_service injected by DI
    :return { token: str }
    """
    token = auth_service.login(request.data)
    return SuccessRes(f'successfully login in with normal flow', {'token': token})




