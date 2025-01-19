"""
Forms for the products app.
Defines forms for product management and review submission.
"""

from django import forms
from .models import Product, Category, Review


class ProductForm(forms.ModelForm):
    """
    Form for creating and editing products.
    Includes all fields from the Product model and
    uses friendly names for categories.
    """
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        """
        Initialize form with custom styling and
        populate category choices with friendly names.
        """
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'


class ReviewForm(forms.ModelForm):
    """
    Form for submitting product reviews.
    Includes rating (1-5) and review text fields.
    """
    class Meta:
        model = Review
        fields = ('rating', 'text',)
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize form with custom styling and
        set up rating input constraints.
        """
        super().__init__(*args, **kwargs)
        self.fields['rating'].widget = forms.NumberInput(attrs={
            'min': '1',
            'max': '5',
            'class': 'border-black rounded-0'
        })
        self.fields['text'].widget.attrs['class'] = 'border-black rounded-0'
