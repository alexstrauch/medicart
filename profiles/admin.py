"""
Admin configuration for the profiles app.
Provides admin interface for managing user profiles.
"""

from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for UserProfile model.
    Displays key user information and delivery details.
    """
    list_display = ('user', 'default_phone_number', 'default_town_or_city', 'default_country')
    list_filter = ('default_country',)
    search_fields = ['user__username', 'user__email', 'default_phone_number']
    ordering = ('user__username',)
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Contact Details', {
            'fields': ('default_phone_number',)
        }),
        ('Delivery Address', {
            'fields': (
                'default_street_address1',
                'default_street_address2',
                'default_town_or_city',
                'default_county',
                'default_postcode',
                'default_country'
            )
        }),
    )
