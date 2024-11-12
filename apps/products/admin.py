import stripe
from django.conf import settings
from django.contrib import admin

from .models import Product, ProductCategory

admin.site.register(ProductCategory)

stripe.api_key = settings.STRIPE_SECRET_KEY


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')
    fields = (
        ('name', 'category'),
        'description',
        ('price', 'stripe_product_price_id'),
        'quantity',
        'image'
    )
    search_fields = ('name',)
    ordering = ('quantity',)
