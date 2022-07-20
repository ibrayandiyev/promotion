from django.urls import path
from django.conf.urls import url

from .views import Index
from .views import About
from .views import Contact
from .views import ProductContact
from .views import category_product
from .views import subcategory_product
from .views import ajax_search_front_product
from .views import DetailProduct

urlpatterns = [
	url(r'^$', Index.as_view(), name='index'),
	url(r'about-us', About.as_view(), name='about-us'),
	url(r'prod-contact-us/(?P<prod_id>.+)/(?P<quantity>\d+)$', ProductContact.as_view(), name='product-contact-us'),
	url(r'contact-us', Contact.as_view(), name='contact-us'),
	
	url(r'^categories/(?P<category>.+)/(?P<pk>\d+)$', category_product, name='categories'),
	url(r'^subcategories/(?P<category>.+)/(?P<subcategory>.+)/(?P<pk>\d+)$', subcategory_product, name='subcategories'),

	url(r'^product/(?P<pk>\d+)$', DetailProduct.as_view(), name='product'),

	url(r'^ajax-search-front-product/$', ajax_search_front_product, name='ajax-search-front-product'),
]