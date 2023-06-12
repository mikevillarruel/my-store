import os

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import PasswordValidator


# Create your models here.
class User(AbstractUser):
    password_validator = PasswordValidator()

    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': 'A user with that email already exists.',
        }
    )
    password = models.CharField(
        max_length=128,
        validators=[password_validator],
    )
    picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.pk:
            old_picture = User.objects.get(pk=self.pk).picture
            if old_picture and old_picture != self.picture:
                try:
                    os.remove(os.path.join(settings.MEDIA_ROOT, old_picture.path))
                except FileNotFoundError:
                    pass
        super().save(*args, **kwargs)
