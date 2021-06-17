import traceback

from django.http import JsonResponse
from rest_framework import status

from api_core import settings


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
                data['trace'] = [trace.strip() for trace in traceback.format_exc().split(sep='\n') if trace]

        return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
