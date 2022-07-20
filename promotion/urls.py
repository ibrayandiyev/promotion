"""promotion URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url

from django.contrib.sitemaps.views import sitemap

from frontend import views as front_view

from backend.sitemaps import Static_Sitemap
from backend.sitemaps import Article_Sitemap
from backend.sitemaps import Banner_Sitemap

from django.views.generic.base import TemplateView

sitemaps = {
    'article': Article_Sitemap(),
    'static': Static_Sitemap(),
    'banner': Banner_Sitemap(),
}

handler404 = front_view.handler404
handler500 = front_view.handler500

urlpatterns = [
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^admin/', include('backend.urls')),
    url(r'^', include('frontend.urls')),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    url(r'^robots\.txt$', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)