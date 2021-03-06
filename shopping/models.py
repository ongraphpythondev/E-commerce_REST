from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.base import Model


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Product(models.Model):
    price = models.IntegerField()
    name = models.CharField(max_length=50)
    image = models.FileField(upload_to = 'shopping/static/shopping/image')
    specification = models.CharField(max_length=500)
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    discount = models.IntegerField(null=True)
    category = models.ForeignKey(Category, related_name="product", on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='products', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Feedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='feedback', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='feedback', on_delete=models.CASCADE)
    message = models.CharField(max_length=500 , null=True )
    rating = models.IntegerField(validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ])

    def __str__(self):
        return str(self.product)

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='cart', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.product)



class Bank(models.Model):
    bank = models.CharField(max_length=100 )
    discount = models.IntegerField(default=0 )


    def __str__(self):
        return str(self.bank)

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='order', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order', on_delete=models.CASCADE)
    bank = models.ForeignKey(Bank, related_name='order', on_delete=models.CASCADE , null=True)
    delivered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    emi = models.BooleanField(default=False)
    pay_on_delivery = models.BooleanField(default=False)
    discounted_price = models.IntegerField(default=0 )


    def __str__(self):
        return str(self.product)


