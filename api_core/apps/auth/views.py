from django.utils import timezone

from rest_framework.decorators import api_view
from rest_framework.request import Request

from api_core.apps.user.models import User
from api_core.apps.user.serializers import UserSerializer, UserLoginSerializer
from api_core.apps.utils.exceptions import InvalidLoginCredential
from api_core.apps.utils.response import SuccessRes
from api_core.apps.utils.token import AccessToken


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
