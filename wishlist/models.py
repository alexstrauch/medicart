from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Wishlist(models.Model):
    """
    Wishlist model to allow users to save products they're interested in.
    Each user can have multiple products in their wishlist.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensure each product can only be in a user's wishlist once
        unique_together = ('user', 'product')
        ordering = ['-date_added']  # Most recently added first

    def __str__(self):
        return f'{self.user.username}\'s wishlist item: {self.product.name}'
