from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass



class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Create_listing(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    bid = models.IntegerField()
    image_url = models.URLField(max_length=200, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, related_name="category")

    def __str__(self):
        return self.title


class bids():
    pass


class comments():
    pass

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Create_listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s watchlist: {self.listing.title}"
