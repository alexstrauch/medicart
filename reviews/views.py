from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from products.models import Product
from .models import ProductReview
from .forms import ProductReviewForm


@login_required
def add_review(request, product_id):
    """
    Add or edit a review for a product.
    If the user has already reviewed this product, their existing review will be updated.
    """
    product = get_object_or_404(Product, pk=product_id)
    existing_review = ProductReview.objects.filter(user=request.user, product=product).first()

    if request.method == 'POST':
        form = ProductReviewForm(request.POST, instance=existing_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            messages.success(request, 'Your review has been saved!')
            return redirect('product_detail', product_id=product_id)
    else:
        form = ProductReviewForm(instance=existing_review)

    template = 'reviews/add_review.html'
    context = {
        'form': form,
        'product': product,
        'existing_review': existing_review,
    }
    return render(request, template, context)


@login_required
def delete_review(request, review_id):
    """
    Delete a review.
    Users can only delete their own reviews.
    """
    review = get_object_or_404(ProductReview, pk=review_id, user=request.user)
    product_id = review.product.id
    review.delete()
    messages.success(request, 'Your review has been deleted!')
    return redirect('product_detail', product_id=product_id)
