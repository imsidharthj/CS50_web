from django import forms
from .models import Create_listing


class CreateListingForm(forms.ModelForm):
    class Meta:
        model = Create_listing
        fields = ['title', 'description', 'bid', 'image_url', 'category']

        labels = {
            'title': 'Listing Title',
            'description' : 'Description',
            'bid' : 'Bid',
            'image_url': 'Image URL',
            'category': 'Category'
        }
