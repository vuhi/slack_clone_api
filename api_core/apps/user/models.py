import uuid

from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from api_core.apps.user import utils


class UserManage(BaseUserManager):
    """ Service class to handle user """

    def create_user(self, email: str, first_name: str, last_name: str, password: str, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        utils.validate_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **other_fields)

        utils.validate_weak_password(password)
        user.set_password(password)

        user.display_name = f'{first_name}.{last_name[0].upper()}'

        user.save()
        return user

    def create_superuser(self, email: str, first_name: str, last_name: str, password: str, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must be assigned to is_staff=True.'))
        if other_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must be assigned to is_superuser=True.'))

        return self.create_user(email, first_name, last_name, password, **other_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """ Custom user model """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True)

    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255, blank=False)
    display_name = models.CharField(max_length=255, default='')

    password = models.CharField(max_length=512)
    # password_salt = models.CharField(blank=False, default='')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_on = models.DateTimeField(default=timezone.now)
    modified_on = models.DateTimeField(auto_now=True)

    objects = UserManage()

    # https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#django.contrib.auth.models.CustomUser.USERNAME_FIELD
    USERNAME_FIELD = 'email'

    # https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#django.contrib.auth.models.CustomUser.REQUIRED_FIELDS
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f'{self.id}: {self.first_name} {self.last_name}'
