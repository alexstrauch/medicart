"""
Custom error handlers for the MediCart project.

This module defines custom error handlers to provide user-friendly
error pages when various HTTP errors occur. Each handler renders
a specific template designed to help users understand and recover
from the error.
"""

from django.shortcuts import render


def handler404(request, exception):
    """
    Handle 404 Page Not Found errors.
    
    Renders a custom template when a requested page cannot be found,
    helping users navigate back to valid content.
    
    Args:
        request: The HTTP request object
        exception: The exception that triggered the 404
        
    Returns:
        HttpResponse: Rendered 404 error page with 404 status code
    """
    return render(request, 'errors/404.html', status=404)


def handler500(request):
    """
    Handle 500 Internal Server Error.
    
    Renders a custom template when a server error occurs,
    providing users with appropriate information while maintaining security.
    
    Args:
        request: The HTTP request object
        
    Returns:
        HttpResponse: Rendered 500 error page with 500 status code
    """
    return render(request, 'errors/500.html', status=500)


def handler502(request):
    """
    Handle 502 Bad Gateway Error.
    
    Renders a custom template when there's a problem with the server
    gateway, typically during deployment or server maintenance.
    
    Args:
        request: The HTTP request object
        
    Returns:
        HttpResponse: Rendered 502 error page with 502 status code
    """
    return render(request, 'errors/502.html', status=502)
