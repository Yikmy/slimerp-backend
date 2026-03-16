from django.db import models
from django.utils.translation import gettext_lazy as _
from kernel.core.models.base import BaseModel


class LoginLog(BaseModel):
    """
    Login log model for recording login attempts.
    """
    
    STATUS_SUCCESS = 'SUCCESS'
    STATUS_FAILURE = 'FAILURE'
    
    STATUS_CHOICES = (
        (STATUS_SUCCESS, _('Success')),
        (STATUS_FAILURE, _('Failure')),
    )

    user = models.ForeignKey(
        'identity.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='login_logs',
        help_text=_("The user attempting to log in")
    )
    
    username = models.CharField(
        max_length=150,
        help_text=_("The username used for the login attempt")
    )
    
    company = models.ForeignKey(
        'company.Company',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='login_logs',
        help_text=_("The company context for this login")
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_SUCCESS,
        help_text=_("The status of the login attempt")
    )
    
    failure_reason = models.TextField(
        null=True,
        blank=True,
        help_text=_("The reason for login failure")
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
    
    details = models.JSONField(
        default=dict,
        blank=True,
        help_text=_("Additional details")
    )

    class Meta:
        verbose_name = _("Login Log")
        verbose_name_plural = _("Login Logs")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.username} {self.status} ({self.created_at})"
