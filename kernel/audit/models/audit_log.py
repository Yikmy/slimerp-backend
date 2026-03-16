from django.db import models
from django.utils.translation import gettext_lazy as _
from kernel.core.models.base import BaseModel


class AuditLog(BaseModel):
    """
    Audit log model for recording business actions.
    Records who did what, when, where, and the result.
    """
    
    ACTION_CREATE = 'CREATE'
    ACTION_UPDATE = 'UPDATE'
    ACTION_DELETE = 'DELETE'
    ACTION_OTHER = 'OTHER'
    
    ACTION_CHOICES = (
        (ACTION_CREATE, _('Create')),
        (ACTION_UPDATE, _('Update')),
        (ACTION_DELETE, _('Delete')),
        (ACTION_OTHER, _('Other')),
    )
    
    RESULT_SUCCESS = 'SUCCESS'
    RESULT_FAILURE = 'FAILURE'
    
    RESULT_CHOICES = (
        (RESULT_SUCCESS, _('Success')),
        (RESULT_FAILURE, _('Failure')),
    )

    company = models.ForeignKey(
        'company.Company',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs',
        help_text=_("The company context for this action")
    )
    
    target_model = models.CharField(
        max_length=100,
        help_text=_("The model name of the target object")
    )
    
    target_object_id = models.CharField(
        max_length=50,
        help_text=_("The ID of the target object")
    )
    
    action = models.CharField(
        max_length=50,
        choices=ACTION_CHOICES,
        default=ACTION_OTHER,
        help_text=_("The type of action performed")
    )
    
    details = models.JSONField(
        default=dict,
        blank=True,
        help_text=_("Detailed changes or payload")
    )
    
    result = models.CharField(
        max_length=20,
        choices=RESULT_CHOICES,
        default=RESULT_SUCCESS,
        help_text=_("The result of the action")
    )
    
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        help_text=_("IP address of the requester")
    )
    
    user_agent = models.TextField(
        null=True,
        blank=True,
        help_text=_("User agent string")
    )
    
    request_id = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text=_("Unique request ID for tracing")
    )

    class Meta:
        verbose_name = _("Audit Log")
        verbose_name_plural = _("Audit Logs")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['target_model', 'target_object_id']),
            models.Index(fields=['action']),
            models.Index(fields=['created_at']),
            models.Index(fields=['created_by']),
        ]

    def __str__(self):
        return f"{self.created_by} {self.action} {self.target_model}:{self.target_object_id} ({self.result})"
