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


admin.site.register(Product, ProductAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Category, CategoryAdmin)
