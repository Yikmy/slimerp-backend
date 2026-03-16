from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models

from kernel.company.models import Company
from kernel.core.models import BaseModel


permission_code_validator = RegexValidator(
    regex=r'^[a-z][a-z0-9_]*\.[a-z][a-z0-9_]*\.[a-z][a-z0-9_]*$',
    message='Permission code must use format: module.resource.action',
)


class Role(BaseModel):
    """RBAC role definition."""

    name = models.CharField(max_length=100, unique=True, help_text='Role unique name')
    description = models.CharField(max_length=255, blank=True, default='', help_text='Role description')
    is_system = models.BooleanField(default=False, help_text='System role cannot be removed casually')

    class Meta:
        db_table = 'sys_role'
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.name


class Permission(BaseModel):
    """Permission code model, format: module.resource.action."""

    code = models.CharField(
        max_length=120,
        unique=True,
        validators=[permission_code_validator],
        help_text='Permission code: module.resource.action',
    )
    description = models.CharField(max_length=255, blank=True, default='', help_text='Permission description')

    class Meta:
        db_table = 'sys_permission'
        verbose_name = 'Permission'
        verbose_name_plural = 'Permissions'

    def __str__(self):
        return self.code


class RolePermission(BaseModel):
    """Role to permission mapping."""

    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_permissions')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name='role_permissions')

    class Meta:
        db_table = 'sys_role_permission'
        verbose_name = 'Role Permission'
        verbose_name_plural = 'Role Permissions'
        unique_together = ('role', 'permission')

    def __str__(self):
        return f'{self.role.name} -> {self.permission.code}'


class UserRole(BaseModel):
    """User role assignment in company scope."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rbac_user_roles')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='rbac_user_roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_roles')

    class Meta:
        db_table = 'sys_user_role'
        verbose_name = 'User Role'
        verbose_name_plural = 'User Roles'
        unique_together = ('user', 'company', 'role')

    def __str__(self):
        return f'{self.user} @ {self.company.code}: {self.role.name}'
