from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from users.managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='User email', max_length=50, db_index=True, unique=True)
    password = models.CharField(verbose_name='User password', max_length=255)
    username = None
    login = models.CharField(verbose_name='User login', unique=True, max_length=30)
    bio = models.TextField(verbose_name='Information about user', max_length=2000, null=True, blank=True)
    count_article = models.PositiveIntegerField(verbose_name='Count articles', default=0, null=True, blank=True)
    avatar = models.FileField(
        upload_to='',
        verbose_name='User avatar',
        max_length=250,
        null=True,
        blank=True
    )
    country = models.CharField(max_length=40, null=True, blank=True)
    city = models.CharField(max_length=40, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = CustomUserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email


class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriber')
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'subscriber'], name='unique_followers')
        ]

    def __str__(self):
        return f'{self.subscriber } подписан на {self.user}'

