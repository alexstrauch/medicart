"""Admin configuration for the contact app.

Customizes the admin interface for managing contact requests.
"""

from django.contrib import admin
from .models import ContactRequest


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    """Admin interface for managing contact requests."""
    
    list_display = (
        'created_at',
        'name',
        'subject',
        'status',
        'user',
    )
    list_filter = ('status', 'subject', 'created_at')
    search_fields = ('name', 'email', 'message', 'admin_notes')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'name', 'email')
        }),
        ('Request Details', {
            'fields': ('subject', 'message')
        }),
        ('Status & Notes', {
            'fields': ('status', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
