from django.contrib.sitemaps import Sitemap
from django.urls import reverse, reverse_lazy
from django.utils import translation

from .models import Product, Banner

class Static_Sitemap(Sitemap):

    priority = 1.0
    changefreq = 'yearly'

    def items(self):
        return ['products', 'category']

    def location(self, item):
        return reverse(item)

class Article_Sitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7
    i18n = True

    def items(self):
        actual_lang = translation.get_language()
        if actual_lang == 'es':
            idlang = 2
        elif actual_lang == 'en':
            idlang = 1
        return Product.objects.filter(language_id=idlang)

    def location(self, obj):
        return "/admin/categories-product/" + str(obj.name) + "/" + str(obj.language_id)

class Banner_Sitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7

    def items(self):
        return Banner.objects.all()

    def location(self, obj):
        return "/admin/banner/" + str(obj.name) + "/"

    