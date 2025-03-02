"""
Configuration for the checkout app.
Handles app configuration and settings for the checkout process.
"""

from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    """
    Configuration class for the checkout app.
    Defines app name and default auto field type.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'checkout'
