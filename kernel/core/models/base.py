import uuid
from django.db import models
from django.utils import timezone

class BaseModel(models.Model):
    """
    Abstract base model for all business models.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, help_text="Creation time")
    updated_at = models.DateTimeField(auto_now=True, help_text="Last update time")
    
    # Optional audit fields - nullable for now as user system might not be fully ready
    created_by = models.UUIDField(null=True, blank=True, help_text="Creator user ID")
    updated_by = models.UUIDField(null=True, blank=True, help_text="Updater user ID")
    
    # Optional soft delete
    is_deleted = models.BooleanField(default=False, help_text="Soft delete flag")

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def __str__(self):
        return str(self.id)
