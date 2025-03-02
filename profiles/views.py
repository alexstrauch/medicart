"""
Views for the profiles app.

This module provides views for managing user profiles, including:
- Profile viewing and editing
- Password changing
- Order history viewing
- Account deletion

All views in this module require user authentication.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Sum, F

from .models import UserProfile
from .forms import UserProfileForm
from checkout.models import Order


@login_required
def profile(request):
    """
    Display and handle updates to the user's profile.

    This view handles:
    1. GET requests: Display profile and order history
    2. POST requests:
       - Profile information updates
       - Password changes

    Args:
        request: HttpRequest object

    Returns:
        HttpResponse: Rendered profile page with:
        - User's profile information
        - Order history
        - Forms for profile and password updates
    """
    profile = get_object_or_404(UserProfile, user=request.user)
    orders = profile.orders.all().order_by('-date')

    if request.method == 'POST':
        if 'password_change' in request.POST:
            # Handle password change
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('profile')
            else:
                messages.error(request, 'Please correct the errors below.')
        else:
            # Handle profile update
            form = UserProfileForm(request.POST, instance=profile)
            if form.is_valid():
                profile = form.save(commit=False)
                
                # Update User model fields
                user = request.user
                user.first_name = form.cleaned_data.get('first_name', '')
                user.last_name = form.cleaned_data.get('last_name', '')
                user.save()
                
                # Now save the profile with the updated user reference
                profile.user = user
                profile.save()
                
                # Re-fetch the profile to ensure we have the latest data
                profile = UserProfile.objects.get(user=request.user)
                
                messages.success(request, 'Profile updated successfully')
                
                # Redirect with updated data
                return redirect('profile')
            else:
                messages.error(request, 'Update failed. Please ensure the form is valid.')
                print(form.errors)  # This will help debug any form validation errors
    else:
        form = UserProfileForm(instance=profile, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        })
        password_form = PasswordChangeForm(request.user)

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'password_form': password_form,
        'orders': orders,
        'on_profile_page': True,
        'profile': profile,  # Add this to ensure profile is in the context
    }

    return render(request, template, context)


@login_required
def order_history(request, order_number):
    """
    Display details of a specific past order.

    Retrieves and displays a past order with calculated totals.
    Uses annotations to recalculate order totals for verification.

    Args:
        request: HttpRequest object
        order_number (str): The unique order number to display

    Returns:
        HttpResponse: Rendered order details using checkout success template

    Notes:
        - Annotates the order query to calculate totals
        - Uses checkout success template with from_profile flag
        - Shows informational message about past order
    """
    order = get_object_or_404(Order.objects.annotate(
        calculated_total=Sum('lineitems__lineitem_total'),
        calculated_delivery=F('delivery_cost'),
        calculated_grand_total=F('calculated_total') + F('delivery_cost')
    ), order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)



@login_required
def delete_account(request):
    """
    Handle user account deletion requests.

    Permanently deletes the user account and all associated data.
    Only processes deletion on POST request as a safety measure.

    Args:
        request: HttpRequest object

    Returns:
        HttpResponse: 
            - POST: Redirect to home after successful deletion
            - GET: Redirect to profile (deletion requires POST)

    Notes:
        - Requires login
        - Logs out user before deletion
        - Cascading delete removes profile and related data
        - Action is irreversible
    """
    if request.method == 'POST':
        user = request.user
        # Logout the user first
        logout(request)
        # Delete the user account
        user.delete()
        messages.success(request, 'Your account has been successfully deleted.')
        return redirect('home')
    
    return redirect('profile')
