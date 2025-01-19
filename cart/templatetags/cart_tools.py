from django import template
from decimal import Decimal, InvalidOperation

register = template.Library()

@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    return price * quantity

@register.filter(name='format_price')
def format_price(price):
    if price is None:
        return "0.00 €"
    try:
        # Convert to Decimal if it's a string
        if isinstance(price, str):
            price = Decimal(price)
        return f"{float(price):.2f} €"
    except (ValueError, TypeError, InvalidOperation):
        return "0.00 €"
