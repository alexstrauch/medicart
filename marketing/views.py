from django.http import JsonResponse
from django.shortcuts import render
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.conf import settings
from .models import NewsletterSubscriber
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError


def subscribe_to_mailchimp(email):
    """
    Subscribe email to Mailchimp list
    """
    try:
        client = MailchimpMarketing.Client()
        client.set_config({
            "api_key": settings.MAILCHIMP_API_KEY,
            "server": settings.MAILCHIMP_REGION
        })

        response = client.lists.add_list_member(settings.MAILCHIMP_AUDIENCE_ID, {
            "email_address": email,
            "status": "subscribed"
        })
        return True, "Successfully subscribed to newsletter!"
    except ApiClientError as error:
        error_message = error.text
        if "Member Exists" in error_message:
            return False, "You are already subscribed to our newsletter."
        return False, "An error occurred. Please try again later."
    except Exception as e:
        return False, "An error occurred. Please try again later."


def newsletter_signup(request):
    """Handle newsletter signup"""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        
        try:
            # Validate email
            validate_email(email)
            
            # Try to create subscriber in local database
            subscriber, created = NewsletterSubscriber.objects.get_or_create(
                email=email
            )
            
            # Subscribe to Mailchimp
            success, message = subscribe_to_mailchimp(email)
            
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
            message = 'An error occurred. Please try again later.'
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': message
                })
            else:
                messages.error(request, message)
    
    return render(request, 'home/index.html')
