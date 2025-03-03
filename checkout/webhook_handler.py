"""
Stripe webhook handler for the checkout app.
Handles various webhook events from Stripe and processes payment intents.
Includes functionality for sending confirmation emails and creating orders.
"""

from django.http import HttpResponse
from django.db import transaction
import logging

logger = logging.getLogger(__name__)
from django.conf import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.template.loader import render_to_string
from django.conf import settings

from .models import Order, OrderLineItem
from products.models import Product
from profiles.models import UserProfile

import json
import time
import stripe


class StripeWH_Handler:
    """
    Handle Stripe webhooks for payment processing.
    Processes webhook events and manages order creation/confirmation.
    """

    def __init__(self, request):
        """
        Initialize handler with the request object.
        Args:
            request: The HTTP request object
        """
        self.request = request

    def _send_confirmation_email(self, order, status='success'):
        print('\n_send_confirmation_email method called')
        """Send the user a confirmation or failure email
        
        Args:
            order: The order instance
            status: 'success' or 'failure' to determine email type
        """
        cust_email = order.email
        
        if status == 'success':
            subject = render_to_string(
                'checkout/confirmation_emails/confirmation_email_subject.txt',
                {'order': order})
            body = render_to_string(
                'checkout/confirmation_emails/confirmation_email_body.txt',
                {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})
        else:
            subject = f'MediCart - Important Notice About Order {order.order_number}'
            body = f"""Dear {order.full_name},

We regret to inform you that there was an issue processing your recent order ({order.order_number}).

Reason: {status}

Your payment has not been processed, and no charges have been made to your account.

Please try placing your order again. If you continue to experience issues, contact us at {settings.DEFAULT_FROM_EMAIL}.

We apologize for any inconvenience.

Best regards,
The MediCart Team"""
        
        try:
            print('\nEmail Debug Information:')
            print(f'Attempting to send email to: {cust_email}')
            print(f'From email: {settings.DEFAULT_FROM_EMAIL}')
            print(f'SMTP settings: {settings.EMAIL_HOST}:{settings.EMAIL_PORT}')
            
            # Create message container
            msg = MIMEMultipart()
            msg['From'] = settings.DEFAULT_FROM_EMAIL
            msg['To'] = cust_email
            msg['Subject'] = subject
            
            # Add body to email
            msg.attach(MIMEText(body, 'plain'))
            
            try:
                from django.core.mail import EmailMessage
                email = EmailMessage(
                    subject,
                    body,
                    settings.DEFAULT_FROM_EMAIL,
                    [cust_email],
                )
                print('Attempting to send email using Django EmailMessage...')
                print(f'From: {settings.DEFAULT_FROM_EMAIL}')
                print(f'To: {cust_email}')
                print(f'Using host: {settings.EMAIL_HOST}')
                print(f'Using port: {settings.EMAIL_PORT}')
                print(f'Using SSL: {settings.EMAIL_USE_SSL}')
                print(f'Using TLS: {settings.EMAIL_USE_TLS}')
                email.send(fail_silently=False)
                
                print('Email sent successfully!')
                return True
                
            except smtplib.SMTPAuthenticationError as e:
                print(f'SMTP Authentication Error: {e}')
                print(f'Attempting to authenticate with: {settings.EMAIL_HOST_USER}')
                print('Please check your Gmail App Password and account settings')
                print('Make sure 2-Step Verification is enabled and you\'re using an App Password')
                return False
                
            except smtplib.SMTPException as e:
                print(f'SMTP Error: {e}')
                print('Please check your SMTP settings')
                return False
                
            except Exception as e:
                print(f'Unexpected error while sending email: {e}')
                print(f'Error type: {type(e).__name__}')
                return False
                
        except Exception as e:
            print(f'Error preparing email: {e}')
            print(f'Error type: {type(e).__name__}')
            return False

    def handle_event(self, event):
        """
        Handle generic/unknown/unexpected webhook events.
        Provides a fallback for unhandled webhook types.
        
        Args:
            event: The webhook event from Stripe
        Returns:
            HttpResponse: 200 status code with message
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        print('\nWebhook: handle_payment_intent_succeeded called')
        print('Processing payment intent...')
        """
        Handle successful payment intent webhooks.
        Creates or updates order when payment succeeds.
        
        Args:
            event: The webhook event from Stripe
        Returns:
            HttpResponse: Status indicating success or failure
        """
        intent = event.data.object
        pid = intent.id
        print(f'Payment Intent ID: {pid}')
        
        try:
            cart = intent.metadata.cart
            print(f'Cart found in metadata: {bool(cart)}')
            save_info = intent.metadata.save_info
            print(f'Save info: {save_info}')
        except AttributeError as e:
            print(f'Error accessing metadata: {str(e)}')
            return HttpResponse(content=f'Webhook error: {str(e)}', status=500)

        # Get the Charge object
        try:
            print(f'Retrieving charge for intent: {intent.latest_charge}')
            stripe_charge = stripe.Charge.retrieve(
                intent.latest_charge
            )
            print('Charge retrieved successfully')
        except Exception as e:
            print(f'Error retrieving charge: {str(e)}')
            return HttpResponse(content=f'Webhook error: {str(e)}', status=500)

        billing_details = stripe_charge.billing_details
        shipping_details = intent.shipping
        grand_total = round(stripe_charge.amount / 100, 2)

        # Clean data in the shipping details
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        # Update profile information if save_info was checked
        profile = None
        username = intent.metadata.username
        if username != 'AnonymousUser':
            profile = UserProfile.objects.get(user__username=username)
            if save_info:
                profile.default_phone_number = shipping_details.phone
                profile.default_country = shipping_details.address.country
                profile.default_postcode = shipping_details.address.postal_code
                profile.default_town_or_city = shipping_details.address.city
                profile.default_street_address1 = shipping_details.address.line1
                profile.default_street_address2 = shipping_details.address.line2
                profile.default_county = shipping_details.address.state
                profile.save()

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    town_or_city__iexact=shipping_details.address.city,
                    street_address1__iexact=shipping_details.address.line1,
                    street_address2__iexact=shipping_details.address.line2,
                    county__iexact=shipping_details.address.state,
                    grand_total=grand_total,
                    original_cart=cart,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exists:
            try:
                order.status = 'confirmed'
                order.save()
                self._send_confirmation_email(order, 'success')
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                    status=200)
            except Exception as e:
                logger.error(f'Error processing existing order: {str(e)}')
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {str(e)}',
                    status=200)
        else:
            order = None
            try:
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    user_profile=profile,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    town_or_city=shipping_details.address.city,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                    original_cart=cart,
                    stripe_pid=pid,
                )
                for item_id, item_data in json.loads(cart).items():
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    else:
                        for size, quantity in item_data['items_by_size'].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                            order_line_item.save()
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)
        try:
            order.status = 'confirmed'
            order.save()
            self._send_confirmation_email(order, 'success')
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
                status=200)
        except Exception as e:
            logger.error(f'Error processing new order: {str(e)}')
            if order:
                order.delete()
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | ERROR: {str(e)}',
                status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle failed payment intent webhooks.
        Sends failure notification to customer and logs failed payment attempts.
        
        Args:
            event: The webhook event from Stripe
        Returns:
            HttpResponse: 200 status code with message
        """
        intent = event.data.object
        
        try:
            # Try to find the order
            order = Order.objects.get(stripe_pid=intent.id)
            # Send failure email
            failure_reason = intent.last_payment_error.message if intent.last_payment_error else 'Payment verification failed'
            self._send_confirmation_email(order, status=failure_reason)
            
            # Update order status if needed
            order.status = 'failed'
            order.save()
            
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | Payment failed: {failure_reason}',
                status=200
            )
        except Order.DoesNotExist:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | No order found',
                status=200
            )
