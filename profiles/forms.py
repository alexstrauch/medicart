"""
Forms for the profiles app.

This module provides forms for managing user profiles, including
both the UserProfile model fields and User model fields (first/last name).
The forms include styling and placeholder text for better UX.
"""

from django import forms
from .models import UserProfile
from django.contrib.auth.models import User


class UserProfileForm(forms.ModelForm):
    """
    Form for managing user profile information.

    This form combines:
    1. User model fields (first_name, last_name)
    2. UserProfile model fields (delivery information)

    The form includes custom styling and placeholders for all fields,
    and handles the complexity of updating both User and UserProfile
    models in a single form.
    """
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = UserProfile
        fields = [
            'first_name',
            'last_name',
            'default_phone_number',
            'default_street_address1',
            'default_street_address2',
            'default_town_or_city',
            'default_county',
            'default_postcode',
            'default_country',
        ]

    def __init__(self, *args, **kwargs):
        """
        Initialize the UserProfileForm.

        Customizes form appearance and behavior by:
        1. Adding placeholders for all fields
        2. Setting autofocus on first name field
        3. Adding custom styling classes
        4. Marking required fields with asterisk

        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'default_phone_number': 'Phone Number',
            'default_street_address1': 'Street Address',
            'default_street_address2': 'House Number',
            'default_town_or_city': 'Town or City',
            'default_county': 'County, State or Locality',
            'default_postcode': 'Postal Code',
        }

        # Set autofocus on first name field
        self.fields['first_name'].widget.attrs['autofocus'] = True
        
        # Custom styling for country field
        self.fields['default_country'].widget.attrs['class'] = 'border-black rounded-0 profile-form-input'
        self.fields['default_country'].label = 'Country'

        # Add placeholders and styling to all fields except country
        for field in self.fields:
            if field != 'default_country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
                self.fields[field].label = False
            self.fields[field].widget.attrs['class'] = 'border-black rounded-0 profile-form-input'

        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
            # Update User model fields
            user = profile.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.save()
        return profile
