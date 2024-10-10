from django.shortcuts import render
from .models import Product, ProductCategory
from django.db.models import Sum


def index(request):
    return render(request, 'index.html')


def products(request):
    categories = ProductCategory.objects.annotate(total_quantity=Sum('products__quantity'))

    context = {
        'title': 'Каталог',
        'products': Product.objects.filter(quantity__gte=1),
        'categories': categories.filter(total_quantity__gte=1),
    }

    return render(request, 'products/products.html', context)
