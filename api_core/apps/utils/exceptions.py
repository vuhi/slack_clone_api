from rest_framework import exceptions, status


class BadAuthHeader(exceptions.APIException):
    """ malformed header exception """
    status_code = status.HTTP_401_UNAUTHORIZED
    default_code = 'bad_authorization_header'


class InvalidToken(exceptions.APIException):
    """ malformed token exception """
    status_code = status.HTTP_401_UNAUTHORIZED
    default_code = 'invalid_token'


class TokenError(Exception):
    """ token exception while decode or sign"""
    pass


class InvalidLoginCredential(exceptions.APIException):
    """ login failed exception """
    status_code = status.HTTP_401_UNAUTHORIZED
    default_code = 'bad_credential'
    default_detail = 'invalid credential, please check your login credentials'
