"""
URL configuration for the home app.
Defines the routing for homepage.
"""

from django.urls import path
from . import views


urlpatterns = [
    # Homepage URL pattern
    path('', views.index, name='home'),
]
