# """
# - Serializer class which gives you a powerful, generic way to control the output of your responses,
# - ModelSerializer class which provides a shortcut for creating serializers that deal with db instances and querysets.
# - https://www.django-rest-framework.org/api-guide/serializers/#serializers
# """
# from rest_framework import serializers
#
# from api_core.apps.user.models import User
# from api_core.apps.core.utils.helper.validation import validate_weak_password
#
#
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = [
#             'id', 'email', 'full_name', 'display_name',
#             'password', 'is_active', 'is_staff', 'created_on', 'modified_on'
#         ]
#         extra_kwargs = {'password': {'write_only': True, 'validators': [validate_weak_password]}}
#
#     # def create(self, validated_data):
#     #     return self.Meta.db.objects.create_user(**validated_data)
#
#
# # .save() will create a new instance.
# # serializer = CommentSerializer(data=data)
#
# # .save() will update the existing `comment` instance.
# # serializer = CommentSerializer(comment, data=data)