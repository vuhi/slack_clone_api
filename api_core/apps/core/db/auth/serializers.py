from rest_framework import serializers

from api_core.apps.type import OAuthType
from api_core.apps.core.utils.error.exceptions import RequiredParametersAbsent


class OAuthSerializer(serializers.Serializer):
    oauth_type = serializers.CharField(max_length=50)
    code = serializers.CharField(max_length=500)
    redirect_origin = serializers.URLField(max_length=200)
    
    def __init__(self, *args, required_fields: list = None, **kwargs):
        super(OAuthSerializer, self).__init__(*args, **kwargs)
        if required_fields is not None:
            existing_fields = self.fields
            for remove_field in set(existing_fields) - set(required_fields):
                self.fields.pop(remove_field)

        try:
            data: dict = kwargs.get('data', None)
            if data is None:
                raise Exception('OAuthSerializer was not initialed correctly: missing initial value')
            missing_required_fields = list(set(self.fields) - set(data.keys()))
            if len(missing_required_fields) > 0:
                raise Exception(f'required fields missing: {missing_required_fields}')
        except Exception as e:
            raise RequiredParametersAbsent

    def validate_oauth_type(self, value: str):
        if value not in OAuthType.values():
            raise serializers.ValidationError('Invalid oauth_type')
        return value


# noinspection PyAbstractClass
class OAuthLoginBody(serializers.Serializer):
    oauth_type = serializers.CharField(max_length=50)
    email = serializers.EmailField(max_length=255)


# noinspection PyAbstractClass
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=512)








