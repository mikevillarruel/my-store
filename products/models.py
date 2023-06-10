import os

from django.conf import settings
from django.db import models

from authentication.models import User


# Create your models here.
class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    description = models.TextField()
    size = models.CharField(max_length=16)
    brand = models.CharField(max_length=64, null=True, blank=True)
    composition = models.CharField(max_length=256, null=True, blank=True)
    stock = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    path = models.ImageField(upload_to='images/')

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        image_path = os.path.join(settings.MEDIA_ROOT, self.path.name)
        try:
            os.remove(image_path)
        except FileNotFoundError:
            pass
