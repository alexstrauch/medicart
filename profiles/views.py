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
    """ Display the user's profile. """
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
                # Save the profile data first
                profile = form.save(commit=False)
                profile.save()
                
                # Update User model fields
                user = request.user
                user.first_name = form.cleaned_data.get('first_name', '')
                user.last_name = form.cleaned_data.get('last_name', '')
                user.save()
                
                messages.success(request, 'Profile updated successfully')
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
def professional_verification(request):
    """ Handle professional verification requests """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        license_number = request.POST.get('professional_license')
        if license_number:
            profile.professional_license = license_number
            profile.is_professional = True
            # In a real application, you would verify the license here
            profile.professional_verification = True
            profile.save()
            messages.success(request, 'Professional status verified successfully')
        else:
            messages.error(request, 'Please provide a valid license number')

    template = 'profiles/professional_verification.html'
    context = {
        'profile': profile,
    }

    return render(request, template, context)


@login_required
def delete_account(request):
    """Handle account deletion"""
    if request.method == 'POST':
        user = request.user
        # Logout the user first
        logout(request)
        # Delete the user account
        user.delete()
        messages.success(request, 'Your account has been successfully deleted.')
        return redirect('home')
    
    return redirect('profile')
