from django.core import validators

from django.utils.deconstruct import deconstructible


@deconstructible
class PasswordValidator(validators.RegexValidator):
    regex = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'
    message = "Password must contain at least 8 characters, one letter and one digit."
