from django.shortcuts import render


def orders(request):
    return render(request, 'orders/orders.html')


def order_detail(request):
    return render(request, 'orders/order.html')
