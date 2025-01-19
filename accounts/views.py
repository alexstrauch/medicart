"""
Views for handling user authentication and registration.
Includes functionality for user registration and login.
"""

from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm


def register(request):
    """
    Handle user registration.
    GET: Display registration form
    POST: Process registration form, create user, and log them in
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request, 
                "Registration successful! Welcome to MediCart!"
                )
            login(request, user)
            return redirect('home')
        else:
            messages.error(
                request, 
                "Registration failed. Please check the form and try again."
                )
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    """
    Handle user login.
    GET: Display login form
    POST: Authenticate user and log them in if credentials are valid
    """
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        # Attempt to authenticate the user
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(
                request, 
                f"Welcome back, {user.get_full_name() or user.email}!"
                )
            return redirect('home')
        else:
            messages.error(request, "Invalid email or password.")
    return render(request, 'accounts/login.html')
