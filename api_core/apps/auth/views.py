from dependency_injector.wiring import Provide, inject

from rest_framework.decorators import api_view
from rest_framework.request import Request

# from api_core.apps.core.service.auth import AuthService
# from api_core.apps.core.service.user import UserService
from api_core.apps.core.utils.res.success import SuccessRes


@api_view(['GET'])
@inject
def get_oauth_config(
    request: Request,
    # auth_service: AuthService = Provide['auth_service']
):
    # https://docs.djangoproject.com/en/3.2/ref/request-response/#django.http.QueryDict.dict
    # config = auth_service.get_oauth_config(request.GET.dict())
    return SuccessRes(f'successfully getting config', {'config': 'config'})


@api_view(['POST'])
@inject
def exchange_code_for_token(
    request: Request,
    # auth_service: AuthService = Provide['auth_service'],
    # user_service: UserService = Provide['user_service'],
):
    # oauth_user = auth_service.exchange_code_for_oauth_user(request.data)
    # is_user_exist = user_service.get_user(email=oauth_user['email'])
    # if not is_user_exist:
        # create user
        # pass
    # get id & generate token
    # print(user_service.test)

    return SuccessRes(f'successfully exchanging code', {'token': 'oauth_token'})


@api_view(['POST'])
def register_user(request: Request):
    # serializer = UserSerializer(data=request.data)
    # serializer.is_valid(raise_exception=True)
    # user = serializer.save()
    #
    # return SuccessRes('user has been registered successfully', user)
    pass


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
    pass
