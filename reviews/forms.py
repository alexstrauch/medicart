from django import forms
from .models import ProductReview


class ProductReviewForm(forms.ModelForm):
    """
    Form for creating and editing product reviews.
    
    Includes:
    - Rating selection (1-5 stars)
    - Review text
    - Custom styling and widgets
    """
    class Meta:
        model = ProductReview
        fields = ['rating', 'review_text']
        widgets = {
            'review_text': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Write your review here...',
                'class': 'form-control',
            }),
            'rating': forms.Select(attrs={
                'class': 'form-control',
            }),
        }
        labels = {
            'review_text': 'Your review',
            'rating': 'Rating',
        }
