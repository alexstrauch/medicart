from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from checkout.models import Order
from django.db.models import Sum, F


@login_required
def orders(request):
    """Display the user's orders."""
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
