"""Models for the contact app.

This module defines the data structure for storing and managing contact requests
from users. It includes status tracking and user association for logged-in users.
"""

from django.db import models
from django.contrib.auth.models import User


class ContactRequest(models.Model):
    """
    Model for storing contact form submissions.

    Attributes:
        user: Optional link to registered user (if logged in)
        name: Name of the person making contact
        email: Email address for correspondence
        subject: Topic or category of the inquiry
        message: Detailed message from the user
        status: Current state of the inquiry
        created_at: When the request was submitted
        updated_at: When the request was last modified
    """

    STATUS_CHOICES = [
        ('NEW', 'New'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
    ]

    SUBJECT_CHOICES = [
        ('GENERAL', 'General Inquiry'),
        ('PRODUCT', 'Product Question'),
        ('ORDER', 'Order Support'),
        ('TECHNICAL', 'Technical Support'),
        ('OTHER', 'Other'),
    ]

    # User Information
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text='Registered user who submitted the request (if logged in)'
    )
    name = models.CharField(
        max_length=100,
        help_text='Name of the person making contact'
    )
    email = models.EmailField(
        help_text='Email address for correspondence'
    )

    # Request Details
    subject = models.CharField(
        max_length=20,
        choices=SUBJECT_CHOICES,
        default='GENERAL',
        help_text='Category of the inquiry'
    )
    message = models.TextField(
        help_text='Detailed message from the user'
    )

    # Status and Tracking
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='NEW',
        help_text='Current status of the inquiry'
    )
    admin_notes = models.TextField(
        blank=True,
        null=True,
        help_text='Internal notes for staff (not visible to users)'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='When the request was submitted'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text='When the request was last modified'
    )

    class Meta:
        ordering = ['-created_at']  # Most recent first
        verbose_name = 'Contact Request'
        verbose_name_plural = 'Contact Requests'

    def __str__(self):
        """Return a string representation of the contact request."""
        return f'{self.subject} - {self.name} ({self.created_at.strftime("%Y-%m-%d %H:%M")})'
