from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *

menu = ["О сайте", "Добавить", "Обратная связь", "Войти"]

class ShopMain(ListView):
    model = Product
    template_name = 'shop/index.html'
    extra_context = {'title' : 'Главная', 'menu': menu}
    context_object_name = 'products'



class ShowProduct(DetailView):
    model = Product
    template_name = 'shop/product.html'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'
