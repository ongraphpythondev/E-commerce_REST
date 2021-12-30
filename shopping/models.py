from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator


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


