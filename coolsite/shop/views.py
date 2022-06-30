from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import RegisterUserForm, LoginUserForm
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
    #success_url = reverse_lazy('login')

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
