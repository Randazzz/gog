from django.urls import path

from apps.products.views import products

app_name = 'products'

urlpatterns = [
    path('', products, name='index'),
]
