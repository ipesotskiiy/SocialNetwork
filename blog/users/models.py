from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from users.managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='Your email', max_length=40, db_index=True, unique=True)
    password = models.CharField(verbose_name='Your password', max_length=255)
    username = None
    information = models.TextField(verbose_name='Information about yourself', max_length=1000, null=True, blank=True)
    count_article = models.PositiveIntegerField(verbose_name='Count articles', null=True, blank=True)
    avatar = models.FileField(
        upload_to='',
        verbose_name='Your avatar',
        max_length=250,
        null=True,
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    object = CustomUserManager()

