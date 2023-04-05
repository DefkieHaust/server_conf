from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager

# Create your models here.


class User(AbstractUser):
    insta = models.CharField(max_length=20, blank=True)
    is_verified = models.BooleanField(default=False)
    objects = UserManager()
