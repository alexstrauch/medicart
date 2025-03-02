"""Forms for the contact app.

This module defines forms for creating and managing contact requests.
"""

from django import forms
from .models import ContactRequest


class ContactForm(forms.ModelForm):
    """
    Form for creating contact requests.

    Includes custom styling and widgets for a better user experience.
    Auto-fills user information for logged-in users.
    """

    class Meta:
        model = ContactRequest
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'message': forms.Textarea(
                attrs={
                    'rows': 6,
                    'class': 'form-control',
                    'placeholder': 'How can we help you?'
                }
            ),
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Your name'
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'your.email@example.com'
                }
            ),
            'subject': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
        }
        labels = {
            'name': 'Your name',
            'email': 'Email address',
            'subject': 'What is this about?',
            'message': 'Your message',
        }
