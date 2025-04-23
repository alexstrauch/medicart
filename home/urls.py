"""
URL configuration for the home app.
Defines the routing for homepage.
"""

from django.urls import path
from . import views


urlpatterns = [
    # Homepage URL patterns
    path('', views.index, name='home'),  # Root URL
    path('home/', views.index, name='home_alt'),  # /home/ URL
    path('index.html', views.index, name='home_html'),  # /index.html URL
]
