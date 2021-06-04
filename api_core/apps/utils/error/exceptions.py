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


class RequiredParametersAbsent(exceptions.APIException):
    """ missing required parameters exception """
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'missing_parameters'
    default_detail = 'one or more required parameters were missing'


class MissMatchedType(exceptions.APIException):
    """ incorrect type exception """
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'miss_matched_type'
    default_detail = 'supplied argument(s) type does not match'

