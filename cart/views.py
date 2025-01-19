"""
Views for managing shopping cart functionality.
Includes adding, removing, and adjusting product quantities.
"""

from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages
from products.models import Product


def view_cart(request):
    """ 
    A view that renders the cart contents page.
    Displays all items currently in the shopping cart.
    """
    return render(request, 'cart/cart.html')


def add_to_cart(request, product_id):
    """ 
    Add a quantity of the specified product to the shopping cart.
    Handles both new items and quantity updates for existing items.
    Parameters:
        - product_id: ID of the product to add
        - quantity: Amount to add (from POST data)
    """
    product = get_object_or_404(Product, pk=product_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})
    
    # Convert product_id to string since session keys are strings
    str_product_id = str(product_id)

    if str_product_id in cart:
        cart[str_product_id] += quantity
        messages.success(request, f'Updated {product.name} quantity to {cart[str_product_id]}')
    else:
        cart[str_product_id] = quantity
        messages.success(request, f'Added {product.name} to your cart')

    request.session['cart'] = cart
    return redirect(redirect_url)


def adjust_cart(request, product_id):
    """
    Adjust the quantity of the specified product to the specified amount.
    If quantity is set to 0, the item is removed from the cart.
    Parameters:
        - product_id: ID of the product to adjust
        - quantity: New quantity (from POST data)
    """
    product = get_object_or_404(Product, pk=product_id)
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})
    
    # Convert product_id to string since session keys are strings
    str_product_id = str(product_id)

    if quantity > 0:
        cart[str_product_id] = quantity
        messages.success(request, f'Updated {product.name} quantity to {cart[str_product_id]}')
    else:
        cart.pop(str_product_id)
        messages.success(request, f'Removed {product.name} from your cart')

    request.session['cart'] = cart
    return redirect(reverse('view_cart'))


def remove_from_cart(request, product_id):
    """
    Remove the item from the shopping cart.
    Handles AJAX requests for item removal.
    Parameters:
        - product_id: ID of the product to remove
    Returns:
        - HTTP 200: Success
        - HTTP 404: Product not found
        - HTTP 500: Error removing item
    """
    try:
        product = get_object_or_404(Product, pk=product_id)
        cart = request.session.get('cart', {})
        
        # Convert product_id to string since session keys are strings
        str_product_id = str(product_id)
        
        if str_product_id in cart:
            cart.pop(str_product_id)
            messages.success(request, f'Removed {product.name} from your cart')

        request.session['cart'] = cart
        return HttpResponse(status=200)
        
    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
