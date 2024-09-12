from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Create_listing(models.Model):
    CATEGORY_CHOICES = [
        ('Fashion', 'Fashion'),
        ('Toys', 'Toys'),
        ('Electronics', 'Electronics'),
        ('Home', 'Home'),
    ]
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    bid = models.IntegerField()
    image_url = models.URLField(max_length=200, blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)


class bids():
    pass


class comments():
    pass