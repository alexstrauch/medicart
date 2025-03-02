"""
URL configuration for the marketing app.
Defines URL patterns for newsletter subscription functionality.
"""

from django.urls import path
from . import views

app_name = 'marketing'

urlpatterns = [
    # Newsletter signup endpoint - handles both AJAX and form submissions
    path('newsletter/signup/', views.newsletter_signup, name='newsletter_signup'),
]
