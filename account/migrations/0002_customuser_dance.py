# Generated by Django 3.2.1 on 2021-12-28 09:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='dance',
            field=models.FileField(default=django.utils.timezone.now, upload_to='account/static/account/image'),
            preserve_default=False,
        ),
    ]
