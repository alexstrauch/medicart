"""
URL configuration for the MediCart project.

This module defines the URL routing for the entire project, including:
- Admin interface access
- User authentication routes
- App-specific URLs
- Static and media file serving
- XML sitemap generation
- Custom error handlers

The URLs are structured to provide a clean and intuitive API structure
while maintaining Django's best practices for URL organization.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap, ProductSitemap, CategorySitemap
from . import views

# Register custom error handlers
handler404 = 'medicart.views.handler404'  # Page not found
handler500 = 'medicart.views.handler500'  # Server error
handler502 = 'medicart.views.handler502'  # Bad gateway

# Configure sitemaps for SEO
sitemaps = {
    'static': StaticViewSitemap,     # Static pages like home
    'products': ProductSitemap,       # Product detail pages
    'categories': CategorySitemap,    # Category listing pages
}

# Main URL patterns
urlpatterns = [
    # Django admin interface
    path('admin/', admin.site.urls),
    
    # User authentication (provided by django-allauth)
    path('accounts/', include('allauth.urls')),
    
    # App-specific URLs
    path('products/', include('products.urls')),    # Product browsing and detail
    path('cart/', include('cart.urls')),           # Shopping cart management
    path('checkout/', include('checkout.urls')),    # Order checkout process
    path('profile/', include('profiles.urls')),     # User profile management
    path('orders/', include('orders.urls')),        # Order history and tracking
    path('marketing/', include('marketing.urls')),   # Newsletter and promotions
    path('wishlist/', include('wishlist.urls', namespace='wishlist')),  # Wishlist functionality
    path('contact/', include('contact.urls', namespace='contact')),  # Contact form and history
    path('reviews/', include('reviews.urls', namespace='reviews')),  # Product reviews
    path('', include('home.urls')),                 # Homepage and static pages
    
    # XML sitemap for search engines
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, 
         name='django.contrib.sitemaps.views.sitemap'),
] 

# Serve media files in development and production
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files in development only
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
