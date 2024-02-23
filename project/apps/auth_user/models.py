from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    user_id = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    gender = models.CharField(max_length=10, choices=(('male', 'male'), ('female', 'female'), ('others', 'others')))
    address = models.TextField(blank=True)
    country = models.CharField(max_length=50, blank=True)
    bio = models.TextField(blank=True)
    role = models.CharField(max_length=20, choices=(('admin', 'admin'), ('user', 'user')))

    class Meta:
        verbose_name = "USER"
        verbose_name_plural = "USERS"

    def __str__(self):
        return f"{self.username}"
