from django.contrib.auth.base_user import BaseUserManager
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from ...utils.helper import validation


class UserManage(BaseUserManager):
    """ Service class to handle user """

    def create_user(self, email: str, full_name: str, password: str, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        validation.validate_email(email)
        user = self.model(email=email, full_name=full_name, **other_fields)

        validation.validate_weak_password(password)
        user.set_password(password)

        user.display_name = email.split(sep='@')[0]

        user.save()
        return user

    def create_superuser(self, email: str, full_name: str, password: str, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must be assigned to is_staff=True.'))
        if other_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must be assigned to is_superuser=True.'))

        return self.create_user(email, full_name, password, **other_fields)

    def get_active_user(self, **identity):
        return self.get(Q(is_active=True), Q(**identity))
