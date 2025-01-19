"""
Configuration for the cart app.
Handles app initialization and template tag registration.
"""

from django.apps import AppConfig


class CartConfig(AppConfig):
    """
    Configuration class for the cart app.
    Handles app initialization and ensures template tags are loaded.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cart'
    
    def ready(self):
        """
        Method called when the app is ready.
        Attempts to import cart template tags to ensure they're registered.
        Silently passes if import fails to avoid startup issues.
        """
        try:
            import cart.templatetags.cart_tools  # noqa
        except ImportError:
            pass
