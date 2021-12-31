from django.db import models
from django.contrib.auth.models import AbstractUser

from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    mobile = models.IntegerField(_('phone no.'), unique=True)
    username = models.CharField(max_length=30)
    is_verified = models.BooleanField(default=False)
    image = models.FileField(upload_to = 'account/static/account/image' , null=True)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return str(self.mobile)

class Otp(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='otp',on_delete=models.CASCADE)
    otp = models.CharField(max_length=4)

    def __str__(self):
        return str(self.user)