import jwt
from datetime import timedelta
from dependency_injector.wiring import inject, Provide

from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from api_core.apps.type import Claim, IToken, JWTConfig, RawToken
from ...utils.error.exceptions import TokenError


# https://pyjwt.readthedocs.io/en/stable/api.html
# https://pyjwt.readthedocs.io/en/stable/usage.html#encoding-decoding-tokens-with-rs256-rsa
@inject
class AccessToken(IToken):
    def __init__(self, exp_time: timedelta = None, jwt_conf: JWTConfig = Provide['config.JWT_TOKEN']):
        self.pub_key = jwt_conf.get('PUBLIC_KEY')
        self.private_key = jwt_conf.get('PRIVATE_KEY')
        self.exp_time = exp_time or jwt_conf.get('EXPIRATION_TIME')
        self.audience = jwt_conf.get('AUDIENCE')
        self.issuer = jwt_conf.get('ISSUER')
        self.algorithm = jwt_conf.get('ALGORITHM')
        self.type = 'access_token'

    def sign(self, user_id: str) -> RawToken:
        current_time = timezone.now()
        payload = dict()
        payload.setdefault(self.CLAIM.ID, user_id)
        payload.setdefault(self.CLAIM.ISSUER, self.issuer)
        payload.setdefault(self.CLAIM.AUDIENCE, self.audience)
        payload.setdefault(self.CLAIM.ISSUED_AT, current_time)
        payload.setdefault(self.CLAIM.EXP_TIME, current_time + self.exp_time)

        try:
            return jwt.encode(
                payload,
                self.private_key,
                algorithm=self.algorithm
            )
        except Exception as e:
            raise TokenError(_(f'token encoding error: {str(e)}'))

    def decode(self, raw_token: str, should_verify=True) -> Claim:
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
        except jwt.exceptions.ExpiredSignatureError as e:
            raise e
        except Exception as e:
            raise TokenError(_(f'token decoding error: {str(e)}'))
