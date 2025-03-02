"""
URL configuration for the products app.

Defines URL patterns for product listing, detail views, and management operations.
URL structure follows RESTful conventions where possible:
- List/Create: /products/
- Detail: /products/<id>/
- Edit: /products/edit/<id>/
- Delete: /products/delete/<id>/
"""

from django.urls import path
from . import views

urlpatterns = [
    # Product listing page - shows all products with sorting and filtering
    path('', views.all_products, name='products'),
    
    # Product detail page - shows full information for a specific product
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    
    # Product management URLs (staff/admin only)
    path('add/', views.add_product, name='add_product'),              # Add new product
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),    # Edit existing product
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),  # Delete product
]
