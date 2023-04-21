from django.db import models
from accounts.models import User

# Create your models here.


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
