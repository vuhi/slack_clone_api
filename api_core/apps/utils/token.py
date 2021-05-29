import jwt
from datetime import timedelta

from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from api_core import settings
from api_core.apps.utils.exceptions import TokenError


# https://pyjwt.readthedocs.io/en/stable/api.html
# https://pyjwt.readthedocs.io/en/stable/usage.html#encoding-decoding-tokens-with-rs256-rsa
class AccessToken:
    token_type = 'access_token'
    id_claim = 'id'
    iss_claim = 'iss'
    aud_claim = 'aud'
    iat_claim = 'iat'
    exp_claim = 'exp'

    def __init__(self, exp_time: timedelta = None):
        self.pub_key = settings.JWT_TOKEN.get('PUBLIC_KEY')
        self.private_key = settings.JWT_TOKEN.get('PRIVATE_KEY')
        self.exp_time = exp_time or settings.JWT_TOKEN.get('EXPIRATION_TIME')
        self.audience = settings.JWT_TOKEN.get('AUDIENCE')
        self.issuer = settings.JWT_TOKEN.get('ISSUER')
        self.algorithm = 'RS256'

    def sign(self, user_id: str) -> str:
        current_time = timezone.now()
        payload = dict()
        payload.setdefault(AccessToken.id_claim, user_id)
        payload.setdefault(AccessToken.iss_claim, self.issuer)
        payload.setdefault(AccessToken.aud_claim, self.audience)
        payload.setdefault(AccessToken.iat_claim, current_time)
        payload.setdefault(AccessToken.exp_claim, current_time + self.exp_time)

        try:
            return jwt.encode(
                payload,
                self.private_key,
                algorithm=self.algorithm
            )
        except Exception as e:
            raise TokenError(_(f'token encoding error: {str(e)}'))

    def decode(self, raw_token: str, should_verify=True) -> dict:
        if raw_token is None or not raw_token or raw_token.isspace():
            raise TokenError(_('failed to initiate token. Invalid parameter'))
        try:
            return jwt.decode(
                jwt=raw_token,
                key=self.pub_key,
                algorithms=[self.algorithm],
                options={
                    'require': ['exp', 'iat', 'aud', 'iss', 'id'],
                    'verify_aud': True,
                    'verify_iat': True,
                    'verify_exp': True,
                    'verify_iss': True,
                    'verify_signature': should_verify
                },
                audience=[self.audience],
                issuer=self.issuer,
            )
        except Exception as e:
            raise TokenError(_(f'token decoding error: {str(e)}'))
