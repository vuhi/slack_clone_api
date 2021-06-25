from dependency_injector.wiring import Provide, inject

from rest_framework.decorators import api_view
from rest_framework.request import Request

from api_core.apps.core.db.auth.auth_service import AuthService
from api_core.apps.core.utils.res.success import SuccessRes


@api_view(['GET'])
@inject
def get_oauth_config(
    request: Request,
    auth_service: AuthService = Provide['auth_service']
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
def register_user(request: Request):
    # serializer = UserSerializer(data=request.data)
    # serializer.is_valid(raise_exception=True)
    # user = serializer.save()
    #
    # return SuccessRes('user has been registered successfully', user)
    pass


@api_view(['POST'])
@inject
def oauth_login(
    request: Request,
    auth_service: AuthService = Provide['auth_service'],
):
    """
    [POST]: api/auth/exchange/code
    :param  request.data[oauth_type], request.data[code], request.data[redirect_origin]
    :param  auth_service injected by DI
    :return { token: str }
    """
    oauth_user = auth_service.login(request.data)
    # is_user_exist = user_service.get_user(email=oauth_user['email'])
    # if not is_user_exist:
        # create user
        # pass
    # get id & generate token
    # print(user_service.test)

    return SuccessRes(f'successfully exchanging code', {'token': 'oauth_login'})


@api_view(['POST'])
def login(request: Request):
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
    return SuccessRes(f'successfully exchanging code', {'token': 'login'})
