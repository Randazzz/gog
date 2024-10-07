from django.urls import path

from apps.orders.views import orders, order_detail

app_name = 'orders'

urlpatterns = [
    path('', orders, name='index'),
    path('order/', order_detail, name='order'),
]
