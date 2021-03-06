# Generated by Django 3.2.1 on 2021-12-29 06:37

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_remove_customuser_dance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='otp',
        ),
        migrations.AddField(
            model_name='customuser',
            name='username',
            field=models.CharField(default=False, error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='image',
            field=models.FileField(null=True, upload_to='account/static/account/image'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
