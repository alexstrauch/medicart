"""
Django application configuration for the home app.
Handles app-specific configuration and initialization.
"""

from django.apps import AppConfig


class HomeConfig(AppConfig):
    """
    Configuration class for the home app.
    
    Attributes:
        default_auto_field (str): The default primary key field type
        name (str): The name of the application
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'
