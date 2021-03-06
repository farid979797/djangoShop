from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_extensions.db.fields import AutoSlugField
import string
import random

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='owner', verbose_name='Добавил')
    description = models.TextField(verbose_name="Описание")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категория")
    count = models.IntegerField(verbose_name="Количество")
    city = models.ForeignKey('City', on_delete=models.PROTECT, verbose_name="Город")
    price = models.IntegerField(verbose_name="Цена")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product', kwargs={'product_slug': self.slug})

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
    city = models.ForeignKey('City', on_delete=models.PROTECT, verbose_name="Город", default=1)
    balance = models.IntegerField(verbose_name="Баланс", default=0)

    def get_absolute_url(self):
        return reverse('profile', kwargs={'profile_id': self.pk})

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class City(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Город")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name


class Purchases(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='купил', verbose_name='купил')
    product = models.ForeignKey('Product', on_delete=models.PROTECT, verbose_name="Товар")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время покупки")
