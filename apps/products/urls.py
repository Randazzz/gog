from django.urls import path

from apps.products.views import ProductsListView, basket_add, basket_remove

app_name = 'products'

urlpatterns = [
    path('', ProductsListView.as_view(), name='index'),
    path('category/<int:category_id>/', ProductsListView.as_view(), name='product_by_category'),
    path('basket/<int:product_id>', basket_add, name='basket_add'),
    path('profile/<int:basket_id>', basket_remove, name='basket_remove'),
]
