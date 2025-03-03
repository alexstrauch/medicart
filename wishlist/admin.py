"""
Admin configuration for the wishlist app.

This module configures how wishlist models are displayed and managed in the Django admin interface.
It provides a customized interface for staff to view and manage user wishlists.
"""

from django.contrib import admin
from .models import Wishlist


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Wishlist model.

    Customizes how wishlists are displayed and managed in the Django admin:
    - Shows user, product, and date added in list view
    - Allows filtering by date
    - Enables searching by username and product name
    - Orders items by most recently added first
    """
    list_display = ('user', 'product', 'date_added')
    list_filter = ('date_added',)
    search_fields = ('user__username', 'product__name')
    ordering = ('-date_added',)
