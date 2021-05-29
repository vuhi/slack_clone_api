import traceback

from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler

from api_core import settings


# Django DRF error handler func. It only handles APIException.
def drf_custom_exception_handler(exception, context):

    # Call REST framework's default exception handler first,
    res = exception_handler(exception, context)
    if res is not None:
        data = dict()
        url = context['request'].build_absolute_uri()
        data['message'] = f'error of type: {type(exception).__name__}, has been thrown at: {url}'
        data['status'] = exception.status_code or status.HTTP_500_INTERNAL_SERVER_ERROR

        if isinstance(exception, ValidationError):
            details = exception.detail
            data['error'] = details
        elif isinstance(res.data, dict) and 'detail' in res.data:
            data['error'] = res.data.get('detail').lower()

        if settings.DEBUG:
            data['trace'] = [trace.strip() for trace in traceback.format_exc().split(sep='\n') if trace]

        res.data = data
    return res


# https://docs.djangoproject.com/en/3.2/topics/http/middleware/
# Normal Exception need to handle with Django Middleware
class ErrorHandlerMiddleware:
    # required
    def __init__(self, get_response):
        self.get_response = get_response

    # required
    def __call__(self, request):
        return self.get_response(request)

    # noinspection PyMethodMayBeStatic
    def process_exception(self, request, exception):
        data = dict()
        if exception:
            url = request.build_absolute_uri()
            data['message'] = f'error of type: {type(exception).__name__}, has been thrown at: {url}'
            data['status'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            data['error'] = str(exception).lower()
            if settings.DEBUG:
                data['trace'] = traceback.format_exc()

        return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
