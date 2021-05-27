from datetime import timedelta

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api_core.apps.utils.token import AccessToken


@api_view(['GET'])
def ping(request):
    return Response({'message': 'pong'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_ping(request):
    return Response({'message': 'Yeah!!. This route was protected behind jwt token!'})


@api_view(['GET'])
def generate_token(request):
    time_by_second = request.GET.get('time_by_second', None)
    exp_time = timedelta(seconds=int(time_by_second)) if time_by_second is not None else None
    token = AccessToken(exp_time)
    signed_token = token.sign(user_id='dummy_id')
    return Response({'token': signed_token})

