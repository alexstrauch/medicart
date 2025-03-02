"""
Forms for user authentication and registration.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    """
    Form for user registration using email as the primary identifier.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email address'})
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'First name'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Last name'})
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.fields.get('username'):
            del self.fields['username']
        
        # Add placeholders and styling to form fields
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Email address'
        })
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'First name'
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Last name'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
        
        # Customize password help text
        self.fields['password1'].help_text = 'At least 8 characters. Must include letters and numbers.'
        self.fields['password2'].help_text = 'Enter the same password again for verification.'

    def clean_email(self):
        """
        Validate that the email is not already in use.
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'An account with this email address already exists.'
            )
        return email

    def try_save(self, request):
        """
        Save the user instance with email as username.
        Required by django-allauth.
        """
        try:
            user = super().save(commit=False)
            user.username = self.cleaned_data['email']  # Use email as username
            user.email = self.cleaned_data['email']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.save()
            return user, None  # Return tuple of (user, error) as expected by allauth
        except Exception as e:
            return None, str(e)  # Return error if something goes wrong
