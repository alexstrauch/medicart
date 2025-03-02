"""
Context processor for the shopping cart functionality.
Provides cart data and calculations to all templates in the application.
Handles product totals, delivery costs, and free delivery threshold logic.
"""

from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def cart_contents(request):
    """
    Calculate and return the current state of the shopping cart.
    
    Args:
        request: The HTTP request object containing the session
    
    Returns:
        dict: Context dictionary containing:
            - cart_items: List of dictionaries with product and quantity info
            - total: Total cost of all items
            - product_count: Total number of items
            - delivery: Calculated delivery cost
            - free_delivery_delta: Amount needed to reach free delivery
            - free_delivery_threshold: Minimum amount for free delivery
            - grand_total: Total including delivery
    """
    cart_items = []
    total = 0
    product_count = 0
    cart = request.session.get('cart', {})

    # Iterate through cart items and calculate totals
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        total += quantity * product.price
        product_count += quantity
        cart_items.append({
            'product_id': product_id,
            'quantity': quantity,
            'product': product,
        })

    # Calculate delivery costs and free delivery delta
    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0
    
    grand_total = delivery + total
    
    # Prepare the context dictionary for template rendering
    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context
