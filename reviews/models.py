"""
Models for the product review system.

This module defines the database models for storing and managing product reviews.
It allows users to rate and review products, with each user being limited to
one review per product.
"""

from django.db import models
from django.db.models import Avg
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from products.models import Product


class ProductReview(models.Model):
    """
    Model representing a user's review of a product.

    Each review includes:
    - A rating (1-5 stars)
    - Review text
    - Creation timestamp
    - Link to the user who wrote it
    - Link to the product being reviewed

    Key features:
    - Users can only review each product once (enforced by unique_together)
    - Reviews are ordered by creation date (newest first)
    - When a user or product is deleted, their reviews are also deleted (CASCADE)
    """

    RATING_CHOICES = [
        (1, '1 - Poor'),        # Lowest rating
        (2, '2 - Fair'),        # Below average
        (3, '3 - Good'),        # Average
        (4, '4 - Very Good'),    # Above average
        (5, '5 - Excellent'),    # Highest rating
    ]
    
    # Foreign Keys and Relationships
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text='The user who wrote the review'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews',
        help_text='The product being reviewed'
    )
    
    # Review Content
    rating = models.IntegerField(
        choices=RATING_CHOICES,
        help_text='Rating from 1 (Poor) to 5 (Excellent)'
    )
    review_text = models.TextField(
        help_text='The actual review text'
    )
    
    # Metadata
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='When the review was created'
    )

    class Meta:
        ordering = ['-created_at']  # Most recent reviews appear first
        unique_together = ('user', 'product')  # Ensure one review per user per product
        verbose_name = 'Product Review'
        verbose_name_plural = 'Product Reviews'
        
    def __str__(self):
        """Return a string representation of the review."""
        return f'{self.user.username}\'s review of {self.product.name}'

    def update_product_rating(self):
        """Update the associated product's rating based on all its reviews."""
        # Calculate average rating from all reviews
        avg_rating = (
            ProductReview.objects
            .filter(product=self.product)
            .aggregate(Avg('rating'))['rating__avg']
        )
        
        # Update the product's rating field
        self.product.rating = round(avg_rating, 2) if avg_rating else None
        self.product.save()


@receiver(post_save, sender=ProductReview)
def update_rating_on_save(sender, instance, **kwargs):
    """Signal handler to update product rating when a review is created/updated."""
    instance.update_product_rating()


@receiver(post_delete, sender=ProductReview)
def update_rating_on_delete(sender, instance, **kwargs):
    """Signal handler to update product rating when a review is deleted."""
    instance.update_product_rating()
