from django.urls import path
from django.views.decorators.cache import cache_page

from apps.products.views import ProductsListView, basket_add, basket_remove

app_name = 'products'

urlpatterns = [
    path('', cache_page(30)(ProductsListView.as_view()), name='index'),
    path('category/<int:category_id>/', cache_page(30)(ProductsListView.as_view()), name='product_by_category'),
    path('basket/<int:product_id>', basket_add, name='basket_add'),
    path('profile/<int:basket_id>', basket_remove, name='basket_remove'),
]
