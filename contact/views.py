"""Views for the contact app.

This module handles the display and processing of contact forms,
as well as viewing contact history for authenticated users.
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .forms import ContactForm
from .models import ContactRequest


def contact(request):
    """
    Display and process the contact form.

    If the user is authenticated, pre-fill their information.
    On successful submission, send confirmation emails and redirect.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_request = form.save(commit=False)
            
            # Associate with user if logged in
            if request.user.is_authenticated:
                contact_request.user = request.user
            
            contact_request.save()

            # Send confirmation email to user
            context = {
                'contact': contact_request,
                'user': request.user if request.user.is_authenticated else None
            }
            
            subject = 'We received your message - MediCart'
            html_message = render_to_string(
                'contact/emails/confirmation_email.html',
                context
            )
            plain_message = render_to_string(
                'contact/emails/confirmation_email.txt',
                context
            )

            # Send confirmation to user
            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [contact_request.email],
                html_message=html_message,
            )

            # Send notification to admin
            admin_subject = f'New Contact Request: {contact_request.get_subject_display()}'
            admin_message = f"""New contact request received:

From: {contact_request.name} ({contact_request.email})
Subject: {contact_request.get_subject_display()}
Message:

{contact_request.message}

View in admin panel: {request.scheme}://{request.get_host}/admin/contact/contactrequest/{contact_request.id}/change/
"""
            
            send_mail(
                admin_subject,
                admin_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],  # Send to medicart.project@gmail.com
            )

            messages.success(
                request,
                'Your message has been sent! We will get back to you soon.'
            )
            return redirect('home')
        
        messages.error(
            request,
            'There was an error with your submission. Please check the form.'
        )
    else:
        # Pre-fill user information if logged in
        initial = {}
        if request.user.is_authenticated:
            initial['name'] = request.user.get_full_name() or request.user.username
            initial['email'] = request.user.email
        form = ContactForm(initial=initial)

    template = 'contact/contact.html'
    context = {
        'form': form,
        'on_profile_page': False
    }

    return render(request, template, context)
