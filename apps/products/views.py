from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import Product, ProductCategory, Basket


def index(request):
    context = {
        'title': 'Grace of the Gods',
    }
    return render(request, 'index.html', context)


def products(request, category_id=None):
    product_categories = ProductCategory.objects.annotate(total_quantity=Sum('products__quantity'))
    available_products = Product.objects.filter(quantity__gte=1)
    if category_id:
        available_products = available_products.filter(category__id=category_id)
    product_list = available_products
    paginator = Paginator(product_list, 3)
    current_page_number = request.GET.get('page')
    paginated_products = paginator.get_page(current_page_number)
    context = {
        'title': 'Каталог',
        'paginated_products': paginated_products,
        'visible_categories': product_categories.filter(total_quantity__gte=1),
        'category_id': category_id,
    }

    return render(request, 'products/products.html', context)


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)
    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
