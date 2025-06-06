"""
URL configuration for the reviews app.

This module defines the URL patterns for review-related views, including:
- Adding/editing reviews
- Deleting reviews
"""

from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('add/<int:product_id>/', views.add_review, name='add_review'),
    path('delete/<int:review_id>/', views.delete_review, name='delete_review'),
]
