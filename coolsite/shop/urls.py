from django.urls import path, re_path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    path('', ShopMain.as_view(), name='home'),
    path('product/<slug:product_slug>/', ShowProduct.as_view(), name='product'),
]
