import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone


class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        return super().update(is_deleted=True, updated_at=timezone.now())

    def hard_delete(self):
        return super().delete()

    def restore(self):
        return super().update(is_deleted=False, updated_at=timezone.now())


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(is_deleted=False)


class BaseModel(models.Model):
    """
    Abstract base model for all business models.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, help_text="Creation time")
    updated_at = models.DateTimeField(auto_now=True, help_text="Last update time")

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='created_%(app_label)s_%(class)s_set',
        help_text="Creator user",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='updated_%(app_label)s_%(class)s_set',
        help_text="Updater user",
    )

    is_deleted = models.BooleanField(default=False, db_index=True, help_text="Soft delete flag")

    objects = SoftDeleteManager()
    all_objects = SoftDeleteQuerySet.as_manager()

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def delete(self, using=None, keep_parents=False):
        if self.is_deleted:
            return
        self.is_deleted = True
        self.updated_at = timezone.now()
        self.save(update_fields=['is_deleted', 'updated_at'], using=using)

    def hard_delete(self, using=None, keep_parents=False):
        return super().delete(using=using, keep_parents=keep_parents)

    def restore(self, using=None):
        if not self.is_deleted:
            return
        self.is_deleted = False
        self.updated_at = timezone.now()
        self.save(update_fields=['is_deleted', 'updated_at'], using=using)

    def __str__(self):
        return str(self.id)
