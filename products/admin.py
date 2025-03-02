"""
Admin configuration for the products app.
Customizes the admin interface for Category and Product models.
"""

from django.contrib import admin
from .models import Category, Product


class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for Category model.
    Displays friendly name and internal name,
    with search functionality.
    """
    list_display = ('friendly_name', 'name',)
    search_fields = ('name', 'friendly_name',)


class ProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for Product model.
    Displays key product information with filtering
    and search capabilities.
    
    Features:
    - Sortable by SKU
    - Searchable by name and description
    - Filterable by category and restrictions
    """
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
        'stock',
        'requires_prescription',
        'is_professional_only',
    )
    ordering = ('sku',)
    search_fields = ('name', 'description',)
    list_filter = ('category', 'requires_prescription', 'is_professional_only',)


# Register models with their respective admin classes
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
