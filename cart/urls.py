"""
URL configuration for the cart app.
Defines URL patterns for cart-related views including viewing,
adding, adjusting, and removing items from the cart.
"""

from django.urls import path
from . import views

urlpatterns = [
    # View shopping cart contents
    path('', views.view_cart, name='view_cart'),
    # Add item to cart with specified product_id
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    # Adjust quantity of item in cart
    path('adjust/<int:product_id>/', views.adjust_cart, name='adjust_cart'),
    # Remove item from cart
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
]
