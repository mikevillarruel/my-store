from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=64)
    SKU = models.CharField(max_length=128)
    UPC = models.CharField(max_length=12)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.IntegerField()
    created_at = models.TimeField(auto_now_add=True)
    modified_at = models.TimeField(auto_now=True)
    deleted_at = models.TimeField()


class Order(models.Model):
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.TimeField(auto_now_add=True)
    modified_at = models.TimeField(auto_now=True)
    deleted_at = models.TimeField()


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    discount = models.IntegerField()
