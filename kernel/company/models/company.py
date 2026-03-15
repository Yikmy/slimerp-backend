from django.db import models
from django.conf import settings
from kernel.core.models import BaseModel

class Company(BaseModel):
    """
    Company model representing the tenant/organization scope.
    """
    name = models.CharField(max_length=255, unique=True, help_text="Company name")
    code = models.CharField(max_length=50, unique=True, help_text="Company code/identifier")
    
    # Optional metadata
    tax_id = models.CharField(max_length=50, blank=True, null=True, help_text="Tax Identification Number")
    currency = models.CharField(max_length=3, default='USD', help_text="Default currency (ISO 4217)")
    
    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        db_table = "sys_company"

    def __str__(self):
        return f"{self.name} ({self.code})"

class UserCompanyAccess(BaseModel):
    """
    Relation table for User <-> Company many-to-many.
    Defines which companies a user can access.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='company_accesses',
        help_text="User who has access"
    )
    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE, 
        related_name='user_accesses',
        help_text="Company the user can access"
    )
    
    # Optional role/level in this company context? 
    # For now, RBAC handles roles. This just defines scope visibility.
    is_default = models.BooleanField(default=False, help_text="Is this the default company for the user?")

    class Meta:
        unique_together = ('user', 'company')
        verbose_name = "User Company Access"
        verbose_name_plural = "User Company Accesses"
        db_table = "sys_user_company_access"

    def __str__(self):
        return f"{self.user} -> {self.company}"
