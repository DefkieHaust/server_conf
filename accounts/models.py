from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager

# Create your models here.


class User(AbstractUser):
    insta = models.CharField(max_length=20, blank=True)
    is_verified = models.BooleanField(default=False)
    allow_crypto = models.BooleanField(default=False)
    allow_bank = models.BooleanField(default=False)
    allow_cash = models.BooleanField(default=False)
    local = models.BooleanField(default=False)
    objects = UserManager()


class Address(models.Model):
    user = models.ForeignKey(
                User,
                on_delete=models.CASCADE,
                related_name="addresses"
            )
    name = models.CharField(max_length=100)
    street = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    postcode = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user} > {self.name}"
