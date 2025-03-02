"""
Views for the marketing app.
Handles newsletter subscription functionality including Mailchimp integration.
"""

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
    Subscribe an email address to the Mailchimp mailing list.
    
    Uses Mailchimp's API to add a new subscriber with double opt-in verification.
    Handles existing subscribers and potential API errors.
    
    Args:
        email (str): Email address to subscribe
        
    Returns:
        tuple: (success, message)
            - success (bool): Whether the subscription was successful
            - message (str): Response message for the user
    """
    try:
        # Initialize Mailchimp client with API credentials
        client = MailchimpMarketing.Client()
        client.set_config({
            "api_key": settings.MAILCHIMP_API_KEY,
            "server": settings.MAILCHIMP_REGION
        })

        # Add subscriber with double opt-in verification
        response = client.lists.add_list_member(settings.MAILCHIMP_AUDIENCE_ID, {
            "email_address": email,
            "status": "pending",  # Use pending for double opt-in
            "status_if_new": "pending"  # Ensures new subscribers need to confirm
        })
        return True, "Thank you! Please check your email to confirm your subscription."
    except ApiClientError as error:
        error_message = error.text
        if "Member Exists" in error_message:
            return False, "You are already subscribed to our newsletter."
        return False, "An error occurred. Please try again later."
    except Exception as e:
        return False, "An error occurred. Please try again later."


def newsletter_signup(request):
    """
    Handle newsletter signup requests.
    
    Processes both AJAX and regular form submissions for newsletter signups.
    Validates email, creates local database record, and syncs with Mailchimp.
    Handles different response formats based on request type.
    
    Args:
        request: HTTP request object containing POST data with email
        
    Returns:
        JsonResponse: For AJAX requests, contains:
            - success (bool): Whether signup was successful
            - message (str): Response message for the user
        HttpResponse: For regular requests, renders homepage with
            appropriate flash messages
    """
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        
        try:
            # Validate email format
            validate_email(email)
            
            # Create or get subscriber in local database
            subscriber, created = NewsletterSubscriber.objects.get_or_create(
                email=email
            )
            
            # Attempt Mailchimp subscription
            success, message = subscribe_to_mailchimp(email)
            
            # Handle AJAX vs regular form submission
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
