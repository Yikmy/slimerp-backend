from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from kernel.core.models import BaseModel

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    """
    Custom user model for identity system.
    Inherits from BaseModel to use UUID primary key.
    """
    username = models.CharField(max_length=150, unique=True, help_text="Unique username")
    email = models.EmailField(blank=True, null=True, help_text="Email address")
    is_staff = models.BooleanField(default=False, help_text="Designates whether the user can log into this admin site.")
    is_active = models.BooleanField(default=True, help_text="Designates whether this user should be treated as active.")
    
    # Audit fields already in BaseModel (created_at, updated_at, etc.)
    # Note: AbstractBaseUser defines password and last_login

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'sys_user'

    def __str__(self):
        return self.username
