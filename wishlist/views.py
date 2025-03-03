"""
Views for the wishlist app.

This module provides views for managing user wishlists, including:
- Viewing the wishlist
- Adding/removing products from the wishlist
- Handling both standard requests and AJAX interactions
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from products.models import Product
from .models import Wishlist


@login_required
def view_wishlist(request):
    """Display the user's wishlist.

    Shows all products that the user has added to their wishlist,
    ordered by most recently added first.

    Args:
        request: HttpRequest object

    Returns:
        HttpResponse: Rendered wishlist page with all wishlist items

    Notes:
        - Requires user authentication (handled by @login_required)
        - Empty wishlist shows appropriate message to user
    """
    wishlist_items = Wishlist.objects.filter(user=request.user)
    context = {
        'wishlist_items': wishlist_items
    }
    return render(request, 'wishlist/wishlist.html', context)


@login_required
def toggle_wishlist(request, product_id):
    """Add or remove a product from the user's wishlist.

    If the product is already in the wishlist, it will be removed.
    If it's not in the wishlist, it will be added.

    Args:
        request: HttpRequest object
        product_id (int): ID of the product to toggle

    Returns:
        - For AJAX requests: JsonResponse with updated wishlist status
        - For standard requests: Redirect to previous page

    Notes:
        - Requires user authentication (handled by @login_required)
        - Handles both AJAX and standard form submissions
        - Shows success messages only for non-AJAX requests
        - Returns JSON with 'in_wishlist' status for AJAX requests
    """
    product = get_object_or_404(Product, pk=product_id)
    wishlist_item = Wishlist.objects.filter(user=request.user, product=product)

    if wishlist_item.exists():
        # Remove from wishlist
        wishlist_item.delete()
        if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            messages.success(request, f'{product.name} removed from your wishlist')
        in_wishlist = False
    else:
        # Add to wishlist
        Wishlist.objects.create(user=request.user, product=product)
        if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            messages.success(request, f'{product.name} added to your wishlist')
        in_wishlist = True

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'in_wishlist': in_wishlist
        })

    return redirect(request.META.get('HTTP_REFERER', 'products'))
