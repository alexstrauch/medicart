"""Configuration for the contact app."""

from django.apps import AppConfig


class ContactConfig(AppConfig):
    """Configuration class for the contact app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'contact'
    verbose_name = 'Contact Management'
