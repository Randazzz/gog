from django.urls import path

from apps.products.views import basket_add, basket_remove, products

app_name = 'products'

urlpatterns = [
    path('', products, name='index'),
    path('category/<int:category_id>/', products, name='product_by_category'),
    path('basket/<int:product_id>', basket_add, name='basket_add'),
    path('profile/<int:basket_id>', basket_remove, name='basket_remove'),
]
