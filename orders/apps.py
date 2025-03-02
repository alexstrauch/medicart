"""
Django app configuration for the orders functionality.

This module contains the configuration class for the orders app,
which is responsible for displaying and managing completed orders.
"""

from django.apps import AppConfig


class OrdersConfig(AppConfig):
    """
    Configuration for the orders app.
    
    This app handles the display and management of completed orders.
    It provides views for users to see their order history and track
    their past purchases. The app is intentionally separate from the
    checkout app to maintain a clear separation of concerns:
    - Checkout app: Handles the process of creating new orders
    - Orders app: Handles viewing and managing existing orders
    
    Attributes:
        default_auto_field (str): The default primary key field type
        name (str): The name of the app
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'
