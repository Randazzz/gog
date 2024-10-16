from django.shortcuts import render


def orders(request):
    context = {
        'title': 'Заказы'
    }
    return render(request, 'orders/orders.html', context)


def order_detail(request):
    context = {
        'title': 'Заказ #1'
    }
    return render(request, 'orders/order.html', context)
