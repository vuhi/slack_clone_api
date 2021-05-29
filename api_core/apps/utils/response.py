from typing import Any

from rest_framework.response import Response
from rest_framework import status


class SuccessRes(Response):

    def __init__(self, message: str, data: Any = None, *args, **kwargs):
        super().__init__(data, status.HTTP_200_OK, *args, **kwargs)
        self.data = dict()
        self.data['message'] = message.lower()
        self.data['status'] = self.status_code
        self.data['data'] = data
