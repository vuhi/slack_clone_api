from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import authentication
from rest_framework.request import Request

from api_core import settings
from api_core.apps.utils.exceptions import BadAuthHeader, InvalidToken, TokenError
from api_core.apps.utils.token import AccessToken


# https://www.django-rest-framework.org/api-guide/authentication/#custom-authentication
class JWTTokenAuthentication(authentication.BaseAuthentication):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_model = get_user_model()
        self.token_separator = settings.JWT_TOKEN.get('TOKEN_PART_SEPARATOR') or ' '
        self.token_prefix_tup = settings.JWT_TOKEN.get('TOKEN_PREFIX')
        self.header = settings.JWT_TOKEN.get('TOKEN_HEADER') or 'Authorization'

    def authenticate(self, request: Request):
        # https://docs.djangoproject.com/en/dev/ref/request-response/#django.http.HttpRequest.META
        header = request.headers.get(self.header)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        token = AccessToken()
        try:
            claims = token.decode(raw_token)
            user = self.user_model.objects.get(id=claims[AccessToken.id_claim])
            print(user.display_name)
            return user, None
        except TokenError as e:
            raise InvalidToken(_(str(e)))
        except Exception as e:
            raise InvalidToken(_(str(e)))

    def get_raw_token(self, header: str):
        parts = header.split(sep=self.token_separator)

        if len(parts) != 2:
            raise BadAuthHeader(_('Authorization header must contain two space-delimited values'))

        prefix = parts[0]
        if not prefix or prefix not in self.token_prefix_tup:
            raise BadAuthHeader(_('Invalid token prefix'))

        return parts[1]

