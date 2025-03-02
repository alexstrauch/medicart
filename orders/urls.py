"""
URL configuration for the orders app.

This module defines the URL patterns for viewing order history.
It provides a simple URL structure where the root path displays
all orders for the authenticated user.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Root path displays order history
    path('', views.orders, name='orders'),
]
