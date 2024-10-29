from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from .models import Basket, Product, ProductCategory


class IndexTemplateView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Grace of the Gods'
        return context


class ProductsListView(ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        queryset = Product.available()
        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)
        return queryset.order_by('id')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        visible_categories = ProductCategory.with_product_count().filter(total_quantity__gte=1)
        context['title'] = 'Каталог'
        context['visible_categories'] = visible_categories
        return context


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
