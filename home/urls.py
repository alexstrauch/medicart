from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('test-email/', views.test_email, name='test_email'),
]
