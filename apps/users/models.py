from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    is_verified_email = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['email'], name='unique_email_constraint')
        ]
