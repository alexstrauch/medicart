"""
URL configuration for the wishlist app.

This module defines the URL patterns for wishlist-related views, including:
- Viewing the wishlist
- Adding/removing items from the wishlist

All URLs are prefixed with 'wishlist/' as defined in the project's main urls.py
"""

from django.urls import path
from . import views

app_name = 'wishlist'

urlpatterns = [
    path('', views.view_wishlist, name='view_wishlist'),
    path('toggle/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),
]
