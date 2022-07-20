from django.urls import path
from django.conf.urls import url

from django.contrib.auth.views import PasswordResetView 
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetCompleteView
from django.contrib.auth.views import PasswordChangeView

from .views import LoginView
from .views import LogoutView
from .views import Index
from .views import Profile
from .views import CategoryPage
from .views import ajax_add_category
from .views import ajax_order_category
from .views import ajax_delete_category
from .views import ajax_get_subcategory

from .views import ProductPage
from .views import ProductNew
from .views import ProductUpdate
from .views import ajax_delete_product
from .views import ajax_search_product
from .views import CategoryProduct
from .views import ajax_order_index_product
from .views import ajax_remove_index_product

from .views import BannerPage
from .views import ajax_add_banner
from .views import ajax_order_banner
from .views import ajax_delete_banner

from .views import About
from .views import ajax_save_about

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^index/$', Index.as_view(), name='admin-index'),
    url(r'^profile/(?P<pk>\d+)/$', Profile.as_view(), name='profile'),
    url(r'^category/$', CategoryPage.as_view(), name='category'),
    url(r'^ajax-add-category/$', ajax_add_category, name='ajax-add-category'),
    url(r'^ajax-order-category/$', ajax_order_category, name='ajax-order-category'),
    url(r'^ajax-delete-category/$', ajax_delete_category, name='ajax-delete-category'),

    url(r'^products/$', ProductPage.as_view(), name='products'),
    url(r'^new-product/$', ProductNew.as_view(), name='new-product'),
    url(r'^update-product/(?P<pk>\d+)/$', ProductUpdate.as_view(), name='update-product'),
    url(r'^ajax-get-subcategory/$', ajax_get_subcategory, name='ajax-get-subcategory'),
    url(r'^ajax-delete-product/$', ajax_delete_product, name='ajax-delete-product'),
    url(r'^ajax-search-product/$', ajax_search_product, name='ajax-search-product'),
    url(r'^categories-product/(?P<pk>\d+)/$', CategoryProduct.as_view(), name='categories-product'),
    url(r'^ajax-order-index-product/$', ajax_order_index_product, name='ajax-order-index-product'),
    url(r'^ajax-remove-index-product/$', ajax_remove_index_product, name='ajax-remove-index-product'),

    url(r'^banner/$', BannerPage.as_view(), name='banner'),
    url(r'^ajax-add-banner/$', ajax_add_banner, name='ajax-add-banner'),
    url(r'^ajax-order-banner/$', ajax_order_banner, name='ajax-order-banner'),
    url(r'^ajax-delete-banner/$', ajax_delete_banner, name='ajax-delete-banner'),

    url(r'^about/$', About.as_view(), name='about'),
    url(r'^ajax-save-about/$', ajax_save_about, name='ajax-save-about'),

    url(r'^reset/password/$', PasswordResetView.as_view(template_name='password_reset_form.html', email_template_name='password_reset_email.html'), name='password_reset'),
    url(r'^reset/password/reset/done/$', PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    url(r'^reset/done/$', PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    url(r'^change/password/(?P<pk>[0-9]+)/$', PasswordChangeView.as_view(template_name='password_change.html', success_url='/'), name='change_password'),
    
]