from django.urls import path, re_path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    path('', ShopMain.as_view(), name='home'),
    path('product/<slug:product_slug>/', ShowProduct.as_view(), name='product'),
    path('category/<slug:cat_slug>/', ProductCategory.as_view(), name='category'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
    path('login/', LoginUser.as_view(), name='login'),
    path('profile/<int:profile_id>/', Profile.as_view(), name='profile'),
    path('product/<slug:product_slug>/<int:product_id>/purchase', purchase, name='purchase'),
    path('history/', PurchasesHistory.as_view(), name='history'),
    path('addproduct/', AddProduct.as_view(), name='addproduct'),
]
