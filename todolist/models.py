from django.contrib.auth.models import BaseUserManager, AbstractUser

from django.db import models


class AccountManager(BaseUserManager):
    def create_user(self, email, username, password, **other_fields):
        if not email:
            raise ValueError('User must have an email!')
        if not username:
            raise ValueError('User must have an username!')

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            **other_fields,
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **other_fields)


class Account(AbstractUser):
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='date_joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last_login', auto_now=True)
    about = models.TextField(verbose_name='about', max_length=200, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = AccountManager()

    def __str__(self):
        return f'Username: {self.username}; Email: {self.email}'
