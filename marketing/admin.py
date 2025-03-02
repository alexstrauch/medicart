"""
Admin configuration for the marketing app.
Defines how newsletter subscribers are displayed and managed in the admin interface.
"""

from django.contrib import admin
from .models import NewsletterSubscriber


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    """
    Admin configuration for NewsletterSubscriber model.
    
    Customizes how newsletter subscribers are displayed and managed
    in the Django admin interface.
    
    Attributes:
        list_display: Fields to display in the list view
        list_filter: Fields available for filtering
        search_fields: Fields available for searching
        date_hierarchy: Field to use for date-based drilldown
        ordering: Default ordering of records
    """
    list_display = ('email', 'date_subscribed', 'is_active')
    list_filter = ('is_active', 'date_subscribed')
    search_fields = ('email',)
    date_hierarchy = 'date_subscribed'
    ordering = ('-date_subscribed',)
