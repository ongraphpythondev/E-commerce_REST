from typing import DefaultDict
from django.db import models
from django.contrib.auth.models import AbstractUser

from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    mobile = models.IntegerField(_('phone no.'), unique=True)
    otp = models.CharField(max_length=4)
    is_verified = models.BooleanField(default=False)
    image = models.FileField(upload_to = 'account/static/account/image' , null=True)

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return str(self.mobile)