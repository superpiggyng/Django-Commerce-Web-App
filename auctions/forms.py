from django import forms
from .models import AuctionListing, Comment

class ListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['title', 'model_name', 'brand', 'image', 'price', 'product_category']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 1, 'cols': 40})
        }