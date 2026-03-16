from django.db import models
from django.core.exceptions import ValidationError
from kernel.core.models import BaseModel
from kernel.company.models import Company

class ConfigScope(models.TextChoices):
    GLOBAL = 'global', 'Global'
    COMPANY = 'company', 'Company'
    MODULE = 'module', 'Module'

class SystemConfig(BaseModel):
    """
    Model for storing system configurations (key-value pairs)
    based on scopes (global, company, module).
    """
    key = models.CharField(max_length=255, db_index=True)
    value = models.JSONField(help_text="Typed config value stored as JSON")
    scope = models.CharField(
        max_length=20, 
        choices=ConfigScope.choices, 
        default=ConfigScope.GLOBAL,
        db_index=True
    )
    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name="configs",
        help_text="Required if scope is company"
    )
    module = models.CharField(
        max_length=100, 
        null=True, 
        blank=True,
        help_text="Required if scope is module"
    )
    description = models.CharField(max_length=500, blank=True)

    class Meta:
        db_table = "sys_system_config"
        verbose_name = "System Config"
        verbose_name_plural = "System Configs"
        unique_together = ('key', 'scope', 'company', 'module')

    def clean(self):
        super().clean()
        if self.scope == ConfigScope.COMPANY and not self.company:
            raise ValidationError("Company is required when scope is 'company'")
        if self.scope == ConfigScope.MODULE and not self.module:
            raise ValidationError("Module is required when scope is 'module'")
        
        # Ensure company is null if not company scope (strict separation)
        if self.scope != ConfigScope.COMPANY and self.company:
            self.company = None
        # Ensure module is null if not module scope
        if self.scope != ConfigScope.MODULE and self.module:
            self.module = None

    def __str__(self):
        return f"{self.key} ({self.scope})"


class ModuleSwitch(BaseModel):
    """
    Model for module enable/disable switches.
    Can be configured globally or per company.
    """
    module_name = models.CharField(max_length=100, db_index=True)
    is_enabled = models.BooleanField(default=True)
    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name="module_switches",
        help_text="If null, represents a global switch. If set, represents a company-specific override."
    )
    
    class Meta:
        db_table = "sys_module_switch"
        verbose_name = "Module Switch"
        verbose_name_plural = "Module Switches"
        unique_together = ('module_name', 'company')

    def __str__(self):
        scope_str = self.company.name if self.company else "Global"
        status = "Enabled" if self.is_enabled else "Disabled"
        return f"{self.module_name} - {scope_str}: {status}"
