from django.http import JsonResponse
from django.shortcuts import render
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import NewsletterSubscriber

# Create your views here.

def newsletter_signup(request):
    """Handle newsletter signup"""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        
        try:
            # Validate email
            validate_email(email)
            
            # Try to create subscriber
            subscriber, created = NewsletterSubscriber.objects.get_or_create(
                email=email
            )
            
            if created:
                message = 'Thank you for subscribing to our newsletter!'
                success = True
            else:
                message = 'You are already subscribed to our newsletter.'
                success = False
                
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': success,
                    'message': message
                })
            else:
                if success:
                    messages.success(request, message)
                else:
                    messages.info(request, message)
                
        except ValidationError:
            message = 'Please enter a valid email address.'
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': message
                })
            else:
                messages.error(request, message)
        except Exception as e:
            message = 'An error occurred. Please try again.'
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': message
                })
            else:
                messages.error(request, message)
    
    return render(request, 'home/index.html')
