from datetime import timedelta
from typing import TypedDict


class JWTConfig(TypedDict):
    PUBLIC_KEY: str
    PRIVATE_KEY: str
    TOKEN_PREFIX: tuple
    EXPIRATION_TIME: timedelta
    AUDIENCE: str
    ISSUER: str
    ALGORITHM: str
    TOKEN_PART_SEPARATOR: str
    TOKEN_HEADER: str


class OAuthConfig(TypedDict):
    OAUTH_REDIRECT_PATH: str
    GOOGLE_OAUTH_SCOPES: str
    GOOGLE_OAUTH_CLIENT_SECRET: str
    GOOGLE_OAUTH_CLIENT_ID: str
    GOOGLE_OAUTH_EXCHANGE_CODE_ENDPOINT: str
    FACEBOOK_OAUTH_CLIENT_ID: str
    FACEBOOK_OAUTH_CLIENT_SECRET: str
    FACEBOOK_OAUTH_SCOPES: str
    FACEBOOK_OAUTH_EXCHANGE_CODE_ENDPOINT: str
