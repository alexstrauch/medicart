"""
Views for the products app.
Handles product listing and details functionality.
"""

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Product, Category
from wishlist.models import Wishlist


def all_products(request):
    """
    A view to show all products, including sorting and search queries.
    
    Supports:
    - Sorting by name, category, etc.
    - Filtering by category
    - Search by name and description
    - Direction (ascending/descending)
    """
    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}' if sort and direction else None

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """
    Display detailed information for a specific product.

    Shows comprehensive product information including:
    - Basic details (name, price, category)
    - Full description
    - Stock status
    - Medical requirements (prescription/professional)
    - Image if available

    Args:
        request: HttpRequest object
        product_id (int): Primary key of the product to display

    Returns:
        HttpResponse: Rendered product detail page

    Raises:
        Http404: If product_id doesn't exist
    """
    product = get_object_or_404(Product, pk=product_id)

    # Check if product is in user's wishlist and get user's review if it exists
    in_wishlist = False
    user_review = None
    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()
        user_review = product.reviews.filter(user=request.user).first()

    context = {
        'product': product,
        'in_wishlist': in_wishlist,
        'user_review': user_review,
    }

    return render(request, 'products/product_detail.html', context)

