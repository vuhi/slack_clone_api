from jwt import ExpiredSignatureError
from dependency_injector.wiring import Provide, inject

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import authentication
from rest_framework.request import Request

from api_core import DIContainer
from api_core.apps.user.models import User
from api_core.apps.utils.error.exceptions import BadAuthHeader, InvalidToken, TokenError
from api_core.apps.utils.auth.access_token import AccessToken


# https://www.django-rest-framework.org/api-guide/authentication/#custom-authentication
# This class will generate a new instance everytime it runs
@inject
class JWTTokenAuthentication(authentication.BaseAuthentication):

    def __init__(self, jwt_conf: dict = Provide[DIContainer.config.JWT_TOKEN], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_model: User = get_user_model()
        self.token_separator: str = jwt_conf.get('TOKEN_PART_SEPARATOR') or ' '
        self.token_prefix_tup: tuple[str] = jwt_conf.get('TOKEN_PREFIX')
        self.header: str = jwt_conf.get('TOKEN_HEADER') or 'Authorization'

    def authenticate(self, request: Request):
        # https://docs.djangoproject.com/en/dev/ref/request-response/#django.http.HttpRequest.META
        header = request.headers.get(self.header)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        token = AccessToken()
        try:
            claims = token.decode(raw_token)
            user = self.user_model.objects.get_active_user(id=claims[AccessToken.id_claim])
            return user, None
        except ExpiredSignatureError as e:
            raise InvalidToken(_(str(e)))
        except TokenError as e:
            raise InvalidToken(_('malformed token received'))
        except Exception as e:
            raise InvalidToken(_('invalid token received'))

    def get_raw_token(self, header: str):
        parts = header.split(sep=self.token_separator)

        if len(parts) != 2:
            raise BadAuthHeader(_('Authorization header must contain two space-delimited values'))

        prefix = parts[0]
        if not prefix or prefix not in self.token_prefix_tup:
            raise BadAuthHeader(_('Invalid token prefix'))

        return parts[1]

