"""
Django app configuration for the wishlist functionality.

This module configures the wishlist app, which allows users to:
- Save products they're interested in
- View their saved items
- Easily access their wishlist from any page
"""

from django.apps import AppConfig


class WishlistConfig(AppConfig):
    """
    Configuration class for the wishlist app.

    Defines basic app settings including:
    - Database field type
    - App name
    - Human-readable app name for admin interface
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wishlist'
    verbose_name = 'Product Wishlist'