import traceback

from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.views import exception_handler

from api_core import settings


# Django DRF error handler func. It only handles APIException.
def drf_custom_exception_handler(exc, context):

    # Call REST framework's default exception handler first,
    res = exception_handler(exc, context)
    if res is not None and isinstance(res.data, dict):
        url = context['request'].build_absolute_uri()
        res.data['message'] = f'error of type: {type(exc).__name__}, has been thrown at: {url}'
        res.data['status'] = exc.status_code or status.HTTP_500_INTERNAL_SERVER_ERROR
        error_msg = res.data.pop('detail', None) or 'unknown error'
        res.data['error'] = error_msg.lower()
        if settings.DEBUG:
            res.data['trace'] = traceback.format_exc()

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
