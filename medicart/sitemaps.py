from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.conf import settings
from products.models import Product, Category

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'
    protocol = 'https' if not settings.DEBUG else 'http'

    def items(self):
        return ['home']

    def location(self, item):
        return reverse(item)

class ProductSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7
    protocol = 'https' if not settings.DEBUG else 'http'

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.last_modified

    def location(self, obj):
        return f'/products/{obj.id}/'

class CategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6
    protocol = 'https' if not settings.DEBUG else 'http'

    def items(self):
        return Category.objects.all()

    def location(self, obj):
        return f'/products/?category={obj.name}'
