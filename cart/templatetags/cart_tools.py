"""
Template filters for cart calculations and price formatting.
Provides custom template filters for calculating subtotals and formatting prices.
"""

from django import template
from decimal import Decimal, InvalidOperation

register = template.Library()

@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    """
    Calculate the subtotal for a line item.
    
    Args:
        price (Decimal): The price per unit
        quantity (int): The quantity of items
    
    Returns:
        Decimal: The calculated subtotal (price * quantity)
    """
    return price * quantity

@register.filter(name='format_price')
def format_price(price):
    """
    Format a price value with Euro symbol and two decimal places.
    
    Args:
        price (Decimal|str|None): The price to format
    
    Returns:
        str: Formatted price string (e.g., '10.99 €')
             Returns '0.00 €' if price is None or invalid
    """
    if price is None:
        return "0.00 €"
    try:
        # Convert to Decimal if it's a string
        if isinstance(price, str):
            price = Decimal(price)
        return f"{float(price):.2f} €"
    except (ValueError, TypeError, InvalidOperation):
        return "0.00 €"
