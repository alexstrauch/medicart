"""
Stripe webhook handling for the checkout app.
Processes webhook events from Stripe to handle payment intents
and ensure order creation even if checkout process is interrupted.
"""

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from checkout.webhook_handler import StripeWH_Handler

import stripe


@require_POST
@csrf_exempt
def webhook(request):
    print('\nWebhook endpoint called')
    print('Webhook received')
    print(f'Request method: {request.method}')
    print(f'Content type: {request.content_type}')
    print(f'Headers: {dict(request.headers)}')
    """
    Listen for webhooks from Stripe.
    
    Handles various webhook events:
    - payment_intent.succeeded: When payment is successful
    - payment_intent.payment_failed: When payment fails
    
    Returns:
        HttpResponse: Status code indicating success or failure
    """
    # Setup Stripe API configuration
    print('Setting up Stripe configuration...')
    wh_secret = settings.STRIPE_WH_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY
    print(f'Webhook secret present: {bool(wh_secret)}')
    print(f'Webhook secret starts with: {wh_secret[:4] if wh_secret else "None"}')

    # Get the webhook data and verify its signature
    payload = request.body
    print(f'Payload size: {len(payload)} bytes')
    
    try:
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        print(f'Signature header found: {sig_header[:10]}...')
    except KeyError:
        print('ERROR: Stripe signature header missing')
        return HttpResponse(status=400)
    
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, wh_secret
        )
    except ValueError as e:
        # Invalid payload
        print(f'ValueError: {str(e)}')
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print(f'SignatureVerificationError: {str(e)}')
        return HttpResponse(status=400)
    except Exception as e:
        print(f'Unexpected error: {str(e)}')
        return HttpResponse(content=str(e), status=400)

    # Set up a webhook handler
    handler = StripeWH_Handler(request)

    # Map webhook events to relevant handler functions
    event_map = {
        'payment_intent.succeeded': handler.handle_payment_intent_succeeded,
        'payment_intent.payment_failed': handler.handle_payment_intent_payment_failed,
    }

    # Get the webhook type from Stripe
    event_type = event['type']

    # If there's a handler for it, get it from the event map
    # Use the generic one by default
    event_handler = event_map.get(event_type, handler.handle_event)

    # Call the event handler with the event
    response = event_handler(event)
    return response
