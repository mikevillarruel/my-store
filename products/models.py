from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    size = models.CharField(max_length=16)
    color = models.CharField(max_length=16)
    brand = models.CharField(max_length=64)
    material = models.CharField(max_length=64, null=True)
    stock = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)


class Image(models.Model):
    path = models.ImageField(upload_to='images/')


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)


class Order(models.Model):
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    discount = models.IntegerField(null=True)
