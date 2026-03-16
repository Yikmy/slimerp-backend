# Generated manually for RBAC models

import django.core.validators
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company', '0002_basemodel_softdelete_and_user_fk'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, help_text='Creation time')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Last update time')),
                ('is_deleted', models.BooleanField(db_index=True, default=False, help_text='Soft delete flag')),
                ('code', models.CharField(help_text='Permission code: module.resource.action', max_length=120, unique=True, validators=[django.core.validators.RegexValidator(message='Permission code must use format: module.resource.action', regex='^[a-z][a-z0-9_]*\\.[a-z][a-z0-9_]*\\.[a-z][a-z0-9_]*$')])),
                ('description', models.CharField(blank=True, default='', help_text='Permission description', max_length=255)),
                ('created_by', models.ForeignKey(blank=True, help_text='Creator user', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_rbac_permission_set', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, help_text='Updater user', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_rbac_permission_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Permission',
                'verbose_name_plural': 'Permissions',
                'db_table': 'sys_permission',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, help_text='Creation time')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Last update time')),
                ('is_deleted', models.BooleanField(db_index=True, default=False, help_text='Soft delete flag')),
                ('name', models.CharField(help_text='Role unique name', max_length=100, unique=True)),
                ('description', models.CharField(blank=True, default='', help_text='Role description', max_length=255)),
                ('is_system', models.BooleanField(default=False, help_text='System role cannot be removed casually')),
                ('created_by', models.ForeignKey(blank=True, help_text='Creator user', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_rbac_role_set', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, help_text='Updater user', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_rbac_role_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Role',
                'verbose_name_plural': 'Roles',
                'db_table': 'sys_role',
            },
        ),
        migrations.CreateModel(
            name='RolePermission',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, help_text='Creation time')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Last update time')),
                ('is_deleted', models.BooleanField(db_index=True, default=False, help_text='Soft delete flag')),
                ('created_by', models.ForeignKey(blank=True, help_text='Creator user', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_rbac_rolepermission_set', to=settings.AUTH_USER_MODEL)),
                ('permission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='role_permissions', to='rbac.permission')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='role_permissions', to='rbac.role')),
                ('updated_by', models.ForeignKey(blank=True, help_text='Updater user', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_rbac_rolepermission_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Role Permission',
                'verbose_name_plural': 'Role Permissions',
                'db_table': 'sys_role_permission',
                'unique_together': {('role', 'permission')},
            },
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, help_text='Creation time')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Last update time')),
                ('is_deleted', models.BooleanField(db_index=True, default=False, help_text='Soft delete flag')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rbac_user_roles', to='company.company')),
                ('created_by', models.ForeignKey(blank=True, help_text='Creator user', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_rbac_userrole_set', to=settings.AUTH_USER_MODEL)),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_roles', to='rbac.role')),
                ('updated_by', models.ForeignKey(blank=True, help_text='Updater user', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_rbac_userrole_set', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rbac_user_roles', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Role',
                'verbose_name_plural': 'User Roles',
                'db_table': 'sys_user_role',
                'unique_together': {('user', 'company', 'role')},
            },
        ),
    ]
