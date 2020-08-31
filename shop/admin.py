from django.contrib import admin
from django.contrib.admin import ModelAdmin

from shop.models import (UserProfile, Visitor, Category, ProductImage, Product)


class UserProfileAdmin(ModelAdmin):
    list_per_page = 50
    list_display = ('django_user', 'ip')
    search_fields = ('django_user',)


class VisitorAdmin(ModelAdmin):
    list_per_page = 50
    list_display = ('product', 'ip')
    search_fields = ('product',)


class CategoryAdmin(ModelAdmin):
    list_per_page = 50
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'slug')
    search_fields = ('name',)


class ProductAdmin(ModelAdmin):
    list_per_page = 50
    list_display = ('name', 'is_available', 'views')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ('category', 'image')


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Visitor, VisitorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductImage, ModelAdmin)
admin.site.register(Product, ProductAdmin)
