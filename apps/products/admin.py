from django.contrib import admin

from .models import ProductCategory, Product

admin.site.register(ProductCategory)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')
    fields = (('name', 'category'), 'description', 'price', 'quantity', 'image')
    search_fields = ('name',)
    ordering = ('quantity',)
