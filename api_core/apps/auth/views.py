from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api_core.apps.utils.token import AccessToken


@api_view(['POST'])
def login(request):
    return Response({'token': AccessToken().sign('uuid')})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response({'msg': 'yeahh!!!'})
