"""
Django application configuration for the marketing app.
Handles app-specific settings and initialization.
"""

from django.apps import AppConfig


class MarketingConfig(AppConfig):
    """
    Configuration class for the marketing app.
    
    Handles app initialization and configuration settings.
    Manages newsletter subscription and Mailchimp integration functionality.
    
    Attributes:
        default_auto_field (str): Default primary key field type for models
        name (str): Name of the Django application
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'marketing'
