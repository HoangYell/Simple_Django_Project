from django.db import models
from django.db.models import Manager
from django.db.models.query import QuerySet
from django.utils import timezone


class SoftDeleteQuerySet(QuerySet):
    def delete(self):
        now = timezone.now()
        obj = None
        for obj in self:
            obj.is_deleted = True
            obj.deleted_at = now
        if obj:
            obj.__class__.objects.bulk_update(self, ["is_deleted", "deleted_at"])

    def hard_delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)


class SoftDeleteManager(Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(is_deleted=False)

    def include_deleted(self):
        return SoftDeleteQuerySet(self.model, using=self._db)


class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False, db_index=True)
    deleted_at = models.DateTimeField(default=None, null=True)

    class Meta:
        abstract = True

    def delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    objects = SoftDeleteManager()
