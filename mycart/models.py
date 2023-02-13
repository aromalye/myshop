from email.policy import default
from django.db import models
from account.models import User
from store.models import Product

# Create your models here.


class MyCart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.cart_id


class MyFav(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=100, blank=True)

class MyCartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(MyCart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    discount = models.IntegerField(null=True, blank=True)
    size = models.CharField(max_length=100, null=True)
    color = models.CharField(max_length=100, null=True)


    def sub_total(self):
        return self.product.price * self.quantity


class Coupons(models.Model):
    code = models.CharField(max_length=20)

    def __str__(self):
        return self.code
    
    def discount(self):
        x = self.split('@')
        return x[1]