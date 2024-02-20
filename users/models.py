from django.db import models
from django.contrib.auth.models import AbstractUser

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)
    is_active = models.BooleanField(default=False, verbose_name='Активность')
    verification_token = models.CharField(max_length=31, **NULLABLE)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
