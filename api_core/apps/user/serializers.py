"""
- Serializer class which gives you a powerful, generic way to control the output of your responses,
- ModelSerializer class which provides a shortcut for creating serializers that deal with model instances and querysets.
- https://www.django-rest-framework.org/api-guide/serializers/#serializers
"""
from rest_framework import serializers

from api_core.apps.user.models import User
from api_core.apps.user.utils import validate_weak_password


# noinspection PyAbstractClass
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=True)
    password = serializers.CharField(max_length=512, required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'display_name',
            'password', 'is_active', 'is_staff', 'created_on', 'modified_on'
        ]
        extra_kwargs = {'password': {'write_only': True, 'validators': [validate_weak_password]}}

    def create(self, validated_data):
        return self.Meta.model.objects.create_user(**validated_data)
