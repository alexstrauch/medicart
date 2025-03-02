"""
Sitemap configuration for the MediCart project.

This module defines XML sitemaps for different types of content,
helping search engines discover and index the site's content.
It includes sitemaps for:
- Static pages (homepage)
- Product pages
- Category pages

Each sitemap class defines its own update frequency, priority,
and content selection criteria.
"""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.conf import settings
from products.models import Product, Category


class StaticViewSitemap(Sitemap):
    """
    Sitemap for static pages like the homepage.
    
    These pages change infrequently but are important for site navigation,
    so they have daily updates but medium priority.
    """
    priority = 0.5      # Medium priority for static pages
    changefreq = 'daily'
    protocol = 'https' if not settings.DEBUG else 'http'

    def items(self):
        """Return list of static page names."""
        return ['home']

    def location(self, item):
        """Get URL for each static page."""
        return reverse(item)


class ProductSitemap(Sitemap):
    """
    Sitemap for product detail pages.
    
    Product pages are the main content of the site, so they have
    high priority but weekly updates since product info changes
    less frequently.
    """
    changefreq = 'weekly'
    priority = 0.7      # High priority for product pages
    protocol = 'https' if not settings.DEBUG else 'http'

    def items(self):
        """Return all active products."""
        return Product.objects.all()

    def lastmod(self, obj):
        """Get last modification date of product."""
        return obj.last_modified

    def location(self, obj):
        """Get URL for each product."""
        return f'/products/{obj.id}/'


class CategorySitemap(Sitemap):
    """
    Sitemap for category listing pages.
    
    Category pages are important for navigation but less so than
    individual products, hence the slightly lower priority.
    """
    changefreq = 'weekly'
    priority = 0.6      # Medium-high priority for category pages
    protocol = 'https' if not settings.DEBUG else 'http'

    def items(self):
        """Return all product categories."""
        return Category.objects.all()

    def location(self, obj):
        """Get URL for each category."""
        return f'/products/?category={obj.name}'
