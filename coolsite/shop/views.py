from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.db.models import Q, F
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import RegisterUserForm, LoginUserForm, AddProductForm
from .models import *
from .utils import DataMixin


class ShopMain(DataMixin, ListView):
    model = Product
    template_name = 'shop/index.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):  #для передачи динамических данных
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная траница')        #in utils.py  DataMixin
        context.update(c_def)
        return context

    def get_queryset(self):
        return Product.objects.filter(is_published=True)

class ShowProduct(DataMixin, DetailView):
    model = Product
    template_name = 'shop/product.html'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'

    def get_context_data(self, *, object_list=None, **kwargs):  #для передачи динамических данных
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(name=context['product'])        #in utils.py  DataMixin
        context.update(c_def)
        return context

class ProductCategory(DataMixin, ListView):
    model = Product
    template_name = 'shop/index.html'
    context_object_name = 'products'
    parent_id = 0
    #allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):  #для передачи динамических данных
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name),
                                      cat_selected=c.pk)        #in utils.py  DataMixin
        context.update(c_def)
        return context

    def get_queryset(self, object_list=None, **kwargs):
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        if c.parent_category is None:
            return Product.objects.filter(Q(cat__parent_category=c.pk) | (Q(pk=c.pk)))
        else:
            return Product.objects.filter(cat__slug=self.kwargs['cat_slug'])


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm                           #in forms.py
    template_name = 'shop/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        context.update(c_def)
        return context

def logout_user(request):
    logout(request)
    return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'shop/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        context.update(c_def)
        return context

    def get_success_url(self):
        return reverse_lazy('home')


class Profile(DataMixin, DetailView):
    model = Profile
    template_name = 'shop/profile.html'
    pk_url_kwarg = 'profile_id'
    context_object_name = 'profile'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Профиль - ' + str(self.request.user))
        context.update(c_def)
        return context

def purchase(request, product_id, product_slug):
    p = Purchases(user_id=request.user.id, product_id=product_id)
    p.save()
    Product.objects.filter(pk=product_id).update(count=F('count') - 1)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class PurchasesHistory(DataMixin, ListView):
    model = Purchases
    template_name = 'shop/purchase_history.html'
    context_object_name = 'purchases'

    def get_context_data(self, *, object_list=None, **kwargs):  #для передачи динамических данных
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='История покупок')
        context.update(c_def)
        return context

    def get_queryset(self):
        return Purchases.objects.filter(user=self.request.user.id)

class AddProduct(LoginRequiredMixin, DataMixin, CreateView):                                 # @login_required если функции представления
    form_class = AddProductForm
    template_name = 'shop/addproduct.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):  #для передачи динамических данных
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление объявление')
        context.update(c_def)
        return context

    def get_initial(self):
        return {'owner': self.request.user.id}
