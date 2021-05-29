from datetime import timedelta

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from api_core.apps.utils.authentication import JWTTokenAuthentication
from api_core.apps.utils.response import SuccessRes
from api_core.apps.utils.token import AccessToken


@api_view(['GET'])
def ping(request: Request):
    return SuccessRes('ping has been successfully received', 'pong')


@api_view(['GET'])
@authentication_classes([JWTTokenAuthentication])
@permission_classes([IsAuthenticated])
def protected_ping(request: Request):
    user = {'id': request.user.id, 'email': request.user.email}
    return SuccessRes('Yeah!!. This route was protected behind jwt token!', {'user': user})


@api_view(['GET'])
def generate_token(request: Request):
    time_by_second = request.GET.get('time_by_second', None)
    user_id = request.GET.get('user_id', None)
    exp_time = timedelta(seconds=int(time_by_second)) if time_by_second is not None else None
    token = AccessToken(exp_time)
    signed_token = token.sign(user_id=user_id)
    return SuccessRes('token has been successfully generated', {'token': signed_token})


@api_view(['GET'])
def capture_normal_exception(request: Request):
    x = 1/0
    return SuccessRes('it should never reach here')


@api_view(['GET'])
def capture_api_exception(request: Request):
    raise APIException('test api exception')

