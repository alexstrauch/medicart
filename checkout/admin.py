"""
Admin configuration for the checkout app.
Defines how Order and OrderLineItem models are displayed and managed in the admin interface.
Includes custom display configurations and filtering options.
"""

from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    """
    Inline admin configuration for OrderLineItem model.
    Allows editing of order line items directly in the Order admin interface.
    """
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin configuration for Order model.
    
    Configures:
    - Inline editing of order line items
    - Read-only fields for order details
    - Field ordering and grouping
    - List display columns
    - Filtering options
    - Default ordering
    """
    inlines = (OrderLineItemAdminInline,)
    
    readonly_fields = ('order_number', 'date',
                     'delivery_cost', 'order_total',
                     'grand_total', 'original_cart',
                     'stripe_pid')

    fields = ('order_number', 'user_profile', 'date', 'full_name',
              'email', 'phone_number', 'country',
              'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'county', 'delivery_cost',
              'order_total', 'grand_total', 'original_cart',
              'stripe_pid', 'status', 'payment_verified',
              'stock_verified', 'notes')

    list_display = ('order_number', 'date', 'full_name',
                   'order_total', 'delivery_cost',
                   'grand_total', 'status',
                   'payment_verified', 'stock_verified')
    
    list_filter = ('status', 'payment_verified', 'stock_verified')
    
    ordering = ('-date',)
