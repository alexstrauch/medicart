"""
Models for the marketing app.
Defines database models for managing newsletter subscriptions.
"""

from django.db import models


class NewsletterSubscriber(models.Model):
    """
    Model representing a newsletter subscriber.
    
    Stores email addresses of users who have subscribed to the newsletter,
    along with their subscription date and current status.
    
    Attributes:
        email (EmailField): Subscriber's email address (unique)
        date_subscribed (DateTimeField): Date and time of subscription
        is_active (BooleanField): Whether the subscription is currently active
    """
    email = models.EmailField(unique=True)
    date_subscribed = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        """Return string representation of the subscriber."""
        return self.email

    class Meta:
        verbose_name = 'Newsletter Subscriber'
        verbose_name_plural = 'Newsletter Subscribers'
