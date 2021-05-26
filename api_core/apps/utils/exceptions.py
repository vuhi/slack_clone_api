from rest_framework import exceptions, status


class BadAuthHeader(exceptions.AuthenticationFailed):
    """ malformed token exception """
    status_code = status.HTTP_401_UNAUTHORIZED
    default_code = 'bad_authorization_header'


class InvalidToken(exceptions.AuthenticationFailed):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_code = 'invalid_token'


class TokenError(Exception):
    pass