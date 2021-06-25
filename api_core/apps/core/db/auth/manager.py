from django.db import models

from ...utils.error.exceptions import QueryActionNotAllowed


class NoDeleteQuerySet(models.query.QuerySet):

    def delete(self):
        raise QueryActionNotAllowed('delete action has been disabled in this model')


class AuthManager(models.Manager):
    def get_queryset(self):
        return NoDeleteQuerySet(self.model, using=self._db)




