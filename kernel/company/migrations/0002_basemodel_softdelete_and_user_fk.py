import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True, help_text='Creation time'),
        ),
        migrations.AlterField(
            model_name='company',
            name='created_by',
            field=models.ForeignKey(blank=True, help_text='Creator user', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_%(app_label)s_%(class)s_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='company',
            name='is_deleted',
            field=models.BooleanField(db_index=True, default=False, help_text='Soft delete flag'),
        ),
        migrations.AlterField(
            model_name='company',
            name='updated_by',
            field=models.ForeignKey(blank=True, help_text='Updater user', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_%(app_label)s_%(class)s_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='usercompanyaccess',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True, help_text='Creation time'),
        ),
        migrations.AlterField(
            model_name='usercompanyaccess',
            name='created_by',
            field=models.ForeignKey(blank=True, help_text='Creator user', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_%(app_label)s_%(class)s_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='usercompanyaccess',
            name='is_deleted',
            field=models.BooleanField(db_index=True, default=False, help_text='Soft delete flag'),
        ),
        migrations.AlterField(
            model_name='usercompanyaccess',
            name='updated_by',
            field=models.ForeignKey(blank=True, help_text='Updater user', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_%(app_label)s_%(class)s_set', to=settings.AUTH_USER_MODEL),
        ),
    ]
