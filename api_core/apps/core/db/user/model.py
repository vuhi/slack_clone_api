import uuid

from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .manager import UserManage
# from ..auth.model import FaceBookAuth, GoogleAuth


class User(AbstractBaseUser, PermissionsMixin):
    """ Custom user db """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True)

    full_name = models.CharField(max_length=255, blank=False)
    display_name = models.CharField(max_length=255, default='', blank=True)

    password = models.CharField(max_length=512, default='', blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_on = models.DateTimeField(default=timezone.now)
    modified_on = models.DateTimeField(auto_now=True)

    # facebook_auth = models.OneToOneField(
    #     FaceBookAuth, on_delete=models.CASCADE,
    #     related_name='user', null=True, blank=True
    # )
    # google_auth = models.OneToOneField(
    #     GoogleAuth, on_delete=models.CASCADE,
    #     related_name='user', null=True, blank=True
    # )

    service = UserManage()

    # https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#django.contrib.auth.models.CustomUser.USERNAME_FIELD
    USERNAME_FIELD = 'email'

    # https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#django.contrib.auth.models.CustomUser.REQUIRED_FIELDS
    REQUIRED_FIELDS = ['full_name']

    class Meta:
        db_table = 'users'
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return f'User=[{f"{self.id}, {self.full_name}" if self.id else "DELETED"}]'


# @receiver(post_save, sender=User)
# def auto_save_oauth_if_attached(sender, instance: User, **kwargs):
#     if hasattr(instance, 'facebook_auth'):
#         instance.facebook_auth.save()
#     if hasattr(instance, 'google_auth'):
#         instance.google_auth.save()



