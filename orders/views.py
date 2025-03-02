"""
Views for the orders app.

This app is responsible for displaying order history to logged-in users.
It is separate from the checkout app because:
1. Checkout handles the process of creating orders
2. Orders handles the display and management of completed orders
3. This separation follows the Single Responsibility Principle

The main view aggregates all orders for a user and displays them
with calculated totals and delivery costs.
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from checkout.models import Order
from django.db.models import Sum, F


@login_required
def orders(request):
    """
    Display the user's order history.

    This view retrieves all orders associated with the logged-in user
    and calculates various totals for each order including:
    - Order total (sum of all line items)
    - Delivery cost
    - Grand total (order total + delivery)

    Orders are sorted by date with most recent first.

    Args:
        request: HttpRequest object containing user data

    Returns:
        HttpResponse: Rendered orders history page

    Notes:
        - Requires user authentication (enforced by @login_required)
        - Uses annotate to calculate totals at the database level
        - Orders are sorted with newest first (-date)
    """
    # Get orders and annotate with calculated totals
    orders = Order.objects.filter(user_profile=request.user.userprofile)\
        .annotate(
            calculated_total=Sum('lineitems__lineitem_total'),
            calculated_delivery=F('delivery_cost'),
            calculated_grand_total=F('calculated_total') + F('delivery_cost')
        ).order_by('-date')
    
    template = 'orders/orders.html'
    context = {
        'orders': orders,
    }
    
    return render(request, template, context)
