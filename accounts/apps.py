"""
Configuration for the accounts app.
Defines app-specific settings and configurations.
"""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    Configuration class for the accounts app.
    Specifies the default auto field type and app name.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
