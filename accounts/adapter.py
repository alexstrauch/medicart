"""
Custom adapter for django-allauth to customize authentication behavior.
Extends the default adapter to provide custom messages and functionality.
"""

from allauth.account.adapter import DefaultAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Custom adapter class to override default allauth behavior.
    Provides customized messages for authentication events.
    """
    def get_login_success_message(self):
        """
        Override the default success message shown after login.
        Returns:
            str: Custom success message for user login
        """
        return "You successfully signed in!"
