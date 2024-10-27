from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import Basket, Product, ProductCategory


def index(request):
    context = {
        'title': 'Grace of the Gods',
    }
    return render(request, 'index.html', context)


def products(request, category_id=None):
    visible_categories = ProductCategory.with_product_count().filter(total_quantity__gte=1)
    available_products = Product.available(category_id=category_id)

    paginator = Paginator(available_products, 3)
    current_page_number = request.GET.get('page')
    paginated_products = paginator.get_page(current_page_number)

    context = {
        'title': 'Каталог',
        'paginated_products': paginated_products,
        'visible_categories': visible_categories,
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
