# Generated by Django 3.0.8 on 2020-07-28 10:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_auto_20200728_0708'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='image',
        ),
    ]