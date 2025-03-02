"""
URL configuration for the profiles app.

Defines URL patterns for user profile management, including:
- Profile viewing and editing
- Order history viewing
- Account deletion

All URLs in this app require user authentication.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Main profile page - view and edit profile information
    path('', views.profile, name='profile'),
    
    # Order history - view details of a specific order
    path('order_history/<order_number>', views.order_history, name='order_history'),
    
    # Account deletion - permanently remove user account
    path('delete-account/', views.delete_account, name='delete_account'),
]
