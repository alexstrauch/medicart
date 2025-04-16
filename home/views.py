"""
Views for the home app.
Handles rendering of the homepage.
"""

from django.shortcuts import render
from products.models import Product, Category


def index(request):
    """ A view to return the index page """
    featured_products = Product.objects.filter(rating__gte=4)[:4]
    categories = Category.objects.all()

    context = {
        'featured_products': featured_products,
        'categories': categories,
    }

    return render(request, 'home/index.html', context)
