"""
Django app configuration for user profiles.

This app handles user profile management, including:
- Storing default delivery information
- Managing user preferences
- Tracking order history
"""

from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    """
    Configuration class for the profiles app.

    This app manages user-specific data and preferences,
    providing a central place for users to manage their
    account information and view their order history.

    Attributes:
        default_auto_field (str): The default primary key field type
        name (str): The name of the app
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profiles'
