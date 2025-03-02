"""
Models for the products app.
Defines the data structure for products and categories.
"""

from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Category(models.Model):
    """
    Category model for grouping products.
    Provides both internal name and customer-friendly display name.
    """
    class Meta:
        verbose_name_plural = 'Categories'
        
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    def get_friendly_name(self):
        """Return the user-friendly name for display"""
        return self.friendly_name


class Product(models.Model):
    """
    Product model representing items for sale.
    Includes fields for medical products like prescription requirements
    and professional-only restrictions.
    """
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0.01)])
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image = CloudinaryField('image', null=True, blank=True)
    stock = models.IntegerField(default=0)
    requires_prescription = models.BooleanField(default=False)
    is_professional_only = models.BooleanField(default=False)
    last_modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

