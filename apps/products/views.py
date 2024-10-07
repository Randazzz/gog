from django.shortcuts import render
from .models import Product, ProductCategory


def index(request):
    return render(request, 'index.html')


def products(request):
    context = {
        'title': 'Каталог',
        'products': Product.objects.all(),
        'categories': ProductCategory.objects.all(),
    }
    return render(request, 'products/products.html', context)
