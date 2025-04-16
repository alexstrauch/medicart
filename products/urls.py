"""
URL configuration for the products app.

Defines URL patterns for product listing and detail views.
URL structure follows RESTful conventions where possible:
- List: /products/
- Detail: /products/<id>/
"""

from django.urls import path
from . import views

urlpatterns = [
    # Product listing page - shows all products with sorting and filtering
    path('', views.all_products, name='products'),
    
    # Product detail page - shows full information for a specific product
    path('<int:product_id>/', views.product_detail, name='product_detail'),
]
