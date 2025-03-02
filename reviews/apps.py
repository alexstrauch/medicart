from django.apps import AppConfig


class ReviewsConfig(AppConfig):
    """
    Configuration for the reviews app.
    
    This app handles product reviews and ratings, allowing users to:
    - Rate products (1-5 stars)
    - Write text reviews
    - Edit their own reviews
    - View all reviews for a product
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reviews'
    verbose_name = 'Product Reviews'
