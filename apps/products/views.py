from django.shortcuts import render
from .models import Product, ProductCategory
from django.db.models import Sum


def index(request):
    context = {
        'title': 'Grace of the Gods',
    }
    return render(request, 'index.html', context)


def products(request, category_id=None):
    categories = ProductCategory.objects.annotate(total_quantity=Sum('products__quantity'))
    available_products = Product.objects.filter(quantity__gte=1)
    if category_id:
        available_products = available_products.filter(category__id=category_id)
    context = {
        'title': 'Каталог',
        'products': available_products,
        'categories': categories.filter(total_quantity__gte=1),
        'category_id': category_id,
    }

    return render(request, 'products/products.html', context)
