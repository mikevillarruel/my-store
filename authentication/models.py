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
