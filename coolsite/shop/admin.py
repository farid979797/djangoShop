from django.contrib import admin

from .models import *
# Register your models here

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'photo', 'description')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'description')

class CityAdmin(admin.ModelAdmin):
    list_display = ('name', )

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )

class ProfileAdmin(admin.ModelAdmin):\
    list_display = ('id', 'bio', 'photo', 'user_id', 'city_id', 'balance')


admin.site.register(Product, ProductAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Profile, ProfileAdmin)
