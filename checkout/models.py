"""
Models for the checkout app.
Defines Order and OrderLineItem models for handling e-commerce transactions.
Includes functionality for order number generation and total calculations.
"""
from django.db import models

# Create your models here.

import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings

from django_countries.fields import CountryField

from products.models import Product
from profiles.models import UserProfile


class Order(models.Model):
    """
    Order model representing a customer's purchase.
    Stores delivery information, costs, and links to line items.
    Includes status tracking and verification methods.
    """
    
    # Order status choices
    STATUS_PENDING = 'PENDING'
    STATUS_PAYMENT_CONFIRMED = 'PAYMENT_CONFIRMED'
    STATUS_PROCESSING = 'PROCESSING'
    STATUS_SHIPPED = 'SHIPPED'
    STATUS_DELIVERED = 'DELIVERED'
    STATUS_CANCELLED = 'CANCELLED'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_PAYMENT_CONFIRMED, 'Payment Confirmed'),
        (STATUS_PROCESSING, 'Processing'),
        (STATUS_SHIPPED, 'Shipped'),
        (STATUS_DELIVERED, 'Delivered'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]
    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                   null=True, blank=True, related_name='orders')
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    original_cart = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        help_text='Current status of the order'
    )
    payment_verified = models.BooleanField(
        default=False,
        help_text='Indicates if payment has been verified through Stripe webhook'
    )
    stock_verified = models.BooleanField(
        default=False,
        help_text='Indicates if stock levels were verified for all items'
    )
    notes = models.TextField(
        blank=True,
        help_text='Additional notes about the order (e.g., verification details)'
    )

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs.
        Calculates delivery cost based on FREE_DELIVERY_THRESHOLD.
        """
        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or 0
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
        else:
            self.delivery_cost = 0
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def verify_payment(self, stripe_charge):
        """
        Verify payment details with Stripe charge
        """
        if stripe_charge:
            verified_amount = round(stripe_charge.amount / 100, 2)
            if verified_amount == float(self.grand_total):
                self.payment_verified = True
                self.status = self.STATUS_PAYMENT_CONFIRMED
                self.notes = f'{self.notes}\nPayment verified with Stripe on {stripe_charge.created}'
                self.save()
                return True
        return False

    def verify_stock(self):
        """
        Verify stock levels for all items in the order
        """
        all_in_stock = True
        for item in self.lineitems.all():
            if item.quantity > item.product.stock:
                all_in_stock = False
                self.notes = f'{self.notes}\nInsufficient stock for {item.product.name}'
        
        self.stock_verified = all_in_stock
        self.save()
        return all_in_stock

    def process_order(self):
        """
        Process the order if payment and stock are verified
        """
        if self.payment_verified and self.stock_verified:
            # Update stock levels
            for item in self.lineitems.all():
                product = item.product
                product.stock -= item.quantity
                product.save()
            
            self.status = self.STATUS_PROCESSING
            self.notes = f'{self.notes}\nOrder processed and stock updated on {self.date}'
            self.save()
            return True
        return False

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    product_size = models.CharField(max_length=2, null=True, blank=True) # XS, S, M, L, XL
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)
        self.order.update_total()  # Update the order total after saving the line item

    def __str__(self):
        return f'SKU {self.product.sku} on order {self.order.order_number}'
