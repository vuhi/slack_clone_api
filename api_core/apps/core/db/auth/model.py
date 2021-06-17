import uuid

from django.db import models

from ..user.model import User
from .manager import AuthManager


class Auth(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    oauth_id = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    # user = models.OneToOneField(User)

    auth = AuthManager()

    class Meta:
        abstract = True


class FaceBookOAuth(Auth):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    oauth_id = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)


class GoogleOAuth(Auth):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    oauth_id = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
