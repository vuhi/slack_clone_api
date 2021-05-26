from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import re


def validate_weak_password(password):
    pattern = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{10,}$'
    result = re.match(pattern, password)
    if not result:
        raise ValidationError(
            _("Password's too weak, must have at least one letter, "
              "one number, one special character & minimum 10 characters"),
            code='password_too_weak'
        )


def validate_email(email):
    pattern = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    result = re.match(pattern, email)
    if not result:
        raise ValidationError(
            _("You must provide a valid email address"),
            code='email_invalid'
        )


# class WeakPasswordValidator:
#     """ Custom password validation class"""
#
#     def validate(self, password, user=None):
#         validate_weak_password(password)
#
#     def get_help_text(self):
#         return _('Your password must have at least one letter, '
#                  'one number, one special character & minimum 10 characters')
