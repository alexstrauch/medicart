"""
Views for the home app.
Handles rendering of the homepage and email testing functionality.
"""

from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings
from products.models import Product, Category


def index(request):
    """ A view to return the index page """
    featured_products = Product.objects.filter(rating__gte=4)[:4]
    categories = Category.objects.all()

    context = {
        'featured_products': featured_products,
        'categories': categories,
    }
    
    return render(request, 'home/index.html', context)


def test_email(request):
    """Test email functionality.
    
    Attempts to send a test email using the configured email settings.
    Used for verifying email functionality in the application.
    
    Args:
        request: HTTP request object
        
    Returns:
        HttpResponse: Success or error message indicating the email status
    """
    try:
        # Send test email to the default email address
        send_mail(
            'Test Email',
            'This is a test email from MediCart.',
            settings.DEFAULT_FROM_EMAIL,
            [settings.DEFAULT_FROM_EMAIL],  # Sending to yourself
            fail_silently=False,
        )
        return HttpResponse('Email sent successfully!')
    except Exception as e:
        return HttpResponse(f'Error sending email: {str(e)}')
