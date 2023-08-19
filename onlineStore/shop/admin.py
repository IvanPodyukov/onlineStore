from django.contrib import admin

from shop.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass
