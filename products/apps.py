"""
Django app configuration for the products app.
Handles product management and related functionality.
"""

from django.apps import AppConfig


class ProductsConfig(AppConfig):
    """
    Configuration class for the products app.
    Uses BigAutoField for primary keys and sets app name.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'
