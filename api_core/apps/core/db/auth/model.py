import re
import uuid

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .manager import AuthManager
from ..user.model import User
from ...utils.error.exceptions import QueryActionNotAllowed


def cw2us(x): # capwords to underscore notation
    return re.sub(r'(?<=[a-z])[A-Z]|(?<!^)[A-Z](?=[a-z])',r"_\g<0>", x).lower()


class Auth(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    oauth_id = models.CharField(max_length=255, unique=True)

    # user = models.OneToOneField(
    #     User, on_delete=models.CASCADE,
    #     related_name=cw2us('%(class)s'), null=True, blank=True,
    #     editable=False,
    # )

    service = AuthManager()

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        raise QueryActionNotAllowed('delete action has been disabled in this model')


class FaceBookAuth(Auth):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        related_name='facebook_auth', null=True, blank=True,
        editable=False,
    )

    class Meta:
        db_table = 'facebook_auths'
        verbose_name = 'facebook_auth'
        verbose_name_plural = 'facebook_auths'

    def __str__(self):
        return f'FaceBookAuth=[{self.id if self.id else "DELETED"}]'


class GoogleAuth(Auth):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        related_name='google_auth', null=True, blank=True,
        editable=False,
    )

    class Meta:
        db_table = 'google_auths'
        verbose_name = 'google_auth'
        verbose_name_plural = 'google_auths'

    def __str__(self):
        return f'GoogleAuth=[{self.id if self.id else "DELETED"}]'


@receiver(pre_save, sender=FaceBookAuth)
def does_not_allow_to_update(sender, instance: FaceBookAuth, **kwargs):
    # oauth record has been created & associated with user
    if FaceBookAuth.service.filter(oauth_id=instance.oauth_id, user_id__isnull=False).exists():
        raise QueryActionNotAllowed('FaceBookAuth\'s user_id does not allow to update')


@receiver(pre_save, sender=GoogleAuth)
def does_not_allow_to_update(sender, instance: GoogleAuth, **kwargs):
    # oauth record has been created & associated with user
    if GoogleAuth.service.filter(oauth_id=instance.oauth_id, user_id__isnull=False).exists():
        raise QueryActionNotAllowed('GoogleAuth\'s user_id does not allow to update')
