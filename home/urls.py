"""
URL configuration for the home app.
Defines the routing for homepage and email testing endpoints.
"""

from django.urls import path
from . import views


urlpatterns = [
    # Homepage URL pattern
    path('', views.index, name='home'),
    # Email testing endpoint
    path('test-email/', views.test_email, name='test_email'),
]
