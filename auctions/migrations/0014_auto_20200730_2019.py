# Generated by Django 3.0.8 on 2020-07-30 20:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_comment_date_posted'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='listing_id',
            new_name='listing',
        ),
    ]