# Generated by Django 3.2.1 on 2022-01-04 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0004_auto_20220104_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='discounted_price',
            field=models.IntegerField(default=0),
        ),
    ]
