# Generated by Django 5.0.7 on 2024-09-12 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_create_listing'),
    ]

    operations = [
        migrations.AddField(
            model_name='create_listing',
            name='category',
            field=models.CharField(default='Miscellaneous', max_length=20),
        ),
    ]
