# Generated by Django 3.0.8 on 2020-08-01 16:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0018_auto_20200801_1543'),
    ]

    operations = [
        migrations.RenameField(
            model_name='winner',
            old_name='winning_bid',
            new_name='amount',
        ),
        migrations.RenameField(
            model_name='winner',
            old_name='title',
            new_name='item',
        ),
        migrations.RenameField(
            model_name='winner',
            old_name='winner',
            new_name='victor',
        ),
    ]